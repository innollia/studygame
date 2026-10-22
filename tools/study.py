#!/usr/bin/env python3
"""게임기획 독학 관리 CLI (Python 3 표준 라이브러리 전용)."""

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUT_DIR = ROOT_DIR / "out"
SITE_DIR = ROOT_DIR / "site"

PLAN_PATH = DATA_DIR / "plan.json"
PROGRESS_PATH = DATA_DIR / "progress.json"
SECOND_PASS_PATH = DATA_DIR / "second-pass.json"

LEARNERS = ("innollia", "pai")
CRITERIA_IDS = ("lecture", "assignment", "apply", "feedback")


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def format_day_markdown(
    day_obj: dict,
    day_progress: dict | None = None,
    include_material_notes: bool = True,
) -> str:
    day_num = day_obj["day"]
    date_str = day_obj["date"]
    week = day_obj["week"]
    theme = day_obj["theme"]
    minutes = day_obj["minutes"]
    min_ver = day_obj["min_version_minutes"]
    is_analysis = day_obj.get("analysis_session", False)

    tag = " [분석 회차]" if is_analysis else ""
    lines = [
        f"# [D{day_num}] {date_str} ({week}주차){tag}",
        f"**주제**: {theme}",
        f"**예상 시간**: {minutes}분 (최소판 {min_ver}분)",
    ]

    if day_progress:
        inno_done = "완료 ✔" if day_progress.get("innollia", {}).get("done") else "미완료 ·"
        pai_done = "완료 ✔" if day_progress.get("pai", {}).get("done") else "미완료 ·"
        lines.append(f"**진도**: innollia [{inno_done}] | pai [{pai_done}]")

    lines.append("")
    lines.append("## 학습 자료")
    for mat in day_obj.get("materials", []):
        login_str = " *(로그인 필요)*" if mat.get("login_required") else ""
        line = f"- **{mat['title']}**{login_str}: {mat['url']}"
        if include_material_notes and mat.get("note"):
            line += f"\n  - {mat['note']}"
        lines.append(line)

    tasks = day_obj.get("tasks", {})
    lines.append("")
    lines.append("## 오늘 할 일")
    lines.append(f"- **공통**: {tasks.get('common', '')}")
    lines.append(f"- **innollia**: {tasks.get('innollia', '')}")
    lines.append(f"- **pai**: {tasks.get('pai', '')}")

    return "\n".join(lines)


def build_day_markdown_under_limit(
    day_obj: dict,
    day_progress: dict | None = None,
    limit: int = 2000,
) -> str:
    md = format_day_markdown(day_obj, day_progress, include_material_notes=True)
    if len(md) <= limit:
        return md
    md = format_day_markdown(day_obj, day_progress, include_material_notes=False)
    if len(md) <= limit:
        return md
    return md[: limit - 10] + "\n...(생략)"


def print_day_for_date(target_date: str) -> int:
    plan = load_json(PLAN_PATH)
    progress = load_json(PROGRESS_PATH)
    days = plan.get("days", [])
    if not days:
        print("계획 데이터가 비어 있습니다.")
        return 1

    first_day = days[0]
    last_day = days[-1]

    for d in days:
        if d["date"] == target_date:
            day_prog = progress.get("days", {}).get(str(d["day"]), {})
            print(format_day_markdown(d, day_prog, include_material_notes=True))
            return 0

    if target_date < first_day["date"]:
        print(
            f"[안내] {target_date}은(는) 계획 시작 전입니다. "
            f"(계획 기간: {first_day['date']} ~ {last_day['date']})"
        )
        print("아래는 첫날(D1) 할 일 안내입니다.\n")
        day_prog = progress.get("days", {}).get(str(first_day["day"]), {})
        print(format_day_markdown(first_day, day_prog, include_material_notes=True))
    else:
        print(
            f"[안내] {target_date}은(는) 계획 종료 후입니다. "
            f"(계획 기간: {first_day['date']} ~ {last_day['date']})"
        )
        print("아래는 마지막 날(D21) 할 일 안내입니다.\n")
        day_prog = progress.get("days", {}).get(str(last_day["day"]), {})
        print(format_day_markdown(last_day, day_prog, include_material_notes=True))
    return 0


def cmd_today(args: argparse.Namespace) -> int:
    target_date = args.date or datetime.date.today().isoformat()
    return print_day_for_date(target_date)


def cmd_tomorrow(args: argparse.Namespace) -> int:
    if getattr(args, "date", None):
        base_date = datetime.date.fromisoformat(args.date)
    else:
        base_date = datetime.date.today()
    tomorrow_date = (base_date + datetime.timedelta(days=1)).isoformat()
    return print_day_for_date(tomorrow_date)


def parse_day_arg(raw_day: str) -> int:
    s = str(raw_day).strip().upper()
    if s.startswith("D"):
        s = s[1:]
    try:
        day_num = int(s)
    except ValueError as exc:
        raise ValueError(f"DAY는 1~21 사이의 숫자여야 합니다: {raw_day}") from exc
    if not (1 <= day_num <= 21):
        raise ValueError(f"DAY는 1~21 범위여야 합니다: {day_num}")
    return day_num


def cmd_done(args: argparse.Namespace) -> int:
    try:
        day_num = parse_day_arg(args.day)
    except ValueError as e:
        print(f"오류: {e}", file=sys.stderr)
        return 1

    learner = args.learner.strip().lower()
    if learner not in LEARNERS:
        print(
            f"오류: LEARNER는 {', '.join(LEARNERS)} 중 하나여야 합니다: {args.learner}",
            file=sys.stderr,
        )
        return 1

    progress = load_json(PROGRESS_PATH)
    days_prog = progress.setdefault("days", {})
    day_key = str(day_num)
    if day_key not in days_prog:
        days_prog[day_key] = {
            "innollia": {"done": False, "date": None, "note": ""},
            "pai": {"done": False, "date": None, "note": ""},
        }

    today_str = datetime.date.today().isoformat()
    days_prog[day_key][learner] = {
        "done": True,
        "date": today_str,
        "note": args.note if args.note is not None else "",
    }

    save_json(PROGRESS_PATH, progress)
    print(f"D{day_num} {learner} 완료 기록")
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    plan = load_json(PLAN_PATH)
    progress = load_json(PROGRESS_PATH)
    days = plan.get("days", [])
    days_prog = progress.get("days", {})

    total_days = len(days)
    inno_count = 0
    pai_count = 0
    both_count = 0

    print("# 21일 학습 진도표")
    print(f"{'일차':<5} | {'날짜':<10} | {'innollia':<8} | {'pai':<8} | 주제")
    print("-" * 78)

    for d in days:
        day_num = d["day"]
        day_key = str(day_num)
        p = days_prog.get(day_key, {})
        inno_done = bool(p.get("innollia", {}).get("done"))
        pai_done = bool(p.get("pai", {}).get("done"))

        if inno_done:
            inno_count += 1
        if pai_done:
            pai_count += 1
        if inno_done and pai_done:
            both_count += 1

        inno_mark = "✔ 완료" if inno_done else "· 미완료"
        pai_mark = "✔ 완료" if pai_done else "· 미완료"
        print(
            f"D{day_num:<4} | {d['date']:<10} | {inno_mark:<6} | {pai_mark:<6} | {d['theme']}"
        )

    print("-" * 78)
    inno_pct = (inno_count / total_days * 100) if total_days else 0.0
    pai_pct = (pai_count / total_days * 100) if total_days else 0.0
    total_checks = total_days * 2
    done_checks = inno_count + pai_count
    total_pct = (done_checks / total_checks * 100) if total_checks else 0.0

    print(
        f"진행률: innollia {inno_count}/{total_days} ({inno_pct:.1f}%) | "
        f"pai {pai_count}/{total_days} ({pai_pct:.1f}%) | "
        f"공동 완료 {both_count}/{total_days}일 | "
        f"전체 {done_checks}/{total_checks} ({total_pct:.1f}%)"
    )
    return 0


def parse_bool_str(val: str) -> bool:
    v = str(val).strip().lower()
    if v in ("true", "1", "yes", "y"):
        return True
    if v in ("false", "0", "no", "n"):
        return False
    raise ValueError(f"--value는 true 또는 false여야 합니다: {val}")


def cmd_second_pass(args: argparse.Namespace) -> int:
    sp = load_json(SECOND_PASS_PATH)
    areas = sp.get("areas", [])

    if args.set_args:
        raw_area, raw_learner, raw_crit = args.set_args
        try:
            area_id = int(raw_area)
        except ValueError:
            print(f"오류: AREA는 1~5 숫자여야 합니다: {raw_area}", file=sys.stderr)
            return 1

        learner = raw_learner.strip().lower()
        if learner not in LEARNERS:
            print(
                f"오류: LEARNER는 {', '.join(LEARNERS)} 중 하나여야 합니다: {raw_learner}",
                file=sys.stderr,
            )
            return 1

        crit_id = raw_crit.strip().lower()
        if crit_id not in CRITERIA_IDS:
            print(
                f"오류: CRITERIA는 {', '.join(CRITERIA_IDS)} 중 하나여야 합니다: {raw_crit}",
                file=sys.stderr,
            )
            return 1

        try:
            bool_val = parse_bool_str(args.value)
        except ValueError as e:
            print(f"오류: {e}", file=sys.stderr)
            return 1

        target_area = next((a for a in areas if a.get("id") == area_id), None)
        if not target_area:
            print(f"오류: 영역 ID를 찾을 수 없습니다 (1~5): {area_id}", file=sys.stderr)
            return 1

        target_area.setdefault("status", {}).setdefault(learner, {})[crit_id] = bool_val
        save_json(SECOND_PASS_PATH, sp)
        state_word = "체크(true)" if bool_val else "해제(false)"
        print(f"[2회독 갱신] {area_id}영역({target_area['name']}) - {learner} - {crit_id}: {state_word}\n")

    print("# 2회독 5영역 현황 (기준: 강의[lecture] / 과제[assignment] / 적용[apply] / 피드백[feedback])")
    print("-" * 86)
    for area in areas:
        aid = area["id"]
        name = area["name"]
        sources = area.get("sources", "")
        print(f"[{aid}영역] {name}")
        print(f"  자료/과제: {sources}")
        status = area.get("status", {})
        for learner in LEARNERS:
            l_stat = status.get(learner, {})
            checks = []
            all_passed = True
            for cid in CRITERIA_IDS:
                ok = bool(l_stat.get(cid, False))
                if not ok:
                    all_passed = False
                mark = "✔" if ok else "·"
                checks.append(f"{cid}:{mark}")
            pass_str = " => [통과]" if all_passed else ""
            print(f"  - {learner:<8}: {'  '.join(checks)}{pass_str}")
        print("-" * 86)

    return 0


def cmd_export(args: argparse.Namespace) -> int:
    target_date = args.date or datetime.date.today().isoformat()
    fmt = (args.format or "md").strip().lower()

    plan = load_json(PLAN_PATH)
    progress = load_json(PROGRESS_PATH)
    days = plan.get("days", [])

    day_obj = next((d for d in days if d["date"] == target_date), None)
    if not day_obj:
        print(
            f"오류: {target_date}에 해당하는 계획이 없습니다. "
            f"(가능한 날짜: {days[0]['date']} ~ {days[-1]['date']})",
            file=sys.stderr,
        )
        return 1

    day_prog = progress.get("days", {}).get(str(day_obj["day"]), {})
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if fmt == "md":
        content = build_day_markdown_under_limit(day_obj, day_prog, limit=2000)
        out_path = OUT_DIR / f"{target_date}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(content)
        print(f"\n[저장 완료] {out_path} ({len(content)}자)")
        return 0

    if fmt == "json":
        merged = dict(day_obj)
        merged["progress"] = day_prog
        out_path = OUT_DIR / f"{target_date}.json"
        save_json(out_path, merged)
        print(json.dumps(merged, ensure_ascii=False, indent=2))
        print(f"\n[저장 완료] {out_path}")
        return 0

    print(f"오류: 지원하지 않는 형식입니다: {fmt}", file=sys.stderr)
    return 1


def check_single_url(url: str, timeout: int = 15) -> tuple[int | None, str, str]:
    """(status_code, final_url, error_message) 반환. HEAD 실패 시 GET 재시도."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.getcode()
                final_url = resp.geturl()
                return code, final_url, ""
        except urllib.error.HTTPError as e:
            if method == "HEAD":
                continue
            return e.code, e.geturl() or url, f"HTTPError {e.code}"
        except Exception as e:
            if method == "HEAD":
                continue
            return None, url, str(e)

    return None, url, "Unknown error"


def cmd_check_links(_args: argparse.Namespace) -> int:
    plan = load_json(PLAN_PATH)
    days = plan.get("days", [])

    # URL별로 등장 일차, 제목, login_required 수집
    url_entries: dict[str, dict] = {}
    for d in days:
        day_label = f"D{d['day']}"
        for mat in d.get("materials", []):
            url = mat["url"]
            if url not in url_entries:
                url_entries[url] = {
                    "title": mat["title"],
                    "url": url,
                    "login_required": bool(mat.get("login_required", False)),
                    "days": [day_label],
                }
            else:
                if day_label not in url_entries[url]["days"]:
                    url_entries[url]["days"].append(day_label)
                if mat.get("login_required"):
                    url_entries[url]["login_required"] = True

    results = []
    print(f"총 {len(url_entries)}개 고유 URL 점검 시작 (타임아웃 15초)...")
    for idx, (url, info) in enumerate(url_entries.items(), start=1):
        code, final_url, err = check_single_url(url, timeout=15)
        login_req = info["login_required"]

        if login_req:
            if code in (200, 301, 302, 303, 307, 308, 401, 403) or code is not None:
                status_note = "로그인 필요(예상됨)"
            else:
                status_note = f"로그인 필요(예상됨) / 연결 확인 필요 ({err})"
        else:
            if code and 200 <= code < 400:
                status_note = "정상"
            elif code:
                status_note = f"확인 필요 ({err})"
            else:
                status_note = f"실패 ({err})"

        code_str = str(code) if code is not None else "ERR"
        days_str = ", ".join(info["days"])
        print(f"[{idx}/{len(url_entries)}] {code_str:<4} | {status_note:<16} | {info['title']} ({url})")

        results.append(
            {
                "days": days_str,
                "title": info["title"],
                "url": url,
                "login_required": login_req,
                "code": code_str,
                "status_note": status_note,
                "redirected": final_url != url,
                "final_url": final_url,
            }
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = OUT_DIR / "link-report.md"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_lines = [
        "# 학습 자료 링크 점검 결과",
        "",
        f"- 점검 시각: `{now_str}`",
        f"- 고유 URL 수: {len(results)}개",
        "",
        "| 일차 | 제목 | URL | 로그인 필요 | 상태 코드 | 판정 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in results:
        login_col = "예" if r["login_required"] else "아니오"
        md_lines.append(
            f"| {r['days']} | {r['title']} | {r['url']} | {login_col} | {r['code']} | {r['status_note']} |"
        )

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    print(f"\n[리포트 저장 완료] {report_path}")
    return 0


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>게임기획 독학 관리 보드 — 핸섬가이즈</title>
  <style>
    :root {
      --bg: #0f141c;
      --surface: #18202c;
      --surface-alt: #1f2937;
      --border: #2e3b4e;
      --text: #e5e7eb;
      --text-muted: #9ca3af;
      --accent: #60a5fa;
      --accent-soft: rgba(96, 165, 250, 0.15);
      --ok: #34d399;
      --ok-soft: rgba(52, 211, 153, 0.15);
      --warn: #fbbf24;
      --warn-soft: rgba(251, 191, 36, 0.15);
      --analysis: #c084fc;
      --analysis-soft: rgba(192, 132, 252, 0.15);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 0;
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Malgun Gothic", "맑은 고딕", "Segoe UI", Roboto, sans-serif;
      line-height: 1.6;
    }
    a {
      color: var(--accent);
      text-decoration: none;
      word-break: break-all;
    }
    a:hover { text-decoration: underline; }
    .container {
      max-width: 1020px;
      margin: 0 auto;
      padding: 16px;
    }
    .readonly-banner {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-left: 4px solid var(--warn);
      padding: 10px 14px;
      border-radius: 6px;
      font-size: 0.9rem;
      color: var(--text);
      margin-bottom: 16px;
    }
    header {
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border);
    }
    header h1 {
      margin: 0 0 6px 0;
      font-size: 1.5rem;
    }
    .subtitle {
      color: var(--text-muted);
      font-size: 0.92rem;
      margin: 0;
    }
    .summary-bar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-top: 14px;
    }
    .stat-box {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
    }
    .stat-label {
      font-size: 0.82rem;
      color: var(--text-muted);
    }
    .stat-value {
      font-size: 1.15rem;
      font-weight: 700;
      margin-top: 4px;
    }
    .progress-track {
      height: 6px;
      background: var(--border);
      border-radius: 3px;
      margin-top: 8px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: var(--ok);
    }
    section {
      margin-bottom: 28px;
    }
    .section-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
    }
    .section-header h2 {
      margin: 0;
      font-size: 1.25rem;
    }
    .range-notice {
      background: var(--warn-soft);
      border: 1px solid var(--warn);
      color: var(--warn);
      padding: 10px 14px;
      border-radius: 6px;
      margin-bottom: 12px;
      font-size: 0.92rem;
    }
    .today-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
      gap: 16px;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
    }
    .card.highlight {
      border-color: var(--accent);
    }
    .card-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 8px;
    }
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 600;
      background: var(--surface-alt);
      border: 1px solid var(--border);
    }
    .badge.accent {
      background: var(--accent-soft);
      color: var(--accent);
      border-color: var(--accent);
    }
    .badge.ok {
      background: var(--ok-soft);
      color: var(--ok);
      border-color: var(--ok);
    }
    .badge.analysis {
      background: var(--analysis-soft);
      color: var(--analysis);
      border-color: var(--analysis);
    }
    .badge.login {
      background: var(--warn-soft);
      color: var(--warn);
      border-color: var(--warn);
    }
    .card-title {
      font-size: 1.08rem;
      font-weight: 700;
      margin: 6px 0;
    }
    .meta-line {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 10px;
    }
    .sub-title {
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--accent);
      margin: 12px 0 6px 0;
    }
    ul.compact {
      margin: 0;
      padding-left: 18px;
      font-size: 0.92rem;
    }
    ul.compact li {
      margin-bottom: 6px;
    }
    .mat-note {
      color: var(--text-muted);
      font-size: 0.84rem;
      margin-top: 2px;
    }
    .btn-group {
      display: flex;
      gap: 8px;
    }
    button.btn {
      background: var(--surface-alt);
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 5px 10px;
      font-size: 0.84rem;
      cursor: pointer;
    }
    button.btn:hover {
      border-color: var(--accent);
    }
    details.day-item {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      margin-bottom: 8px;
      overflow: hidden;
    }
    details.day-item[open] {
      border-color: var(--accent);
    }
    details.day-item summary {
      padding: 12px 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      list-style: none;
    }
    details.day-item summary::-webkit-details-marker {
      display: none;
    }
    .day-sum-left {
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
    }
    .day-sum-right {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 0.84rem;
    }
    .day-body {
      padding: 12px 16px 16px 16px;
      border-top: 1px solid var(--border);
      background: var(--surface-alt);
    }
    .table-wrap {
      overflow-x: auto;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }
    th, td {
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
    }
    th {
      background: var(--surface-alt);
      color: var(--text-muted);
      font-weight: 600;
      white-space: nowrap;
    }
    tr:last-child td {
      border-bottom: none;
    }
    @media (max-width: 640px) {
      .container { padding: 12px; }
      header h1 { font-size: 1.28rem; }
      .today-grid { grid-template-columns: 1fr; }
      details.day-item summary {
        flex-direction: column;
        align-items: flex-start;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="readonly-banner">
      ℹ️ <strong>읽기 전용 페이지</strong>입니다. 진도 변경은 CLI(<code>python tools/study.py done DAY LEARNER</code>)로 기록한 뒤 <code>python tools/study.py build</code>를 다시 실행하면 반영됩니다.
    </div>

    <header>
      <h1>🎮 게임기획 독학 관리 보드 (핸섬가이즈)</h1>
      <p class="subtitle">학습자: <strong>innollia</strong> (백지 분석) &amp; <strong>pai</strong> (학습지) | 하루 60~90분 (최소판 30분)</p>
      <div class="summary-bar" id="summary-bar"></div>
    </header>

    <section id="today-section">
      <div class="section-header">
        <h2>📌 오늘 / 내일 할 일</h2>
        <span class="subtitle" id="current-date-label"></span>
      </div>
      <div id="range-notice-box"></div>
      <div class="today-grid" id="today-cards"></div>
    </section>

    <section id="plan-section">
      <div class="section-header">
        <h2>📅 21일 전체 계획 및 진도</h2>
        <div class="btn-group">
          <button class="btn" type="button" id="btn-expand-all">모두 펼치기</button>
          <button class="btn" type="button" id="btn-collapse-all">모두 접기</button>
        </div>
      </div>
      <div id="days-list"></div>
    </section>

    <section id="second-pass-section">
      <div class="section-header">
        <h2>🧭 2회독 5영역 통과 현황</h2>
      </div>
      <div class="table-wrap">
        <table id="second-pass-table">
          <thead>
            <tr>
              <th>영역</th>
              <th>자료 및 공식 과제</th>
              <th>innollia (강의/과제/적용/피드백)</th>
              <th>pai (강의/과제/적용/피드백)</th>
            </tr>
          </thead>
          <tbody id="second-pass-tbody"></tbody>
        </table>
      </div>
    </section>
  </div>

  <script>
    const STUDY_DATA = __EMBEDDED_DATA__;

    function escapeHtml(str) {
      if (str === null || str === undefined) return "";
      return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    function getLocalDateStr(dateObj) {
      const y = dateObj.getFullYear();
      const m = String(dateObj.getMonth() + 1).padStart(2, "0");
      const d = String(dateObj.getDate()).padStart(2, "0");
      return `${y}-${m}-${d}`;
    }

    function getDayProgress(dayNum) {
      const daysProg = (STUDY_DATA.progress && STUDY_DATA.progress.days) || {};
      return daysProg[String(dayNum)] || {
        innollia: { done: false, date: null, note: "" },
        pai: { done: false, date: null, note: "" }
      };
    }

    function renderLearnerBadge(name, progObj) {
      const isDone = Boolean(progObj && progObj.done);
      const cls = isDone ? "badge ok" : "badge";
      const mark = isDone ? "✔ 완료" : "· 미완료";
      return `<span class="${cls}">${escapeHtml(name)}: ${mark}</span>`;
    }

    function renderCardHtml(label, dayObj, highlight) {
      if (!dayObj) {
        return `<div class="card"><div class="card-title">${escapeHtml(label)}</div><p class="subtitle">해당 날짜의 일정이 없습니다.</p></div>`;
      }
      const prog = getDayProgress(dayObj.day);
      const analysisBadge = dayObj.analysis_session
        ? `<span class="badge analysis">분석 회차</span>`
        : "";

      const matsHtml = (dayObj.materials || []).map(m => {
        const loginBadge = m.login_required ? ` <span class="badge login">로그인 필요</span>` : "";
        const noteHtml = m.note ? `<div class="mat-note">${escapeHtml(m.note)}</div>` : "";
        return `<li><a href="${escapeHtml(m.url)}" target="_blank" rel="noopener noreferrer"><strong>${escapeHtml(m.title)}</strong></a>${loginBadge}${noteHtml}</li>`;
      }).join("");

      const tasks = dayObj.tasks || {};
      const innoNote = prog.innollia && prog.innollia.note ? ` <em>(메모: ${escapeHtml(prog.innollia.note)})</em>` : "";
      const paiNote = prog.pai && prog.pai.note ? ` <em>(메모: ${escapeHtml(prog.pai.note)})</em>` : "";

      return `
        <div class="card ${highlight ? "highlight" : ""}">
          <div class="card-head">
            <div>
              <span class="badge accent">${escapeHtml(label)}</span>
              <span class="badge">D${dayObj.day} · ${dayObj.week}주차</span>
              ${analysisBadge}
            </div>
            <div>
              ${renderLearnerBadge("innollia", prog.innollia)}
              ${renderLearnerBadge("pai", prog.pai)}
            </div>
          </div>
          <div class="card-title">${escapeHtml(dayObj.theme)}</div>
          <div class="meta-line">📅 ${escapeHtml(dayObj.date)} | ⏱️ 예상 ${dayObj.minutes}분 (최소판 ${dayObj.min_version_minutes}분)</div>
          <div class="sub-title">📚 학습 자료</div>
          <ul class="compact">${matsHtml}</ul>
          <div class="sub-title">✅ 할 일</div>
          <ul class="compact">
            <li><strong>공통</strong>: ${escapeHtml(tasks.common || "")}</li>
            <li><strong>innollia</strong>: ${escapeHtml(tasks.innollia || "")}${innoNote}</li>
            <li><strong>pai</strong>: ${escapeHtml(tasks.pai || "")}${paiNote}</li>
          </ul>
        </div>
      `;
    }

    function initBoard() {
      const days = (STUDY_DATA.plan && STUDY_DATA.plan.days) || [];
      if (!days.length) return;

      // 1. Summary Bar
      let innoDone = 0;
      let paiDone = 0;
      let bothDone = 0;
      days.forEach(d => {
        const p = getDayProgress(d.day);
        const iOk = Boolean(p.innollia && p.innollia.done);
        const pOk = Boolean(p.pai && p.pai.done);
        if (iOk) innoDone++;
        if (pOk) paiDone++;
        if (iOk && pOk) bothDone++;
      });
      const total = days.length;
      const innoPct = ((innoDone / total) * 100).toFixed(1);
      const paiPct = ((paiDone / total) * 100).toFixed(1);
      const bothPct = ((bothDone / total) * 100).toFixed(1);

      document.getElementById("summary-bar").innerHTML = `
        <div class="stat-box">
          <div class="stat-label">innollia 진도</div>
          <div class="stat-value">${innoDone} / ${total}일 (${innoPct}%)</div>
          <div class="progress-track"><div class="progress-fill" style="width:${innoPct}%"></div></div>
        </div>
        <div class="stat-box">
          <div class="stat-label">pai 진도</div>
          <div class="stat-value">${paiDone} / ${total}일 (${paiPct}%)</div>
          <div class="progress-track"><div class="progress-fill" style="width:${paiPct}%"></div></div>
        </div>
        <div class="stat-box">
          <div class="stat-label">공동 완료 일수</div>
          <div class="stat-value">${bothDone} / ${total}일 (${bothPct}%)</div>
          <div class="progress-track"><div class="progress-fill" style="width:${bothPct}%"></div></div>
        </div>
      `;

      // 2. Today / Tomorrow Section
      const now = new Date();
      const todayStr = getLocalDateStr(now);
      const tomorrowObj = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
      const tomorrowStr = getLocalDateStr(tomorrowObj);

      document.getElementById("current-date-label").textContent = `기준일: ${todayStr}`;

      const firstDay = days[0];
      const lastDay = days[days.length - 1];
      const noticeBox = document.getElementById("range-notice-box");
      const todayCards = document.getElementById("today-cards");

      const exactToday = days.find(d => d.date === todayStr);
      const exactTomorrow = days.find(d => d.date === tomorrowStr);

      if (todayStr < firstDay.date) {
        noticeBox.innerHTML = `<div class="range-notice">📢 오늘(${escapeHtml(todayStr)})은 <strong>계획 시작 전</strong>입니다 (시작일: ${escapeHtml(firstDay.date)}). 아래에 <strong>첫날(D1)</strong>과 <strong>둘째 날(D2)</strong> 할 일을 미리 안내합니다.</div>`;
        todayCards.innerHTML =
          renderCardHtml(exactTomorrow ? "내일 (첫날 D1)" : "첫날 (D1 안내)", days[0], true) +
          renderCardHtml("둘째 날 (D2 안내)", days[1], false);
      } else if (todayStr > lastDay.date) {
        noticeBox.innerHTML = `<div class="range-notice">📢 오늘(${escapeHtml(todayStr)})은 1회독 21일 <strong>계획 종료 후</strong>입니다 (종료일: ${escapeHtml(lastDay.date)}). 아래에 <strong>마지막 날(D21)</strong> 할 일과 2회독 전환 안내를 표시합니다.</div>`;
        todayCards.innerHTML =
          renderCardHtml("마지막 날 (D21 기준)", lastDay, true) +
          renderCardHtml("직전 날 (D20 기준)", days[days.length - 2], false);
      } else {
        noticeBox.innerHTML = "";
        todayCards.innerHTML =
          renderCardHtml("오늘 할 일", exactToday, true) +
          renderCardHtml("내일 할 일", exactTomorrow, false);
      }

      // 3. 21 Days List
      const listHtml = days.map(d => {
        const prog = getDayProgress(d.day);
        const isToday = d.date === todayStr;
        const analysisBadge = d.analysis_session ? `<span class="badge analysis">분석 회차</span>` : "";
        const matsHtml = (d.materials || []).map(m => {
          const loginBadge = m.login_required ? ` <span class="badge login">로그인 필요</span>` : "";
          const noteHtml = m.note ? `<div class="mat-note">${escapeHtml(m.note)}</div>` : "";
          return `<li><a href="${escapeHtml(m.url)}" target="_blank" rel="noopener noreferrer"><strong>${escapeHtml(m.title)}</strong></a>${loginBadge}${noteHtml}</li>`;
        }).join("");
        const tasks = d.tasks || {};
        const innoDate = prog.innollia && prog.innollia.date ? ` (${escapeHtml(prog.innollia.date)})` : "";
        const paiDate = prog.pai && prog.pai.date ? ` (${escapeHtml(prog.pai.date)})` : "";
        const innoNote = prog.innollia && prog.innollia.note ? ` — 메모: ${escapeHtml(prog.innollia.note)}` : "";
        const paiNote = prog.pai && prog.pai.note ? ` — 메모: ${escapeHtml(prog.pai.note)}` : "";

        return `
          <details class="day-item" ${isToday ? "open" : ""}>
            <summary>
              <div class="day-sum-left">
                <span class="badge ${isToday ? "accent" : ""}">D${d.day}</span>
                <span>${escapeHtml(d.date)} (${d.week}주차)</span>
                <strong>${escapeHtml(d.theme)}</strong>
                ${analysisBadge}
              </div>
              <div class="day-sum-right">
                <span>⏱️ ${d.minutes}분(최소 ${d.min_version_minutes}분)</span>
                ${renderLearnerBadge("innollia", prog.innollia)}
                ${renderLearnerBadge("pai", prog.pai)}
              </div>
            </summary>
            <div class="day-body">
              <div class="sub-title">📚 학습 자료</div>
              <ul class="compact">${matsHtml}</ul>
              <div class="sub-title">✅ 할 일</div>
              <ul class="compact">
                <li><strong>공통</strong>: ${escapeHtml(tasks.common || "")}</li>
                <li><strong>innollia</strong>: ${escapeHtml(tasks.innollia || "")}${innoDate}${innoNote}</li>
                <li><strong>pai</strong>: ${escapeHtml(tasks.pai || "")}${paiDate}${paiNote}</li>
              </ul>
            </div>
          </details>
        `;
      }).join("");
      document.getElementById("days-list").innerHTML = listHtml;

      document.getElementById("btn-expand-all").addEventListener("click", () => {
        document.querySelectorAll("details.day-item").forEach(el => { el.open = true; });
      });
      document.getElementById("btn-collapse-all").addEventListener("click", () => {
        document.querySelectorAll("details.day-item").forEach(el => { el.open = false; });
      });

      // 4. Second-pass Table
      const areas = (STUDY_DATA.secondPass && STUDY_DATA.secondPass.areas) || [];
      const critLabels = [
        { id: "lecture", label: "강의" },
        { id: "assignment", label: "과제" },
        { id: "apply", label: "적용" },
        { id: "feedback", label: "피드백" }
      ];

      function formatCriteriaCell(statusObj) {
        const st = statusObj || {};
        let allOk = true;
        const items = critLabels.map(c => {
          const ok = Boolean(st[c.id]);
          if (!ok) allOk = false;
          return `<span class="badge ${ok ? "ok" : ""}">${c.label}: ${ok ? "✔" : "·"}</span>`;
        }).join(" ");
        const passBadge = allOk ? ` <span class="badge ok">🎉 통과</span>` : "";
        return `${items}${passBadge}`;
      }

      document.getElementById("second-pass-tbody").innerHTML = areas.map(area => {
        const st = area.status || {};
        return `
          <tr>
            <td><strong>${area.id}영역. ${escapeHtml(area.name)}</strong></td>
            <td>${escapeHtml(area.sources || "")}</td>
            <td>${formatCriteriaCell(st.innollia)}</td>
            <td>${formatCriteriaCell(st.pai)}</td>
          </tr>
        `;
      }).join("");
    }

    initBoard();
  </script>
</body>
</html>
"""


def cmd_build(_args: argparse.Namespace) -> int:
    plan = load_json(PLAN_PATH)
    progress = load_json(PROGRESS_PATH)
    second_pass = load_json(SECOND_PASS_PATH)

    embedded = {
        "plan": plan,
        "progress": progress,
        "secondPass": second_pass,
        "generatedAt": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    embedded_json = json.dumps(embedded, ensure_ascii=False).replace("</", "<\\/")
    html_content = HTML_TEMPLATE.replace("__EMBEDDED_DATA__", embedded_json)

    SITE_DIR.mkdir(parents=True, exist_ok=True)
    index_path = SITE_DIR / "index.html"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"정적 페이지 생성 완료: {index_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="study.py",
        description="게임기획 독학 관리 CLI (innollia & pai)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # today
    p_today = subparsers.add_parser("today", help="오늘(또는 특정 날짜) 할 일 출력")
    p_today.add_argument("--date", help="기준 날짜 (YYYY-MM-DD, 기본: 오늘)")
    p_today.set_defaults(func=cmd_today)

    # tomorrow
    p_tomorrow = subparsers.add_parser("tomorrow", help="내일 할 일 출력")
    p_tomorrow.add_argument("--date", help="기준 날짜 (YYYY-MM-DD, 기본: 오늘 기준 내일)")
    p_tomorrow.set_defaults(func=cmd_tomorrow)

    # done
    p_done = subparsers.add_parser("done", help="일일 진도 완료 기록")
    p_done.add_argument("day", metavar="DAY", help="일차 번호 (1~21)")
    p_done.add_argument("learner", metavar="LEARNER", help="학습자 (innollia | pai)")
    p_done.add_argument("--note", default="", help="완료 메모 (선택)")
    p_done.set_defaults(func=cmd_done)

    # status
    p_status = subparsers.add_parser("status", help="21일 전체 진도표 및 진행률 출력")
    p_status.set_defaults(func=cmd_status)

    # second-pass
    p_sp = subparsers.add_parser("second-pass", help="2회독 5영역 현황 출력 및 기준 설정")
    p_sp.add_argument(
        "--set",
        nargs=3,
        metavar=("AREA", "LEARNER", "CRITERIA"),
        dest="set_args",
        help="영역(1~5) 학습자(innollia|pai) 기준(lecture|assignment|apply|feedback)",
    )
    p_sp.add_argument(
        "--value",
        default="true",
        help="설정할 값 (true|false, 기본: true)",
    )
    p_sp.set_defaults(func=cmd_second_pass)

    # export
    p_export = subparsers.add_parser("export", help="특정 날짜 할 일을 out/ 폴더에 내보내기")
    p_export.add_argument("--date", required=True, help="내보낼 날짜 (YYYY-MM-DD)")
    p_export.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="출력 형식 (md | json)",
    )
    p_export.set_defaults(func=cmd_export)

    # check-links
    p_links = subparsers.add_parser(
        "check-links", help="plan.json의 모든 URL 상태 확인 후 out/link-report.md 저장"
    )
    p_links.set_defaults(func=cmd_check_links)

    # build
    p_build = subparsers.add_parser("build", help="site/index.html 정적 페이지 생성")
    p_build.set_defaults(func=cmd_build)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
