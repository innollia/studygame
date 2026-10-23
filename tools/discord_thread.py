#!/usr/bin/env python3
"""'📅 매일 할 일' 스레드의 학습자 답글 조회 및 매니저 답장 게시 도구."""

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# tools 폴더를 sys.path에 추가하여 discord_post 재사용
TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from discord_post import (  # noqa: E402
    API_BASE,
    CONFIG_PATH,
     LOG_PATH,
    KST,
    USER_AGENT,
    DiscordHTTPError,
    append_log,
    discord_post_json,
    load_bot_token,
    split_into_chunks,
)


def load_config() -> dict:
    """설정 파일 로드."""
    if not CONFIG_PATH.exists():
        raise RuntimeError(f"설정 파일을 찾을 수 없습니다: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg: dict) -> None:
    """설정 파일 저장 (기존 키 유지)."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")


def discord_get_json(endpoint: str, token: str) -> list | dict:
    """Discord GET 요청 수행."""
    url = f"{API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": USER_AGENT,
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw else []
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            err_body = ""
        raise DiscordHTTPError(e.code, err_body[:300]) from None


def format_kst(iso_ts: str) -> str:
    """ISO 타임스탬프를 KST 'YYYY-MM-DD HH:MM' 형식으로 변환."""
    if not iso_ts:
        return ""
    dt = datetime.datetime.fromisoformat(iso_ts.replace("Z", "+00:00"))
    return dt.astimezone(KST).strftime("%Y-%m-%d %H:%M")


def cmd_read(show_all: bool) -> int:
    """스레드 메시지 조회."""
    cfg = load_config()
    thread_id = cfg.get("thread_id")
    if not thread_id:
        raise RuntimeError("설정 파일에 thread_id가 없습니다.")

    last_seen_id = cfg.get("last_seen_id")
    last_seen_int = int(last_seen_id) if last_seen_id is not None else None

    token = load_bot_token()
    messages = discord_get_json(f"/channels/{thread_id}/messages?limit=100", token)
    if not isinstance(messages, list):
        messages = []

    # 오래된 순으로 정렬
    messages.sort(key=lambda m: int(m["id"]))

    printed_ids: list[str] = []
    for msg in messages:
        msg_id = str(msg["id"])
        msg_id_int = int(msg_id)

        if not show_all and last_seen_int is not None and msg_id_int <= last_seen_int:
            continue

        author = msg.get("author") or {}
        is_bot = bool(author.get("bot"))
        if is_bot and not show_all:
            continue

        username = author.get("username") or "unknown"
        if is_bot:
            username = f"[봇] {username}"

        kst_str = format_kst(msg.get("timestamp", ""))
        msg_ref = msg.get("message_reference") or {}
        ref_id = msg_ref.get("message_id")

        header_parts = [msg_id, kst_str, username]
        if ref_id:
            header_parts.append(str(ref_id))

        content = msg.get("content") or ""
        if is_bot and show_all:
            content = content[:80]

        print(f"--- {' | '.join(header_parts)}")
        print(content)

        for att in msg.get("attachments") or []:
            att_url = att.get("url")
            if att_url:
                print(f"첨부: {att_url}")

        printed_ids.append(msg_id)

    last_id = printed_ids[-1] if printed_ids else (last_seen_id or "없음")
    print(f"새 메시지 {len(printed_ids)}개, 마지막 id {last_id}")
    return 0


def cmd_mark(message_id: str) -> int:
    """마지막으로 확인한 메시지 ID 저장."""
    cfg = load_config()
    cfg["last_seen_id"] = str(message_id).strip()
    save_config(cfg)
    print(f"last_seen_id 저장 완료: {cfg['last_seen_id']}")
    return 0


def cmd_reply(md_path_str: str, reply_to: str | None) -> int:
    """마크다운 파일 내용을 스레드에 답장으로 게시."""
    md_path = Path(md_path_str)
    if not md_path.exists():
        raise RuntimeError(f"파일을 찾을 수 없습니다: {md_path}")

    text = md_path.read_text(encoding="utf-8").strip()
    if not text:
        raise RuntimeError(f"파일 내용이 비어 있습니다: {md_path}")

    cfg = load_config()
    thread_id = cfg.get("thread_id")
    if not thread_id:
        raise RuntimeError("설정 파일에 thread_id가 없습니다.")

    token = load_bot_token()
    chunks = split_into_chunks(text)
    sent_ids: list[str] = []

    for idx, chunk in enumerate(chunks):
        payload: dict = {
            "content": chunk,
            "allowed_mentions": {"parse": []},
        }
        if idx == 0 and reply_to:
            payload["message_reference"] = {
                "message_id": str(reply_to),
                "fail_if_not_exists": False,
            }
        resp = discord_post_json(f"/channels/{thread_id}/messages", payload, token)
        sent_ids.append(str(resp["id"]))

    ids_comma = ",".join(sent_ids)
    print(ids_comma)

    now_str = datetime.datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    append_log(f"{now_str} reply OK {ids_comma}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="'📅 매일 할 일' 스레드 답글 읽기 및 답장 보내기 도구"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # read 명령
    p_read = subparsers.add_parser("read", help="스레드 메시지 읽기")
    p_read.add_argument("--all", action="store_true", help="봇 포함 전체 메시지 출력")

    # mark 명령
    p_mark = subparsers.add_parser("mark", help="last_seen_id 갱신")
    p_mark.add_argument("message_id", help="저장할 마지막 메시지 ID")

    # reply 명령
    p_reply = subparsers.add_parser("reply", help="마크다운 파일로 답장 게시")
    p_reply.add_argument("md_path", help="답장 내용 마크다운 파일 경로")
    p_reply.add_argument("--to", dest="reply_to", help="답글 대상 message_id")

    args = parser.parse_args()

    try:
        if args.command == "read":
            return cmd_read(show_all=args.all)
        if args.command == "mark":
            return cmd_mark(args.message_id)
        if args.command == "reply":
            return cmd_reply(args.md_path, args.reply_to)
    except DiscordHTTPError as e:
        print(f"HTTP 오류 {e.status_code}: {e.body_snippet}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"오류: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
