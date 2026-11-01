"""피그잼 게임 아이디어 자동 분류 (하루 2번, 작업 스케줄러가 부른다).

봇 전용 크롬 프로필을 잠깐 켜서 보드를 열고, "게임 아이디어 판"에 올라온 스티키를
Jev로 분류해 섹션으로 옮긴 뒤 크롬을 끈다. 사용자 크롬과는 프로필이 달라 섞이지 않는다.
- 처음 한 번: python tools/idea_sorter.py --login  → 뜬 창에서 Figma 로그인 후 창을 닫는다.
- 실행:       pythonw tools/idea_sorter.py
- 스티키 원문은 기록하지 않는다. 기록: data/idea-sorter.log (git 제외)
"""

import asyncio
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

import websockets

sys.path.insert(0, str(Path(__file__).resolve().parent))
from idea_sort import classify  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BOARD = "https://www.figma.com/board/5nPD4oRTN3oiVhiLnP0DpU"
JS = ROOT / "tools" / "figjam_ideas.js"
LOG = ROOT / "data" / "idea-sorter.log"
PROFILE = Path(os.environ["LOCALAPPDATA"]) / "gamedesign-idea-bot"
PORT = 9333
CHROME = next(p for p in (
    Path(os.environ.get("PROGRAMFILES", "")) / "Google/Chrome/Application/chrome.exe",
    Path(os.environ.get("PROGRAMFILES(X86)", "")) / "Google/Chrome/Application/chrome.exe",
    Path(os.environ["LOCALAPPDATA"]) / "Google/Chrome/Application/chrome.exe",
) if p.exists())
PARAMS_LINE = 'const PARAMS = { mode: "read", from: ["게임 아이디어 판"], decisions: [] };'
# 창이 가려져 있어도 보드가 뜨도록 백그라운드 절전을 끈다(숨은 탭에서는 figma 전역이 안 생긴다).
FLAGS = ["--no-first-run", "--no-default-browser-check", "--disable-renderer-backgrounding",
         "--disable-backgrounding-occluded-windows", "--disable-background-timer-throttling",
         "--disable-features=CalculateNativeWinOcclusion"]


def log(msg):
    LOG.parent.mkdir(exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M} {msg}\n")


def script(params):
    src = JS.read_text(encoding="utf-8")
    assert PARAMS_LINE in src
    return src.replace(PARAMS_LINE, "const PARAMS = " + json.dumps(params, ensure_ascii=False) + ";").strip().rstrip(";")


class Page:
    def __init__(self, ws):
        self.ws, self.next_id = ws, 0

    async def call(self, method, params=None, timeout=120):
        self.next_id += 1
        await self.ws.send(json.dumps({"id": self.next_id, "method": method, "params": params or {}}))
        deadline = time.monotonic() + timeout
        while True:
            msg = json.loads(await asyncio.wait_for(self.ws.recv(), deadline - time.monotonic()))
            if msg.get("id") == self.next_id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error'].get('message')}")
                return msg.get("result", {})

    async def eval(self, expr):
        res = await self.call("Runtime.evaluate", {"expression": expr, "awaitPromise": True, "returnByValue": True})
        if "exceptionDetails" in res:
            raise RuntimeError("JS 오류: " + res["exceptionDetails"].get("text", "")[:200])
        return res.get("result", {}).get("value")


def page_ws():
    deadline = time.monotonic() + 30
    while True:
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/list", timeout=3) as r:
                pages = [t for t in json.load(r) if t["type"] == "page"]
            if pages:
                return pages[0]["webSocketDebuggerUrl"]
        except OSError:
            pass
        if time.monotonic() > deadline:
            raise RuntimeError("봇 크롬에 연결 못 함")
        time.sleep(1)


async def sort(page):
    await page.call("Page.navigate", {"url": BOARD})
    ready = "typeof figma !== 'undefined' && !!figma.currentPage && figma.currentPage.children.length > 0"
    deadline = time.monotonic() + 120
    while not await page.eval(ready):
        if time.monotonic() > deadline:
            url = await page.eval("location.href")
            raise RuntimeError("보드가 열리지 않음" + (" (로그인 필요: --login)" if "login" in url else ""))
        await asyncio.sleep(3)
    stickies = json.loads(await page.eval(script({"mode": "read", "from": ["게임 아이디어 판"], "decisions": []})))
    if not stickies:
        log("새 스티키 없음")
        return
    decisions = await asyncio.to_thread(classify, stickies)
    slim = [{k: d[k] for k in ("id", "kind", "maturity", "platform") if k in d} for d in decisions]
    result = await page.eval(script({"mode": "apply", "from": [], "decisions": slim}))
    await asyncio.sleep(10)  # 바뀐 내용이 서버에 저장될 시간
    log(f"분류 {len(stickies)}개 → {result} " + json.dumps(slim, ensure_ascii=False))


def main():
    if "--login" in sys.argv:
        subprocess.run([str(CHROME), f"--user-data-dir={PROFILE}", *FLAGS[:2], "https://www.figma.com/login"])
        return
    chrome = subprocess.Popen([str(CHROME), f"--user-data-dir={PROFILE}", f"--remote-debugging-port={PORT}",
                               "--window-size=1280,800", *FLAGS, "about:blank"])
    try:
        async def run():
            async with websockets.connect(page_ws(), max_size=None) as ws:
                await sort(Page(ws))
        asyncio.run(run())
    except Exception as error:
        log(f"실패: {type(error).__name__}: {str(error)[:200]}")
    finally:
        close_chrome(chrome)


def close_chrome(chrome):
    """CDP로 정상 종료(프로필 저장), 안 되면 강제 종료."""
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=3) as r:
            url = json.load(r)["webSocketDebuggerUrl"]

        async def close():
            async with websockets.connect(url) as ws:
                await ws.send(json.dumps({"id": 1, "method": "Browser.close"}))
        asyncio.run(close())
        chrome.wait(20)
    except Exception:
        chrome.kill()


if __name__ == "__main__":
    main()
