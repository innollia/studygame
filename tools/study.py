#!/usr/bin/env python3
"""게임기획 독학 관리 CLI v2 (Python 3 표준 라이브러리 전용)."""

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

TYPE_KO = {
    "jam": "잼",
    "review": "복기",
    "study": "공부",
    "analysis": "분석",
    "rest": "휴식",
    "buffer": "보강",
}

PHASE_KO = {
    "pre": "사전 기간: 게임잼·복기 (10/22 ~ 11/02)",
    "pass1": "1회독 본과정: D1~D21 (11/03 ~ 11/24)",
    "post": "보강 및 월간 리뷰 (11/25 ~ 11/30)",
}

STATUS_LABELS = {
    "done": "✔ 완료",
    "min": "△ 최소판",
    "skipped": "⏭ 건너뜀",
    "rest": "☕ 휴식",
    "todo": "· 대기",
}


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def get_learner_status_str(prog_entry: dict | None, day_type: str = "") -> str:
    if not prog_entry:
        st = "rest" if day_type == "rest" else "todo"
    else:
        st = prog_entry.get("status") or ("rest" if day_type == "rest" else "todo")
    label = STATUS_LABELS.get(st, st)
    actual = prog_entry.get("actual_min") if prog_entry else None
    if st in ("done", "min") and actual is not None:
        return f"{label}({actual}분)"
    return label


def format_day_markdown(
    day_obj: dict,
    day_progress: dict | None = None,
    include_material_notes: bool = True,
) -> str:
    day_id = day_obj["id"]
    date_str = day_obj["date"]
    weekday = day_obj.get("weekday", "")
    dtype = day_obj.get("type", "study")
    type_ko = TYPE_KO.get(dtype, dtype)
    week = day_obj.get("week")
    theme = day_obj.get("theme", "")
    minutes = day_obj.get("minutes", 0)
    min_ver = day_obj.get("min_version_minutes", 0)
    weekly_rev = bool(day_obj.get("weekly_review", False))
    templates = day_obj.get("templates", [])

    week_tag = f" · {week}주차" if week else ""
    weekly_tag = " [주간 리뷰]" if weekly_rev else ""

    lines = [
        f"# [{day_id}] {date_str} ({weekday}) · [{type_ko}]{week_tag}{weekly_tag}",
        f"**주제**: {theme}",
        f"**예상 시간**: {minutes}분 (최소판 {min_ver}분)",
        f"**주간 리뷰**: {'예 (끝 10분 templates/weekly-review.md)' if weekly_rev else '아니오'}",
    ]

    if dtype == "analysis" or day_obj.get("lens") or day_obj.get("game"):
        lens = day_obj.get("lens", "")
        game = day_obj.get("game") or {}
        g_title = game.get("title", "")
        g_url = game.get("url", "")
        if lens:
            lines.append(f"**분석 렌즈**: {lens}")
        if g_title:
            game_str = f"{g_title} ({g_url})" if g_url else g_title
            lines.append(f"**대상 게임**: {game_str}")

    if templates:
        lines.append(f"**템플릿**: {', '.join(templates)}")
    else:
        lines.append("**템플릿**: 없음")

    if day_progress is not None:
        inno_str = get_learner_status_str(day_progress.get("innollia"), dtype)
        pai_str = get_learner_status_str(day_progress.get("pai"), dtype)
        lines.append(f"**진도**: innollia [{inno_str}] | pai [{pai_str}]")

    lines.append("")
    lines.append("## 학습 자료")
    mats = day_obj.get("materials", [])
    if not mats:
        lines.append("- (별도 외부 자료 없음)")
    else:
        for mat in mats:
            login_str = " *(로그인 필요)*" if mat.get("login_required") else ""
            line = f"- **{mat['title']}**{login_str}: {mat['url']}"
            if include_material_notes and mat.get("note"):
                line += f"\n  - {mat['note']}"
            lines.append(line)

    tasks = day_obj.get("tasks", {})
    lines.append("")
    lines.append("## 할 일")
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


def resolve_day_for_date(days: list[dict], target_date: str) -> tuple[dict, str | None]:
    """target_date에 해당하는 day_obj를 찾고, 없으면 가장 가까운 다음 날(또는 마지막 날)과 안내 문구 반환."""
    for d in days:
        if d["date"] == target_date:
            return d, None

    next_days = [d for d in days if d["date"] > target_date]
    if next_days:
        chosen = next_days[0]
        msg = (
            f"[안내] {target_date}에 해당하는 일정이 없습니다. "
            f"가장 가까운 다음 날인 [{chosen['id']}] {chosen['date']} ({chosen.get('weekday', '')}) 일정을 안내합니다."
        )
        return chosen, msg

    chosen = days[-1]
    msg = (
        f"[안내] {target_date}에 해당하는 일정이 없습니다(계획 종료일: {chosen['date']}). "
        f"마지막 날인 [{chosen['id']}] {chosen['date']} ({chosen.get('weekday', '')}) 일정을 안내합니다."
    )
    return chosen, msg


def print_day_for_date(target_date: str) -> int:
    plan = load_json(PLAN_PATH)
    progress = load_json(PROGRESS_PATH)
    days = plan.get("days", [])
    if not days:
        print("계획 데이터가 비어 있습니다.", file=sys.stderr)
        return 1

    day_obj, notice = resolve_day_for_date(days, target_date)
    if notice:
        print(notice + "\n")
    day_prog = progress.get("days", {}).get(day_obj["id"], {})
    print(format_day_markdown(day_obj, day_prog, include_material_notes=True))
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


def find_day_by_id(days: list[dict], raw_id: str) -> dict | None:
    target = str(raw_id).strip().upper()
    for d in days:
        if d["id"].upper() == target:
            return d
    return None


def cmd_done(args: argparse.Namespace) -> int:
    plan = load_json(PLAN_PATH)
    days = plan.get("days", [])
    day_obj = find_day_by_id(days, args.id)
    if not day_obj:
        valid_ids = ", ".join(d["id"] for d in days)
        print(f"오류: 유효하지 않은 ID입니다: {args.id} (가능한 ID: {valid_ids})", file=sys.stderr)
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
    day_id = day_obj["id"]
    if day_id not in days_prog:
        days_prog[day_id] = {
            "innollia": {
                "status": "todo",
                "date": None,
                "level": None,
                "planned_min": None,
                "actual_min": None,
                "note": "",
            },
            "pai": {
                "status": "todo",
                "date": None,
                "level": None,
                "planned_min": None,
                "actual_min": None,
                "note": "",
            },
        }

    is_min = bool(args.min)
    status_val = "min" if is_min else "done"
    level_val = "min" if is_min else "normal"
    rec_date = args.date or datetime.date.today().isoformat()
    planned_min = day_obj.get("minutes", 0)
    if args.minutes is not None:
        actual_min = args.minutes
    else:
        actual_min = day_obj.get("min_version_minutes", planned_min) if is_min else planned_min

    days_prog[day_id][learner] = {
        "status": status_val,
        "date": rec_date,
        "level": level_val,
        "planned_min": planned_min,
        "actual_min": actual_min,
        "note": args.note if args.note is not None else "",
    }

    save_json(PROGRESS_PATH, progress)
    mode_ko = "최소판(min)" if is_min else "정상(done)"
    print(f"[{day_id}] {learner} {mode_ko} 완료 기록 (날짜: {rec_date}, 시간: {actual_min}분)")
    return 0


def cmd_skip(args: argparse.Namespace) -> int:
    plan = load_json(PLAN_PATH)
    days = plan.get("days", [])
    day_obj = find_day_by_id(days, args.id)
    if not day_obj:
        valid_ids = ", ".join(d["id"] for d in days)
        print(f"오류: 유효하지 않은 ID입니다: {args.id} (가능한 ID: {valid_ids})", file=sys.stderr)
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
    day_id = day_obj["id"]
    if day_id not in days_prog:
        days_prog[day_id] = {
            "innollia": {
                "status": "todo",
                "date": None,
                "level": None,
                "planned_min": None,
                "actual_min": None,
                "note": "",
            },
            "pai": {
                "status": "todo",
                "date": None,
                "level": None,
                "planned_min": None,
                "actual_min": None,
                "note": "",
            },
        }

    rec_date = getattr(args, "date", None) or datetime.date.today().isoformat()
    days_prog[day_id][learner] = {
        "status": "skipped",
        "date": rec_date,
        "level": None,
        "planned_min": day_obj.get("minutes", 0),
        "actual_min": 0,
        "note": args.note if args.note is not None else "",
    }

    save_json(PROGRESS_PATH, progress)
    print(f"[{day_id}] {learner} 건너뜀(skipped) 기록 (날짜: {rec_date})")
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    plan = load_json(PLAN_PATH)
    progress = load_json(PROGRESS_PATH)
    days = plan.get("days", [])
    days_prog = progress.get("days", {})

    print("# 전체 학습 진도표 (v2)")
    print(f"{'ID':<4} | {'날짜(요일)':<14} | {'유형':<4} | {'innollia':<12} | {'pai':<12} | 주제")
    print("-" * 92)

    pass1_days = [d for d in days if d["id"].startswith("D")]
    pass1_total = len(pass1_days)

    p1_inno_done = 0
    p1_inno_min = 0
    p1_pai_done = 0
    p1_pai_min = 0
    p1_both = 0

    all_inno_done = 0
    all_pai_done = 0

    for d in days:
        did = d["id"]
        dtype = d.get("type", "study")
        type_ko = TYPE_KO.get(dtype, dtype)
        p = days_prog.get(did, {})
        inno_p = p.get("innollia", {})
        pai_p = p.get("pai", {})

        inno_st = inno_p.get("status") or ("rest" if dtype == "rest" else "todo")
        pai_st = pai_p.get("status") or ("rest" if dtype == "rest" else "todo")

        if inno_st in ("done", "min"):
            all_inno_done += 1
        if pai_st in ("done", "min"):
            all_pai_done += 1

        if did.startswith("D"):
            if inno_st in ("done", "min"):
                p1_inno_done += 1
                if inno_st == "min":
                    p1_inno_min += 1
            if pai_st in ("done", "min"):
                p1_pai_done += 1
                if pai_st == "min":
                    p1_pai_min += 1
            if inno_st in ("done", "min") and pai_st in ("done", "min"):
                p1_both += 1

        inno_mark = STATUS_LABELS.get(inno_st, inno_st)
        pai_mark = STATUS_LABELS.get(pai_st, pai_st)
        date_col = f"{d['date']}({d.get('weekday', '')})"
        print(
            f"{did:<4} | {date_col:<13} | {type_ko:<3} | {inno_mark:<10} | {pai_mark:<10} | {d.get('theme', '')}"
        )

    print("-" * 92)
    inno_p1_pct = (p1_inno_done / pass1_total * 100) if pass1_total else 0.0
    pai_p1_pct = (p1_pai_done / pass1_total * 100) if pass1_total else 0.0
    print(
        f"[1회독 pass1 (D1~D21) 진행률]\n"
        f"- innollia: {p1_inno_done}/{pass1_total} ({inno_p1_pct:.1f}%) [최소판(min): {p1_inno_min}회]\n"
        f"- pai     : {p1_pai_done}/{pass1_total} ({pai_p1_pct:.1f}%) [최소판(min): {p1_pai_min}회]\n"
        f"- 공동 완료: {p1_both}/{pass1_total}일 | 전체 완료(A0~M1 중): innollia {all_inno_done}회, pai {all_pai_done}회"
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
    if not days:
        print("계획 데이터가 비어 있습니다.", file=sys.stderr)
        return 1

    day_obj, notice = resolve_day_for_date(days, target_date)
    if notice:
        print(notice + "\n")

    day_prog = progress.get("days", {}).get(day_obj["id"], {})
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_date_str = day_obj["date"]

    if fmt == "md":
        content = build_day_markdown_under_limit(day_obj, day_prog, limit=2000)
        out_path = OUT_DIR / f"{out_date_str}.md"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(content)
        print(f"\n[저장 완료] {out_path} ({len(content)}자)")
        return 0

    if fmt == "json":
        merged = dict(day_obj)
        merged["progress"] = day_prog
        out_path = OUT_DIR / f"{out_date_str}.json"
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

    url_entries: dict[str, dict] = {}

    def register_url(url: str, title: str, day_id: str, login_req: bool) -> None:
        if not url:
            return
        if url not in url_entries:
            url_entries[url] = {
                "title": title,
                "url": url,
                "login_required": login_req,
                "days": [day_id],
            }
        else:
            if day_id not in url_entries[url]["days"]:
                url_entries[url]["days"].append(day_id)
            if login_req:
                url_entries[url]["login_required"] = True

    for d in days:
        day_id = d["id"]
        game = d.get("game") or {}
        if game.get("url"):
            register_url(game["url"], f"[게임] {game.get('title', '')}", day_id, False)
        for mat in d.get("materials", []):
            register_url(
                mat.get("url", ""),
                mat.get("title", ""),
                day_id,
                bool(mat.get("login_required", False)),
            )

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
        "# 학습 자료 및 게임 링크 점검 결과",
        "",
        f"- 점검 시각: `{now_str}`",
        f"- 고유 URL 수: {len(results)}개",
        "",
        "| ID | 제목 | URL | 로그인 필요 | 상태 코드 | 판정 |",
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
  <title>게임기획 독학 관리 보드 v2 — 핸섬가이즈</title>
  <style>
    :root {
      --bg: #0d1117;
      --surface: #161b22;
      --surface-alt: #1f2733;
      --border: #30363d;
      --text: #e6edf3;
      --text-muted: #9ca3af;
      --accent: #58a6ff;
      --ok: #3fb950;
      --ok-soft: rgba(63, 185, 80, 0.16);
      --min: #fbbf24;
      --min-soft: rgba(251, 191, 36, 0.16);
      --skip: #f87171;
      --skip-soft: rgba(248, 113, 113, 0.16);

      /* Type colors (high contrast on dark background) */
      --type-study: #60a5fa;
      --type-study-bg: rgba(96, 165, 250, 0.14);
      --type-analysis: #c084fc;
      --type-analysis-bg: rgba(192, 132, 252, 0.16);
      --type-jam: #fb923c;
      --type-jam-bg: rgba(251, 146, 60, 0.16);
      --type-review: #2dd4bf;
      --type-review-bg: rgba(45, 212, 191, 0.16);
      --type-rest: #94a3b8;
      --type-rest-bg: rgba(148, 163, 184, 0.16);
      --type-buffer: #a3e635;
      --type-buffer-bg: rgba(163, 230, 53, 0.15);
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
      max-width: 1080px;
      margin: 0 auto;
      padding: 16px;
    }
    .readonly-banner {
      background: var(--surface-alt);
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      padding: 10px 14px;
      border-radius: 6px;
      font-size: 0.9rem;
      color: var(--text);
      margin-bottom: 16px;
    }
    header {
      margin-bottom: 22px;
      padding-bottom: 14px;
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
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
      font-size: 1.1rem;
      font-weight: 700;
      margin-top: 4px;
    }
    .stat-sub {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 2px;
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
      margin-bottom: 30px;
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
    .today-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(330px, 1fr));
      gap: 16px;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-top: 4px solid var(--border);
      border-radius: 10px;
      padding: 16px;
    }
    .card.type-study { border-top-color: var(--type-study); }
    .card.type-analysis { border-top-color: var(--type-analysis); }
    .card.type-jam { border-top-color: var(--type-jam); }
    .card.type-review { border-top-color: var(--type-review); }
    .card.type-rest { border-top-color: var(--type-rest); }
    .card.type-buffer { border-top-color: var(--type-buffer); }

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
      color: var(--text);
    }
    .badge.type-study { background: var(--type-study-bg); color: var(--type-study); border-color: var(--type-study); }
    .badge.type-analysis { background: var(--type-analysis-bg); color: var(--type-analysis); border-color: var(--type-analysis); }
    .badge.type-jam { background: var(--type-jam-bg); color: var(--type-jam); border-color: var(--type-jam); }
    .badge.type-review { background: var(--type-review-bg); color: var(--type-review); border-color: var(--type-review); }
    .badge.type-rest { background: var(--type-rest-bg); color: var(--type-rest); border-color: var(--type-rest); }
    .badge.type-buffer { background: var(--type-buffer-bg); color: var(--type-buffer); border-color: var(--type-buffer); }

    .badge.st-done { background: var(--ok-soft); color: var(--ok); border-color: var(--ok); }
    .badge.st-min { background: var(--min-soft); color: var(--min); border-color: var(--min); }
    .badge.st-skipped { background: var(--skip-soft); color: var(--skip); border-color: var(--skip); }
    .badge.st-rest { background: var(--type-rest-bg); color: var(--type-rest); border-color: var(--type-rest); }
    .badge.weekly { background: var(--type-review-bg); color: var(--type-review); border-color: var(--type-review); }
    .badge.login { background: var(--min-soft); color: var(--min); border-color: var(--min); }

    .card-title {
      font-size: 1.08rem;
      font-weight: 700;
      margin: 6px 0;
    }
    .meta-line {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-bottom: 8px;
    }
    .analysis-box {
      background: var(--type-analysis-bg);
      border: 1px solid var(--type-analysis);
      border-radius: 6px;
      padding: 8px 12px;
      font-size: 0.88rem;
      margin: 8px 0;
    }
    .sub-title {
      font-size: 0.86rem;
      font-weight: 700;
      color: var(--accent);
      margin: 12px 0 6px 0;
    }
    ul.compact {
      margin: 0;
      padding-left: 18px;
      font-size: 0.91rem;
    }
    ul.compact li {
      margin-bottom: 5px;
    }
    .mat-note {
      color: var(--text-muted);
      font-size: 0.83rem;
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
    details.phase-group {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-bottom: 16px;
      overflow: hidden;
    }
    details.phase-group > summary {
      padding: 14px 16px;
      background: var(--surface-alt);
      cursor: pointer;
      font-weight: 700;
      font-size: 1.05rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      list-style: none;
    }
    details.phase-group > summary::-webkit-details-marker {
      display: none;
    }
    .phase-body {
      padding: 12px;
    }
    details.day-item {
      background: var(--surface);
      border: 1px solid var(--border);
      border-left: 4px solid var(--border);
      border-radius: 8px;
      margin-bottom: 8px;
      overflow: hidden;
    }
    details.day-item.type-study { border-left-color: var(--type-study); }
    details.day-item.type-analysis { border-left-color: var(--type-analysis); }
    details.day-item.type-jam { border-left-color: var(--type-jam); }
    details.day-item.type-review { border-left-color: var(--type-review); }
    details.day-item.type-rest { border-left-color: var(--type-rest); }
    details.day-item.type-buffer { border-left-color: var(--type-buffer); }

    details.day-item summary {
      padding: 10px 14px;
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
      flex-wrap: wrap;
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
      ℹ️ <strong>읽기 전용 페이지</strong>입니다. 진도 변경은 CLI(<code>python tools/study.py done ID LEARNER [--min] [--minutes N]</code> 또는 <code>skip ID LEARNER</code>)로 기록한 뒤 <code>python tools/study.py build</code>를 실행하면 반영됩니다.
    </div>

    <header>
      <h1>🎮 게임기획 독학 관리 보드 v2 (핸섬가이즈)</h1>
      <p class="subtitle">학습자: <strong>innollia</strong> (백지 분석) &amp; <strong>pai</strong> (학습지 + 유튜브 카드) | 2026-10-22 ~ 2026-11-30</p>
      <div class="summary-bar" id="summary-bar"></div>
    </header>

    <section id="today-section">
      <div class="section-header">
        <h2>📌 오늘 / 내일 할 일</h2>
        <span class="subtitle" id="current-date-label"></span>
      </div>
      <div class="today-grid" id="today-cards"></div>
    </section>

    <section id="plan-section">
      <div class="section-header">
        <h2>📅 전체 일정 (Phase별 묶음 · A0 ~ M1)</h2>
        <div class="btn-group">
          <button class="btn" type="button" id="btn-expand-all">모두 펼치기</button>
          <button class="btn" type="button" id="btn-collapse-all">모두 접기</button>
        </div>
      </div>
      <div id="phases-container"></div>
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

    const TYPE_KO = {
      jam: "잼",
      review: "복기",
      study: "공부",
      analysis: "분석",
      rest: "휴식",
      buffer: "보강"
    };

    const PHASE_META = [
      { key: "pre", title: "1단계 (pre): 사전 기준선 & 두 번의 게임잼·복기 (10/22 ~ 11/02)" },
      { key: "pass1", title: "2단계 (pass1): 1회독 21일 본과정 D1~D21 & 휴식 (11/03 ~ 11/24)" },
      { key: "post", title: "3단계 (post): 보강 주간 B1~B5 & 월간 리뷰 M1 (11/25 ~ 11/30)" }
    ];

    const STATUS_MAP = {
      done: { label: "✔ 완료", cls: "st-done" },
      min: { label: "△ 최소판", cls: "st-min" },
      skipped: { label: "⏭ 건너뜀", cls: "st-skipped" },
      rest: { label: "☕ 휴식", cls: "st-rest" },
      todo: { label: "· 대기", cls: "" }
    };

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

    function getDayProgress(dayId, dayType) {
      const daysProg = (STUDY_DATA.progress && STUDY_DATA.progress.days) || {};
      const defaultSt = dayType === "rest" ? "rest" : "todo";
      return daysProg[String(dayId)] || {
        innollia: { status: defaultSt, date: null, level: null, planned_min: null, actual_min: null, note: "" },
        pai: { status: defaultSt, date: null, level: null, planned_min: null, actual_min: null, note: "" }
      };
    }

    function renderLearnerBadge(name, progObj, dayType) {
      const st = (progObj && progObj.status) || (dayType === "rest" ? "rest" : "todo");
      const info = STATUS_MAP[st] || { label: st, cls: "" };
      const minText = (st === "done" || st === "min") && progObj && progObj.actual_min != null
        ? `(${progObj.actual_min}분)`
        : "";
      return `<span class="badge ${info.cls}">${escapeHtml(name)}: ${info.label}${minText}</span>`;
    }

    function resolveDayForDate(days, targetDate) {
      const exact = days.find(d => d.date === targetDate);
      if (exact) return { day: exact, fallbackNotice: null };
      const nextDays = days.filter(d => d.date > targetDate);
      if (nextDays.length > 0) {
        return {
          day: nextDays[0],
          fallbackNotice: `${targetDate} 일정이 없어 가장 가까운 다음 날(${nextDays[0].id}, ${nextDays[0].date})을 표시합니다.`
        };
      }
      const last = days[days.length - 1];
      return {
        day: last,
        fallbackNotice: `${targetDate} 일정이 없어 마지막 날(${last.id}, ${last.date})을 표시합니다.`
      };
    }

    function renderDayDetailsHtml(dayObj) {
      const dtype = dayObj.type || "study";
      const prog = getDayProgress(dayObj.id, dtype);

      let analysisHtml = "";
      if (dtype === "analysis" || dayObj.lens || dayObj.game) {
        const lensLine = dayObj.lens ? `<div><strong>🔍 렌즈</strong>: ${escapeHtml(dayObj.lens)}</div>` : "";
        const g = dayObj.game || {};
        let gameLine = "";
        if (g.title) {
          const gLink = g.url
            ? `<a href="${escapeHtml(g.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(g.title)}</a>`
            : escapeHtml(g.title);
          gameLine = `<div><strong>🎮 대상 게임</strong>: ${gLink}</div>`;
        }
        analysisHtml = `<div class="analysis-box">${lensLine}${gameLine}</div>`;
      }

      const mats = dayObj.materials || [];
      const matsHtml = mats.length
        ? mats.map(m => {
            const loginBadge = m.login_required ? ` <span class="badge login">로그인 필요</span>` : "";
            const noteHtml = m.note ? `<div class="mat-note">${escapeHtml(m.note)}</div>` : "";
            return `<li><a href="${escapeHtml(m.url)}" target="_blank" rel="noopener noreferrer"><strong>${escapeHtml(m.title)}</strong></a>${loginBadge}${noteHtml}</li>`;
          }).join("")
        : `<li><span class="mat-note">(별도 외부 자료 없음)</span></li>`;

      const tasks = dayObj.tasks || {};
      const innoNote = prog.innollia && prog.innollia.note ? ` <em>(메모: ${escapeHtml(prog.innollia.note)})</em>` : "";
      const paiNote = prog.pai && prog.pai.note ? ` <em>(메모: ${escapeHtml(prog.pai.note)})</em>` : "";
      const tmpls = (dayObj.templates || []).length ? dayObj.templates.map(escapeHtml).join(", ") : "없음";
      const weeklyStr = dayObj.weekly_review ? "예 (끝 10분 templates/weekly-review.md)" : "아니오";

      return `
        ${analysisHtml}
        <div class="meta-line">🗂️ <strong>템플릿</strong>: ${tmpls} | 🔁 <strong>주간 리뷰</strong>: ${weeklyStr}</div>
        <div class="sub-title">📚 학습 자료</div>
        <ul class="compact">${matsHtml}</ul>
        <div class="sub-title">✅ 할 일</div>
        <ul class="compact">
          <li><strong>공통</strong>: ${escapeHtml(tasks.common || "")}</li>
          <li><strong>innollia</strong>: ${escapeHtml(tasks.innollia || "")}${innoNote}</li>
          <li><strong>pai</strong>: ${escapeHtml(tasks.pai || "")}${paiNote}</li>
        </ul>
      `;
    }

    function renderCardHtml(label, resolved) {
      if (!resolved || !resolved.day) {
        return `<div class="card"><div class="card-title">${escapeHtml(label)}</div></div>`;
      }
      const d = resolved.day;
      const dtype = d.type || "study";
      const typeKo = TYPE_KO[dtype] || dtype;
      const prog = getDayProgress(d.id, dtype);
      const weekBadge = d.week ? `<span class="badge">${d.week}주차</span>` : "";
      const weeklyBadge = d.weekly_review ? `<span class="badge weekly">주간 리뷰</span>` : "";
      const fallbackHtml = resolved.fallbackNotice
        ? `<div class="mat-note" style="margin-bottom:6px;">ℹ️ ${escapeHtml(resolved.fallbackNotice)}</div>`
        : "";

      return `
        <div class="card type-${escapeHtml(dtype)}">
          <div class="card-head">
            <div>
              <span class="badge">${escapeHtml(label)}</span>
              <span class="badge type-${escapeHtml(dtype)}">[${escapeHtml(d.id)}] ${escapeHtml(typeKo)}</span>
              ${weekBadge}
              ${weeklyBadge}
            </div>
            <div>
              ${renderLearnerBadge("innollia", prog.innollia, dtype)}
              ${renderLearnerBadge("pai", prog.pai, dtype)}
            </div>
          </div>
          ${fallbackHtml}
          <div class="card-title">${escapeHtml(d.theme)}</div>
          <div class="meta-line">📅 ${escapeHtml(d.date)} (${escapeHtml(d.weekday || "")}) | ⏱️ ${d.minutes}분 (최소판 ${d.min_version_minutes}분)</div>
          ${renderDayDetailsHtml(d)}
        </div>
      `;
    }

    function initBoard() {
      const days = (STUDY_DATA.plan && STUDY_DATA.plan.days) || [];
      if (!days.length) return;

      // 1. Summary Bar (pass1 D1~D21 + overall)
      const pass1Days = days.filter(d => String(d.id).startsWith("D"));
      const p1Total = pass1Days.length;
      let p1InnoDone = 0, p1InnoMin = 0;
      let p1PaiDone = 0, p1PaiMin = 0;
      let p1Both = 0;

      pass1Days.forEach(d => {
        const p = getDayProgress(d.id, d.type);
        const iSt = p.innollia && p.innollia.status;
        const pSt = p.pai && p.pai.status;
        const iOk = iSt === "done" || iSt === "min";
        const pOk = pSt === "done" || pSt === "min";
        if (iOk) { p1InnoDone++; if (iSt === "min") p1InnoMin++; }
        if (pOk) { p1PaiDone++; if (pSt === "min") p1PaiMin++; }
        if (iOk && pOk) p1Both++;
      });

      const innoPct = p1Total ? ((p1InnoDone / p1Total) * 100).toFixed(1) : "0.0";
      const paiPct = p1Total ? ((p1PaiDone / p1Total) * 100).toFixed(1) : "0.0";
      const bothPct = p1Total ? ((p1Both / p1Total) * 100).toFixed(1) : "0.0";

      document.getElementById("summary-bar").innerHTML = `
        <div class="stat-box">
          <div class="stat-label">1회독(D1~D21) innollia</div>
          <div class="stat-value">${p1InnoDone} / ${p1Total}일 (${innoPct}%)</div>
          <div class="stat-sub">최소판(min): ${p1InnoMin}회</div>
          <div class="progress-track"><div class="progress-fill" style="width:${innoPct}%"></div></div>
        </div>
        <div class="stat-box">
          <div class="stat-label">1회독(D1~D21) pai</div>
          <div class="stat-value">${p1PaiDone} / ${p1Total}일 (${paiPct}%)</div>
          <div class="stat-sub">최소판(min): ${p1PaiMin}회</div>
          <div class="progress-track"><div class="progress-fill" style="width:${paiPct}%"></div></div>
        </div>
        <div class="stat-box">
          <div class="stat-label">1회독(D1~D21) 공동 완료</div>
          <div class="stat-value">${p1Both} / ${p1Total}일 (${bothPct}%)</div>
          <div class="stat-sub">전체 일정 수: ${days.length}일 (A0~M1)</div>
          <div class="progress-track"><div class="progress-fill" style="width:${bothPct}%"></div></div>
        </div>
      `;

      // 2. Today / Tomorrow Cards
      const now = new Date();
      const todayStr = getLocalDateStr(now);
      const tomorrowObj = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);
      const tomorrowStr = getLocalDateStr(tomorrowObj);

      document.getElementById("current-date-label").textContent = `기준일: ${todayStr}`;

      const resolvedToday = resolveDayForDate(days, todayStr);
      const resolvedTomorrow = resolveDayForDate(days, tomorrowStr);

      document.getElementById("today-cards").innerHTML =
        renderCardHtml(`오늘 (${todayStr})`, resolvedToday) +
        renderCardHtml(`내일 (${tomorrowStr})`, resolvedTomorrow);

      // 3. Schedule grouped by Phase
      const phasesHtml = PHASE_META.map(pm => {
        const phaseDays = days.filter(d => d.phase === pm.key);
        const hasToday = phaseDays.some(d => d.date === todayStr);
        const daysItemsHtml = phaseDays.map(d => {
          const dtype = d.type || "study";
          const typeKo = TYPE_KO[dtype] || dtype;
          const prog = getDayProgress(d.id, dtype);
          const isToday = d.date === todayStr;
          const weekBadge = d.week ? `<span class="badge">${d.week}주차</span>` : "";
          const weeklyBadge = d.weekly_review ? `<span class="badge weekly">주간 리뷰</span>` : "";

          return `
            <details class="day-item type-${escapeHtml(dtype)}" ${isToday ? "open" : ""}>
              <summary>
                <div class="day-sum-left">
                  <span class="badge type-${escapeHtml(dtype)}">[${escapeHtml(d.id)}] ${escapeHtml(typeKo)}</span>
                  <span>${escapeHtml(d.date)} (${escapeHtml(d.weekday || "")})</span>
                  ${weekBadge}
                  <strong>${escapeHtml(d.theme)}</strong>
                  ${weeklyBadge}
                </div>
                <div class="day-sum-right">
                  <span>⏱️ ${d.minutes}분(최소 ${d.min_version_minutes}분)</span>
                  ${renderLearnerBadge("innollia", prog.innollia, dtype)}
                  ${renderLearnerBadge("pai", prog.pai, dtype)}
                </div>
              </summary>
              <div class="day-body">
                ${renderDayDetailsHtml(d)}
              </div>
            </details>
          `;
        }).join("");

        return `
          <details class="phase-group" open>
            <summary>
              <span>${escapeHtml(pm.title)}</span>
              <span class="badge">${phaseDays.length}일</span>
            </summary>
            <div class="phase-body">
              ${daysItemsHtml}
            </div>
          </details>
        `;
      }).join("");

      document.getElementById("phases-container").innerHTML = phasesHtml;

      document.getElementById("btn-expand-all").addEventListener("click", () => {
        document.querySelectorAll("details.phase-group, details.day-item").forEach(el => { el.open = true; });
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
          return `<span class="badge ${ok ? "st-done" : ""}">${c.label}: ${ok ? "✔" : "·"}</span>`;
        }).join(" ");
        const passBadge = allOk ? ` <span class="badge st-done">🎉 통과</span>` : "";
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
        description="게임기획 독학 관리 CLI v2 (innollia & pai)",
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
    p_done = subparsers.add_parser("done", help="일일 진도 완료 기록 (정상 또는 최소판)")
    p_done.add_argument("id", metavar="ID", help="일정 ID (예: A0, J1, D1, R1, M1)")
    p_done.add_argument("learner", metavar="LEARNER", help="학습자 (innollia | pai)")
    p_done.add_argument("--min", action="store_true", help="최소판(30분)으로 완료한 경우 지정")
    p_done.add_argument("--minutes", type=int, default=None, help="실제 소요 시간(분)")
    p_done.add_argument("--note", default="", help="완료 메모 (선택)")
    p_done.add_argument("--date", default=None, help="완료 날짜 (YYYY-MM-DD, 기본: 오늘)")
    p_done.set_defaults(func=cmd_done)

    # skip
    p_skip = subparsers.add_parser("skip", help="일정 건너뜀(skipped) 기록")
    p_skip.add_argument("id", metavar="ID", help="일정 ID (예: J1, D1)")
    p_skip.add_argument("learner", metavar="LEARNER", help="학습자 (innollia | pai)")
    p_skip.add_argument("--note", default="", help="사유 또는 메모 (선택)")
    p_skip.add_argument("--date", default=None, help="기록 날짜 (YYYY-MM-DD, 기본: 오늘)")
    p_skip.set_defaults(func=cmd_skip)

    # status
    p_status = subparsers.add_parser("status", help="전체 진도표 및 1회독(D1~D21) 진행률 출력")
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
        "check-links", help="plan.json의 모든 자료 및 게임 URL 상태 확인 후 out/link-report.md 저장"
    )
    p_links.set_defaults(func=cmd_check_links)

    # build
    p_build = subparsers.add_parser("build", help="site/index.html 정적 페이지 재생성")
    p_build.set_defaults(func=cmd_build)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
