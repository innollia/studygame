# 게임기획 독학 관리 프로젝트 — 명세 (오케스트레이터 작성)

원본: docs/source/gpt-curriculum-2026-10-22.md (수정 금지). 모든 문서는 한국어, 쉬운 말.

## 학습자
- innollia (스승 겸 같이 공부. 고등학생. "백지 분석": 템플릿만 보고 자기 말로 분석)
- pai (제자, 디스코드 hanguoren10293. 질문 몇 개 적힌 "학습지"를 채움)
- 장소: 디스코드 서버 "핸섬가이즈". 방식: 게임을 만드는 것보다 게임 분석 우선. 개발 경험=게임잼, 최신 흐름=유튜브, 기초=강의. 분석은 하루이틀에 한 번.
- 하루 공부 시간은 60~90분 이내로 잡는다(학교 수행평가 병행). 마감 압박이 있을 땐 "최소판(30분)"도 둔다.

## 파일 구조 (의존성은 Python 3 표준 라이브러리만)
- README.md — 사용법 (한국어, 짧게)
- data/plan.json — 21일 계획 (아래 형식)
- data/progress.json — 진도 기록 (아래 형식)
- data/second-pass.json — 2회독 5영역 x 통과기준 4개 x 학습자 2명
- templates/pai-worksheet.md — 파이용 학습지 템플릿 (분석 회차마다 복사해 씀)
- templates/analysis-guide.md — innollia용 백지 분석 가이드
- tools/study.py — CLI
- site/index.html — study.py build 가 생성하는 정적 페이지 (외부 라이브러리 없음, 모바일에서도 보임)
- out/ — study.py export 결과 (gitignore 하지 않음, 디스코드 연동용 출력)

## data/plan.json 형식
{"start_date":"2026-10-23","days":[{"day":1,"date":"2026-10-23","week":1,"theme":"...",
 "minutes":75,"min_version_minutes":30,
 "materials":[{"title":"...","url":"https://...","note":"...","login_required":false}],
 "tasks":{"common":"둘이 같이 할 일","innollia":"...","pai":"..."},
 "analysis_session":false}, ...]}
- 학습지/분석 회차 날은 analysis_session=true, tasks에 템플릿 경로 언급.

## data/progress.json 형식
{"days":{"1":{"innollia":{"done":false,"date":null,"note":""},"pai":{...}}, ...}}
(21일 전부 미리 채워 둔다)

## data/second-pass.json 형식
{"areas":[{"id":1,"name":"게임디자인 이론","sources":"...","criteria":[
 {"id":"lecture","name":"실제 대학 강의를 학습했는가"},
 {"id":"assignment","name":"공식 과제를 수행했는가"},
 {"id":"apply","name":"새 사례에 적용할 수 있는가"},
 {"id":"feedback","name":"외부 피드백·테스트로 자기 판단을 검토했는가"}],
 "status":{"innollia":{"lecture":false,"assignment":false,"apply":false,"feedback":false},"pai":{...}},"notes":""}, ...]}
영역 5개는 원본 "2회독" 목록 그대로(1 이론 / 2 분석·설계 방법론 / 3 시스템·레벨·밸런스 / 4 플레이테스트와 개선 / 5 실전 제작). 각 영역 sources는 원본의 자료와 과제를 그대로 옮긴다.

## tools/study.py 명령 (argparse)
- today [--date YYYY-MM-DD] : 그날 할 일을 터미널에 출력. 기본은 오늘. 계획 범위 밖이면 "계획 시작 전/종료 후" 안내.
- tomorrow : 내일 할 일 (today --date 내일과 동일)
- done DAY LEARNER [--note TEXT] : 진도 기록 (LEARNER = innollia|pai). 오늘 날짜 저장.
- status : 21일 진도표(누가 끝냈나)와 전체 진행률 출력
- second-pass [--set AREA LEARNER CRITERIA] : 2회독 현황 출력/체크. 4개 모두 true면 "통과" 표시
- export --date YYYY-MM-DD --format md|json : out/YYYY-MM-DD.md 또는 .json 에 하루치 출력 (디스코드에 붙일 수 있는 형식. md는 2000자 이하)
- check-links : plan.json의 모든 url에 HTTP 요청(urllib, 타임아웃 15초, User-Agent 지정). 상태 코드 출력. login_required=true 는 200/302/403 이어도 "로그인 필요(예상됨)" 로 표시. 결과를 out/link-report.md 에 저장.
- build : site/index.html 생성(plan+progress 임베드). 오늘 날짜 칸을 맨 위에 크게 "오늘/내일 할 일"로, 아래에 21일 목록과 진도 체크 표시, 2회독 현황 표.
Windows 콘솔에서 한글이 깨지지 않게 stdout을 utf-8로 설정한다. 파일 읽기/쓰기는 항상 encoding="utf-8".
