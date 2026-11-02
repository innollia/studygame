"""피그잼 하루 변화 보기 (매니저가 매일 밤 부른다).

봇 크롬으로 보드를 열어 섹션 지문 목록을 뽑고, 어제 본 지문(data/figjam-daily.json, git 제외)과
비교해 new/changed 섹션만 읽어 출력한다. 작성자 이름은 aliases로 바꾼다. 저장소에는 아무것도 저장하지 않는다.
공부 섹션을 남기려면 --out 파일을 tools/figjam_save.py에 넘긴다(docs/FIGJAM.md).
- 실행: python tools/figjam_check.py [--out read.json] [--dry]   (--dry: 기준 지문을 갱신하지 않음)
"""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path

import websockets

sys.path.insert(0, str(Path(__file__).resolve().parent))
import idea_sorter as bot  # noqa: E402

ROOT = bot.ROOT
DAILY = ROOT / "data" / "figjam-daily.json"
INDEX = ROOT / "data" / "figjam-index.json"
JS = ROOT / "tools" / "figjam_extract.js"


def script(mode, only=(), known=None):
    src = JS.read_text(encoding="utf-8")
    src = src.replace('const MODE = "list";', f'const MODE = "{mode}";')
    src = src.replace("const ONLY = [];", "const ONLY = " + json.dumps(list(only)) + ";")
    src = src.replace("const KNOWN = {};", "const KNOWN = " + json.dumps(known or {}) + ";")
    return src.strip().rstrip(";")


async def check(page, known):
    await page.call("Page.navigate", {"url": bot.BOARD})
    ready = "typeof figma !== 'undefined' && !!figma.currentPage && figma.currentPage.children.length > 0"
    deadline = time.monotonic() + 240  # 보드가 커서 2분 넘게 걸릴 때가 있다
    while not await page.eval(ready):
        if time.monotonic() > deadline:
            raise RuntimeError("보드가 열리지 않음 (로그인 풀렸으면 python tools/idea_sorter.py --login)")
        await asyncio.sleep(3)
    listing = json.loads(await page.eval(script("list", known=known)))["sections"]
    changed = [s["id"] for s in listing if s["status"] != "same" and s["count"]]
    read = json.loads(await page.eval(script("read", only=changed)))["sections"] if changed else []
    return listing, read


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    known = json.loads(DAILY.read_text(encoding="utf-8")) if DAILY.exists() else {}
    aliases = json.loads(INDEX.read_text(encoding="utf-8")).get("aliases", {})
    chrome = subprocess.Popen([str(bot.CHROME), f"--user-data-dir={bot.PROFILE}", f"--remote-debugging-port={bot.PORT}",
                               "--window-size=1280,800", *bot.FLAGS, "about:blank"])
    try:
        async def run():
            async with websockets.connect(bot.page_ws(), max_size=None) as ws:
                return await check(bot.Page(ws), known)
        listing, read = asyncio.run(run())
    finally:
        bot.close_chrome(chrome)

    if out:
        Path(out).write_text(json.dumps({"mode": "read", "sections": read}, ensure_ascii=False), encoding="utf-8")
    if "--dry" not in sys.argv:
        DAILY.write_text(json.dumps({s["id"]: s["hash"] for s in listing}, ensure_ascii=False, indent=1), encoding="utf-8")

    sys.stdout.reconfigure(encoding="utf-8")
    print("섹션: " + ", ".join(f"{s['name']}({s['id']}) {s['status']}" for s in listing))
    if not read:
        print("바뀐 섹션 없음")
    for sec in read:
        print(f"\n##### {sec['name']} ({sec['id']})")
        for it in sec["items"]:
            who = aliases.get(it["a"], it["a"]) or "-"
            print(f"[{who}] {it['t']}")


if __name__ == "__main__":
    main()
