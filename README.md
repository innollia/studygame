# 게임기획 독학 관리 프로젝트 (v2)

**innollia**(스승 겸 함께 공부)와 **pai**(제자)가 디스코드 서버 **핸섬가이즈**에서 대학 수준의 공개 게임기획 과정(MIT OCW, K-MOOC, 에듀코카 등)을 독학하고 게임 분석·게임잼 복기를 기록하는 관리 도구입니다.

- **일정 구성 (`2026-10-22 ~ 2026-11-30`)**: 사전 기준선 분석(`A0`) 및 두 번의 게임잼·복기(`J1~J8`, `R1~R3`) → 1회독 본과정(`D1~D21`, 휴식 `X1`) → 보강 주간(`B1~B5`) 및 월간 리뷰(`M1`) → 이후 5영역 **2회독** 진행
- **학습 시간**: 공부/분석 평일 75분·주말 90분(바쁜 날 최소판 30분), 잼 날 3분 결정 로그, 일요일 끝 10분 주간 리뷰

## 주요 문서 및 폴더 구조
- `docs/MANAGER.md` — 연구 결과(research/1~7)를 바탕으로 매니저가 일정·학습·피드백·분석·유튜브·게임잼을 운영하는 핵심 규칙서
- `docs/plan-outline-v2.md` — v2 일정 골격 및 공식 URL 정본
- `templates/` — 백지 분석 가이드(`analysis-guide.md`), 파이 학습지(`pai-worksheet.md`), 유튜브 카드(`youtube-card.md`), 잼 복기(`jam-postmortem.md`), 주간 리뷰(`weekly-review.md`) 등 회차별 작성 양식 모음
- `data/plan.json` — 전체 일정 상세 계획 (v2)
- `data/progress.json` — 학습자별(`innollia`, `pai`) 진도·소요시간 기록 (v2)
- `data/second-pass.json` — 2회독 5영역 및 통과 기준 현황
- `tools/study.py` — 진도·출력·정적 페이지 생성 CLI (Python 3 표준 라이브러리 전용)
- 디스코드 자동 게시: 매일 21:30 KST에 AWS 서버(eve-runtime-host)가 이 저장소를 `git pull`한 뒤 `tools/discord_post.py`를 실행한다. 그래서 plan.json·progress.json은 **push해야 게시에 반영**된다. 이 PC에서는 discord_post.py를 실행하지 않는다(중복 게시 위험).
- 디스코드 보고: "📅 매일 할 일" 스레드에 답글로 보고한다. 봇을 @멘션하면 매니저(Claude)가 바로 답하고, 멘션하지 않은 보고는 매일 23:30 정기 처리에서 답한다. `tools/discord_thread.py`의 read/reply/mark 인터페이스는 바깥 호출 경로가 쓰므로 바꿀 때 관제와 상의한다.
- `site/index.html` — 정적 현황 보드 (Phase별 접기/펼치기, 다크 테마)
- `out/` — 디스코드 공유용 내보내기 및 링크 점검 리포트

## CLI 사용법 (`tools/study.py`)

```bash
# 오늘(또는 특정 날짜) 할 일 출력 (해당 날짜 일정이 없으면 가장 가까운 다음 날 안내)
python tools/study.py today [--date YYYY-MM-DD]

# 내일 할 일 출력
python tools/study.py tomorrow [--date YYYY-MM-DD]

# 진도 완료 기록 (ID 예: A0, J1, R1, D1~D21, M1 / LEARNER = innollia | pai)
python tools/study.py done ID LEARNER [--min] [--minutes N] [--note TEXT] [--date YYYY-MM-DD]

# 일정 건너뜀(skipped) 기록
python tools/study.py skip ID LEARNER [--note TEXT] [--date YYYY-MM-DD]

# 전체 진도표 및 1회독(D1~D21) 진행률(최소판 횟수 포함) 출력
python tools/study.py status

# 2회독 현황 출력 및 기준 체크 (4개 기준 모두 true면 "통과" 표시)
python tools/study.py second-pass [--set AREA LEARNER CRITERIA] [--value true|false]

# 특정 날짜 할 일을 디스코드 공유용(md/json)으로 out/ 폴더에 저장
python tools/study.py export --date YYYY-MM-DD --format md|json

# plan.json의 모든 자료 및 게임 URL 상태 확인 후 out/link-report.md 저장
python tools/study.py check-links

# site/index.html 정적 대시보드 재생성
python tools/study.py build
```
