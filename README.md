# 게임기획 독학 관리 프로젝트

**innollia**(스승 겸 함께 공부)와 **pai**(제자)가 디스코드 서버 **핸섬가이즈**에서 대학 수준의 공개 게임기획 과정(MIT OCW, K-MOOC, 에듀코카 등)을 독학하고 게임 분석을 기록하는 관리 도구입니다.

- **학습 시간**: 하루 60~90분 (평일 75분, 주말 90분 / 바쁜 날 최소판 30분)
- **방식**: 3주(21일) 동안 완강이 아니라 대학 커리큘럼 전체 지도를 그리는 **1회독** 후, 5개 영역별 실제 과제를 수행하는 **2회독**으로 넘어갑니다.
- **분석 회차**: 2~3일에 한 번씩 같은 게임을 플레이하고 innollia는 `templates/analysis-guide.md`(백지 분석), pai는 `templates/pai-worksheet.md`(학습지)로 분석합니다.

## 폴더 및 파일 구조
- `docs/SPEC.md` — 프로젝트 명세
- `docs/plan-outline.md` — 21일 계획 골격 및 공식 URL 목록
- `docs/source/gpt-curriculum-2026-10-22.md` — 원본 커리큘럼 자료 (수정 금지)
- `data/plan.json` — 21일 상세 학습 계획
- `data/progress.json` — 학습자별(innollia, pai) 일일 진도 기록
- `data/second-pass.json` — 2회독 5영역 및 통과 기준 현황
- `templates/pai-worksheet.md` — 파이용 게임 분석 학습지 템플릿
- `templates/analysis-guide.md` — innollia용 백지 분석 가이드
- `tools/study.py` — 진도·출력·정적 페이지 생성 CLI (Python 3 표준 라이브러리만 사용)
- `site/index.html` — 정적 현황 페이지
- `out/` — 디스코드 공유용 내보내기 및 링크 점검 결과

## CLI 사용법 (`tools/study.py`)

```bash
# 오늘(또는 특정 날짜) 할 일 출력
python tools/study.py today [--date YYYY-MM-DD]

# 내일 할 일 출력 (today --date 내일과 동일)
python tools/study.py tomorrow

# 진도 완료 기록 (LEARNER = innollia | pai)
python tools/study.py done DAY LEARNER [--note TEXT]

# 21일 전체 진도표와 진행률 출력
python tools/study.py status

# 2회독 현황 출력 및 기준 체크 (4개 기준 모두 true면 "통과" 표시)
python tools/study.py second-pass [--set AREA LEARNER CRITERIA]

# 특정 날짜 할 일을 디스코드 공유용(md/json)으로 out/ 폴더에 저장
python tools/study.py export --date YYYY-MM-DD --format md|json

# plan.json의 모든 자료 URL 상태 확인 후 out/link-report.md 저장
python tools/study.py check-links

# site/index.html 정적 대시보드 생성
python tools/study.py build
```
