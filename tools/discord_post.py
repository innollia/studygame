#!/usr/bin/env python3
"""다음 날 할 일(study.py export 결과)을 Discord 포럼 스레드에 게시하는 스크립트."""

import argparse
import datetime
import json
import subprocess
import sys
import time
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
STUDY_SCRIPT = ROOT_DIR / "tools" / "study.py"

CONFIG_PATH = DATA_DIR / "discord.local.json"
LOG_PATH = DATA_DIR / "discord-post.log"
TOKEN_ENV_PATH = Path.home() / ".all-tomorrow" / "key-pool.env"

API_BASE = "https://discord.com/api/v10"
USER_AGENT = "DiscordBot (studygame, 1)"
MAX_CHUNK_LEN = 1900
KST = datetime.timezone(datetime.timedelta(hours=9))

DEFAULT_CONFIG = {
    "forum_channel_id": "1562273221749907516",
    "thread_id": None,
    "thread_title": "📅 매일 할 일",
    "posted": {},
}


class DiscordHTTPError(Exception):
    """Discord HTTP 오류 (토큰 등 민감정보 제외)."""

    def __init__(self, status_code: int, body_snippet: str) -> None:
        super().__init__(f"HTTP {status_code}")
        self.status_code = status_code
        self.body_snippet = body_snippet


def get_tomorrow_kst() -> str:
    now_kst = datetime.datetime.now(KST).date()
    return (now_kst + datetime.timedelta(days=1)).isoformat()


def load_or_init_config(dry_run: bool) -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        cfg = dict(DEFAULT_CONFIG)
        cfg.update(loaded)
        if not isinstance(cfg.get("posted"), dict):
            cfg["posted"] = {}
        return cfg

    cfg = {
        "forum_channel_id": DEFAULT_CONFIG["forum_channel_id"],
        "thread_id": DEFAULT_CONFIG["thread_id"],
        "thread_title": DEFAULT_CONFIG["thread_title"],
        "posted": {},
    }
    if not dry_run:
        save_config(cfg)
    return cfg


def save_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")


def append_log(line: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line.rstrip("\n") + "\n")


def load_bot_token() -> str:
    if not TOKEN_ENV_PATH.exists():
        raise RuntimeError(f"토큰 파일을 찾을 수 없습니다: {TOKEN_ENV_PATH}")

    with open(TOKEN_ENV_PATH, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            if "=" not in line:
                continue
            key, val = line.split("=", 1)
            if key.strip() == "EVE_DISCORD_BOT_TOKEN":
                token = val.strip().strip("'").strip('"').strip()
                if not token:
                    raise RuntimeError("EVE_DISCORD_BOT_TOKEN 값이 비어 있습니다.")
                return token

    raise RuntimeError("토큰 파일에서 EVE_DISCORD_BOT_TOKEN 항목을 찾을 수 없습니다.")


def build_post_body(target_date: str) -> str:
    cmd = [
        sys.executable,
        str(STUDY_SCRIPT),
        "export",
        "--date",
        target_date,
        "--format",
        "md",
    ]
    proc = subprocess.run(
        cmd,
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        err_msg = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"study.py export 실행 실패 (코드 {proc.returncode}): {err_msg}")

    md_path = OUT_DIR / f"{target_date}.md"
    if not md_path.exists():
        raise RuntimeError(f"내보낸 마크다운 파일을 찾을 수 없습니다: {md_path}")

    content = md_path.read_text(encoding="utf-8").rstrip("\n")
    return f"📅 **내일 할 일 — {target_date}**\n{content}"


def split_into_chunks(text: str, max_len: int = MAX_CHUNK_LEN) -> list[str]:
    lines = text.split("\n")
    chunks: list[str] = []
    current_lines: list[str] = []
    current_len = 0

    for line in lines:
        while len(line) > max_len:
            if current_lines:
                chunks.append("\n".join(current_lines))
                current_lines = []
                current_len = 0
            chunks.append(line[:max_len])
            line = line[max_len:]

        add_len = len(line) if not current_lines else len(line) + 1
        if current_lines and (current_len + add_len > max_len):
            chunks.append("\n".join(current_lines))
            current_lines = [line]
            current_len = len(line)
        else:
            current_lines.append(line)
            current_len += add_len

    if current_lines:
        chunks.append("\n".join(current_lines))

    return chunks


def discord_post_json(endpoint: str, payload: dict, token: str) -> dict:
    url = f"{API_BASE}{endpoint}"
    data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
    }

    for attempt in range(2):
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                err_body = ""

            if e.code == 429 and attempt == 0:
                retry_after = 1.0
                try:
                    parsed = json.loads(err_body)
                    retry_after = float(parsed.get("retry_after", 1.0))
                except Exception:
                    retry_after = 1.0
                time.sleep(max(0.0, retry_after))
                continue

            raise DiscordHTTPError(e.code, err_body[:300]) from None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="다음 날 할 일을 Discord 포럼 스레드에 게시합니다."
    )
    parser.add_argument(
        "--date",
        default=get_tomorrow_kst(),
        help="대상 날짜 (YYYY-MM-DD, 기본값: 한국 시간 기준 내일)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Discord 요청 및 파일 저장 없이 분할 결과만 출력",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="이미 게시된 날짜여도 다시 게시",
    )
    args = parser.parse_args()

    target_date = args.date.strip()
    cfg = load_or_init_config(dry_run=args.dry_run)

    posted_map = cfg.get("posted", {})
    if target_date in posted_map and posted_map[target_date] and not args.force:
        ids_str = ", ".join(str(mid) for mid in posted_map[target_date])
        print(f"이미 올림: {target_date} (메시지 id {ids_str})")
        return 0

    try:
        full_text = build_post_body(target_date)
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        return 1

    chunks = split_into_chunks(full_text, MAX_CHUNK_LEN)

    forum_channel_id = cfg.get("forum_channel_id")
    thread_id = cfg.get("thread_id")
    thread_title = cfg.get("thread_title", "📅 매일 할 일")

    if args.dry_run:
        if thread_id:
            target_desc = f"기존 스레드 (thread_id={thread_id})"
        else:
            target_desc = (
                f"새 포럼 스레드 생성 (forum_channel_id={forum_channel_id}, "
                f"title={thread_title!r})"
            )
        chunk_lengths = ", ".join(f"{idx + 1}번={len(c)}자" for idx, c in enumerate(chunks))
        print(f"[DRY-RUN] 대상 날짜: {target_date}")
        print(f"[DRY-RUN] 보낼 대상: {target_desc}")
        print(f"[DRY-RUN] 조각 개수: {len(chunks)}개 ({chunk_lengths})")
        print("[DRY-RUN] --- 첫 조각 전문 ---")
        print(chunks[0] if chunks else "")
        return 0

    try:
        token = load_bot_token()
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        return 1

    msg_ids: list[str] = []
    config_dirty = False

    try:
        start_idx = 0
        if not thread_id:
            first_payload = {
                "name": thread_title,
                "message": {
                    "content": chunks[0],
                    "allowed_mentions": {"parse": []},
                },
            }
            resp = discord_post_json(
                f"/channels/{forum_channel_id}/threads",
                first_payload,
                token,
            )
            thread_id = str(resp["id"])
            cfg["thread_id"] = thread_id
            config_dirty = True

            msg_obj = resp.get("message")
            if isinstance(msg_obj, dict) and msg_obj.get("id"):
                first_msg_id = str(msg_obj["id"])
            else:
                first_msg_id = thread_id
            msg_ids.append(first_msg_id)
            start_idx = 1

        for chunk in chunks[start_idx:]:
            payload = {
                "content": chunk,
                "allowed_mentions": {"parse": []},
            }
            resp = discord_post_json(
                f"/channels/{thread_id}/messages",
                payload,
                token,
            )
            msg_ids.append(str(resp["id"]))

    except DiscordHTTPError as e:
        if config_dirty:
            save_config(cfg)
        print(f"HTTP 오류 {e.status_code}: {e.body_snippet}", file=sys.stderr)
        return 1
    except Exception as e:
        if config_dirty:
            save_config(cfg)
        print(f"요청 중 오류 발생: {type(e).__name__}", file=sys.stderr)
        return 1

    cfg.setdefault("posted", {})[target_date] = msg_ids
    save_config(cfg)

    ids_str = ", ".join(msg_ids)
    print(f"게시 완료 {target_date}: 스레드 {thread_id}, 메시지 {ids_str}")

    now_str = datetime.datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    append_log(f"{now_str} {target_date} OK {','.join(msg_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
