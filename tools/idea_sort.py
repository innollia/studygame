"""피그잼 게임 아이디어 분류기 (Jev).

입력: 스티키 목록 JSON [{"id", "text", "author"}] (파일 경로 또는 표준입력)
출력: 판정 JSON [{"id", "kind", "maturity", "platform", "answers"}] (표준출력)

판단은 Jev가, 결정은 아래 decide()가 한다. 질문 문구는 QUESTIONS에만 둔다.
키는 환경변수 TYPESAFE_API_KEY에서 읽는다. 스티키 원문은 저장소에 남기지 않는다.
"""

import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

API = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"
YES, NO = 0.7, 0.3

QUESTIONS = {
    "is_reaction": {
        "type": "noul",
        "instructions": "Is `sticky` a reaction to another sticky note rather than an idea of its own?",
        "criteria": {
            "true": "A short opinion about some other idea, like '가볍게 만들어볼만한듯' or '이거 재밌을 듯'",
            "false": "The note proposes its own game, theme, mechanic, or topic, even in one word like '경마'",
        },
    },
    "is_image_prompt": {
        "type": "noul",
        "instructions": "Does `sticky` ask an image generator to draw a picture?",
        "criteria": {
            "true": "It is a drawing request, like '고양이 그림을 그려줘, 배경은 빼줘'",
            "false": "It describes a game, a game topic, a mechanic, or a plan for making games",
        },
    },
    "has_play": {
        "type": "noul",
        "instructions": "Does `sticky` say what the player actually does while playing?",
        "criteria": {
            "true": "A concrete player action or loop is written, like 'merge units that attack enemies' or 'brew the tea the customer hinted at'",
            "false": "Only a topic, genre, mood, or platform is written, like '경마' or '로블록스 타워'",
        },
    },
    "detail": {
        "type": "score",
        "instructions": "How far has the game idea in `sticky` been worked out?",
        "criteria": [
            "Only a word or topic, like '경마' or '드럼통'",
            "One mechanic or twist, without saying how a play session goes",
            "A core mechanic plus a goal, twist, or progression that makes it a playable game",
            "A plan with mechanics, progression, and content or production notes",
        ],
    },
    "names_indie": {
        "type": "noul",
        "instructions": "Does `sticky` itself say this is an indie, PC, or Steam game?",
        "criteria": {"true": "The text says 인디, PC, or 스팀", "false": "The text does not mention indie, PC, or Steam"},
    },
    "names_roblox": {
        "type": "noul",
        "instructions": "Does `sticky` itself say this is a Roblox game?",
        "criteria": {"true": "The text says 로블록스, 로블, or Roblox", "false": "The text does not mention Roblox"},
    },
    "names_mobile": {
        "type": "noul",
        "instructions": "Does `sticky` itself say this is a mobile game?",
        "criteria": {
            "true": "The text says the game is for 모바일 or phones",
            "false": "The text does not say which device the game is for, or names another platform",
        },
    },
    "best_platform": {
        "type": "choice",
        "instructions": "Which platform suits the game in `sticky` best?",
        "criteria": {
            "indie_pc": "A PC indie game sold on Steam or itch.io, often story, puzzle, or a single-player twist",
            "roblox": "A Roblox experience played with friends, often obby, tower, simulator, or PvP with items",
            "mobile": "A phone game played in short sessions with taps or swipes, often casual or management",
        },
    },
    "fits_any": {
        "type": "noul",
        "instructions": "Would the game in `sticky` work about equally well on PC, Roblox, and mobile?",
        "criteria": {
            "true": "Nothing in the idea ties it to one platform",
            "false": "Its controls, players, or business model clearly suit one platform",
        },
    },
}


def api_key():
    """환경변수, 없으면 key-pool 파일(JEV__BELLASIL2085). 값은 출력하지 않는다."""
    if key := os.environ.get("TYPESAFE_API_KEY", "").strip():
        return key
    pool = Path.home() / ".all-tomorrow" / "key-pool.env"
    for line in pool.read_text(encoding="utf-8-sig").splitlines():
        name, sep, value = line.strip().partition("=")
        if sep and name.strip() == "JEV__BELLASIL2085" and value.strip():
            return value.strip().strip("\"'")
    raise RuntimeError("Jev 키 없음")


def ask(sticky):
    body = {"model": MODEL, "state": {"sticky": sticky["text"]}, "questions": QUESTIONS}
    req = urllib.request.Request(
        API,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + api_key(),
            "Content-Type": "application/json",
            "User-Agent": "gamedesign-study-idea-sort",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as res:
        return json.load(res)["answers"]


def decide(a):
    n = lambda k: a[k]["noul"]
    if n("is_reaction") > YES or (n("is_reaction") > NO and n("has_play") < NO):
        return {"kind": "reaction"}
    if n("is_image_prompt") > YES:
        return {"kind": "other"}
    # detail 2 = 핵심 동작 + 목표·변주·성장까지 있음
    maturity = "useful" if a["detail"]["score"] >= 1.8 else "fragment"
    named = [p for p, k in (("indie", "names_indie"), ("roblox", "names_roblox"), ("mobile", "names_mobile")) if n(k) > YES]
    if len(named) == 1:
        platform = named[0]
    elif named or n("fits_any") > YES:
        platform = "any"
    else:
        platform = {"indie_pc": "indie", "roblox": "roblox", "mobile": "mobile"}[a["best_platform"]["choice"]]
    return {"kind": "idea", "maturity": maturity, "platform": platform}


def classify(stickies):
    with ThreadPoolExecutor(8) as pool:
        answers = list(pool.map(ask, stickies))
    out = []
    for s, a in zip(stickies, answers):
        brief = {k: round(v["noul"], 2) if v["type"] == "noul" else v.get("choice") or round(v["score"], 2)
                 for k, v in a.items()}
        out.append({"id": s["id"], **decide(a), "answers": brief})
    return out


def main():
    src = open(sys.argv[1], encoding="utf-8") if len(sys.argv) > 1 else sys.stdin
    print(json.dumps(classify(json.load(src)), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
