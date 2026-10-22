import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "data" / "figjam-index.json"
DOCS_DIR = ROOT_DIR / "docs" / "figjam"
KST = timezone(timedelta(hours=9))


def load_index() -> dict:
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {
        "board": "5nPD4oRTN3oiVhiLnP0DpU",
        "aliases": {},
        "skip_names": [],
        "sections": {},
    }


def sanitize_filename(name: str) -> str:
    s = re.sub(r"\s+", "-", name.strip())
    s = re.sub(r"[^0-9A-Za-z가-힣ㄱ-ㅎㅏ-ㅣ_-]", "", s)
    s = s[:60]
    return s or "section"


def main() -> None:
    if len(sys.argv) < 2:
        print("사용법: python tools/figjam_save.py <read 결과 JSON 파일 경로> | --known", file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]
    index_data = load_index()
    aliases = index_data.get("aliases", {})
    skip_names = index_data.get("skip_names", [])
    sections_index = index_data.setdefault("sections", {})

    if arg == "--known":
        known = {sec_id: info.get("hash", "") for sec_id, info in sections_index.items()}
        print(json.dumps(known, ensure_ascii=False))
        return

    input_path = Path(arg)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    sections = payload.get("sections", [])

    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    now_kst = datetime.now(KST).isoformat(timespec="seconds")
    saved_files = []

    for sec in sections:
        sec_id = sec["id"]
        sec_name = sec.get("name") or sec_id
        if sec_name in skip_names:
            print(f"건너뜀: {sec_name}")
            continue
        sec_hash = sec.get("hash", "")
        items = sec.get("items", [])

        safe_name = sanitize_filename(sec_name)
        safe_id = sec_id.replace(":", "-")
        rel_file = f"docs/figjam/{safe_name}__{safe_id}.md"
        out_path = ROOT_DIR / rel_file

        by_author: dict[str, list[dict]] = {}
        for item in items:
            raw_author = (item.get("a") or "").strip()
            author = aliases.get(raw_author, raw_author) or "(작성자 없음)"
            by_author.setdefault(author, []).append(item)

        lines = [
            f"# {sec_name}",
            "",
            f"- 섹션 ID: `{sec_id}`",
            f"- 해시: `{sec_hash}`",
            f"- 저장 시각(KST): {now_kst}",
            "",
        ]

        for author, author_items in by_author.items():
            lines.append(f"## {author}")
            lines.append("")
            for it in author_items:
                text = it.get("t", "")
                lines.append(f"- {text}")
            lines.append("")

        out_path.write_text("\n".join(lines), encoding="utf-8")

        sections_index[sec_id] = {
            "name": sec_name,
            "hash": sec_hash,
            "file": rel_file,
            "saved_at": now_kst,
            "count": len(items),
        }
        saved_files.append(rel_file)

    INDEX_PATH.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"저장 완료: {len(saved_files)}개 섹션")
    for f in saved_files:
        print(f" - {f}")


if __name__ == "__main__":
    main()
