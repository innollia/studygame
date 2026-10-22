# 계획 v2 골격 (2026-10-22 매니저 확정) — data/plan.json 으로 옮길 것

규칙은 docs/MANAGER.md. URL은 여기 적힌 것만 쓴다(지어내지 말 것). 요일: 10/23 금, 11/3 화, 11/6 금, 11/7 토, 11/8 일.

## 날 유형(type)과 기본 시간
- `jam` 잼 날: 공부 0분. 할 일 = 잼 세션 끝에 "결정 로그" 1줄(시각/결정/이유/버린 것) 3분. 파이 유튜브는 막힌 문제 해결용 5~15분만.
- `review` 복기 날: templates/jam-postmortem.md 사용. 60분(11/1만 15분 짧은 버전).
- `study` 공부 날: 평일 75분, 주말 90분, 최소판 30분. 시작은 항상 "2분 인출"(지난 개념 하나를 자료 없이 말하기 → 원문과 맞추기).
- `analysis` 분석 날: 60~90분. templates/analysis-guide.md(아안), templates/pai-worksheet.md(파이). 렌즈 하나와 게임 하나.
- `rest` 쉬는 날: 0분. 의무 없음.
- `buffer` 보강 날: 밀린 회차만. 밀린 게 없으면 자유.
- 평일 study/analysis 날 파이 할 일에는 항상 "학교 시간 유튜브: 깊게 1편 + 훑기 1~2편, 깊게 본 영상은 templates/youtube-card.md로 디스코드에 기록"을 넣는다(jam/rest/review 날 제외).
- 일요일(11/8, 11/15, 11/22)에는 끝 10분 주간 리뷰(templates/weekly-review.md)를 추가한다.

## 날짜별

id | 날짜 | type | 내용
---|---|---|---
A0 | 10/22 목 | analysis | (이미 완료) Deepest Sword 기준선 분석. 자료: https://cosmicadventuresquad.itch.io/deepest-sword , 결과: feedback/2026-10-22-deepest-sword.md
J1 | 10/23 금 | jam | 아리스토텔레스 1일차. 시작 전 10분: 잼 규칙 확인 + "이번 잼에서 실험할 설계 가설 1개" 정하기(templates/jam-postmortem.md 의 '잼 전' 칸)
J2 | 10/24 토 | jam | 아리스토텔레스
J3 | 10/25 일 | jam | 아리스토텔레스
J4 | 10/26 월 | jam | 아리스토텔레스
J5 | 10/27 화 | jam | 아리스토텔레스 마감
R1 | 10/28 수 | review | 아리스토텔레스 복기 60분. 초점: 일정 예상 vs 실제, 최소 플레이 범위, 첫 외부 테스트 시점. 끝에 slap jam에서 바꿀 규칙 CHANGE 1개
J6 | 10/29 목 | jam | slap jam 1일차. 10/28의 CHANGE를 실제로 적용
J7 | 10/30 금 | jam | slap jam
J8 | 10/31 토 | jam | slap jam (Flesh Pit 목표일이기도 함 — 무리 금지)
R2 | 11/01 일 | review | slap jam 제출 + 15분 짧은 복기(각자 잘된 것 1, 아쉬운 것 1, 다음에 바꿀 것 1). 나머지는 11/2
R3 | 11/02 월 | review | slap jam 복기 나머지 45분 + 두 잼 비교(10/28 CHANGE가 실행됐나, 같은 문제가 줄었나). 마지막 10분: K-MOOC 게임컨셉디자인 수강신청 확인
D1 | 11/03 화 | study | 1회독 지도 그리기. 자료: CMS.608 Syllabus https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/syllabus/ , CMS.608 Calendar https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/calendar/ , K-MOOC 강의계획 https://www.kmooc.kr/view/course/detail/21313 . 산출물: 3주 동안 볼 것의 한 장 지도. 참고: CMS.608 오디오 강의는 현재 막혀 있음
D2 | 11/04 수 | study | 메커니즘과 의미 있는 선택. 자료: K-MOOC 6주 1-1 '메카닉스와 매커니즘의 개요'(https://www.kmooc.kr/view/course/detail/21313), CMS.608 Calendar Session 2 'Meaningful Decisions, Visibility' 읽기 주제(위 Calendar URL). 영어 선택: CMS.611J Session 1 https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-1-introduction/ . 산출물: 용어 3개를 자기 말로 + 아는 게임 장면 하나씩
D3 | 11/05 목 | analysis | A1 렌즈 MDA·감정. 사전 10분: MDA 논문 핵심 https://www.cs.northwestern.edu/~hunicke/MDA.pdf . 게임: We Become What We Behold https://ncase.itch.io/wbwwb (한국어 팬번역 https://game.hyeon.me/wbwwb/). 질문: 실제 규칙 하나 / 그 규칙에서 반복된 행동 / 감정이 언제 어떻게 바뀌었나
X1 | 11/06 금 | rest | 쉬는 날. 의무 없음
D4 | 11/07 토 | study | 게임 장르. 자료: 에듀코카 '장르에 대한 이해' https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=1044 (로그인 없이 열림 확인), K-MOOC 3주 1-1·1-2. 산출물: 장르 2개의 핵심 메커니즘 비교표
D5 | 11/08 일 | study | 대학이 내는 과제 보기. 자료: CMS.608 Assignment 1 Single Mechanic https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmentone/ , Assignment 2 Experience and Aesthetics https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmenttwo/ , 학생작품 https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/assignments-and-student-work/ (규칙서 하나 읽기). + 주간 리뷰 10분
D6 | 11/09 월 | analysis | A2 렌즈 '계획과 결과가 보이는가(FADT)'. 사전 10분: Formal Abstract Design Tools https://www.gamedeveloper.com/design/formal-abstract-design-tools . 게임: Sort the Court! https://graebor.itch.io/sort-the-court . 질문: 선택 전에 무엇을 예상했나 / 결과를 무엇으로 알았나 / 몰라서 생긴 실수는 의도된 불확실성인가 소통 실패인가
D7 | 11/10 화 | study | 1주차 정리. 지도 갱신 + 서로에게 설명 10분씩 + 이틀 전 용어 인출 시험(자료 없이 3개)
D8 | 11/11 수 | study | 설계 방법론의 지도. 자료: CMS.301 Calendar https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/calendar/ , Assignments https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/ (특히 Assignment 2 Board Game Analysis — MIT가 분석 과제에 무엇을 요구하는지 우리 분석과 비교)
D9 | 11/12 목 | study | 레벨디자인. 자료: K-MOOC 9주 1-1 '레벨 디자인의 개요와 기본 개념', GMTK 레벨 4단계 영상 https://www.youtube.com/watch?v=dBmIkEvEBtA . 산출물: Deepest Sword에서 소개→전개→비틀기 장면 찾기(없으면 없다고)
D10 | 11/13 금 | analysis | A3 렌즈 '레벨이 가르치는 순서'. 게임: Celeste Classic https://www.lexaloffle.com/bbs/?tid=2145 . 질문: 규칙을 안전하게 소개하는 장면 / 같은 규칙을 어렵게 응용하는 장면 / 예상이 뒤집히는 구간
D11 | 11/14 토 | study | UI/UX. 자료: K-MOOC 10주 1-1 'UI/UX 개요', 1-2 'UI/UX의 설계 방법'. 선택: Design Doc 'Great and Terrible UX Design in Games' https://www.youtube.com/watch?v=o86rWZlF30g . 산출물: 우리 잼 게임 화면 하나의 정보 우선순위 점검
D12 | 11/15 일 | study | 밸런스 입문. 자료: Game Balance Concepts Level 1 https://gamebalanceconcepts.wordpress.com/2010/07/07/level-1-intro-to-game-balance/ . 산출물: 선택지 하나의 비용/효용 분석. + 주간 리뷰 10분
D13 | 11/16 월 | analysis | A4 렌즈 '피드백 루프와 밸런스'. 사전 10분: Game Balance Concepts Level 7 https://gamebalanceconcepts.wordpress.com/2010/08/18/level-7-advancement-progression-and-pacing/ . 게임: Super Auto Pets https://store.steampowered.com/app/1714040/ (무료, 한국어) — 설치가 어려우면 2048 https://play2048.co/ . 질문: 이득이 다음 이득을 키우는 장치 / 뒤처진 쪽을 돕거나 앞선 쪽을 막는 장치 / 하나를 바꾸면 흐름이 어떻게 바뀌나
D14 | 11/17 화 | study | 기획문서와 프로토타입. 자료: CMS.301 Assignment 5 GDD & Pitch https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment5/ , High Level Design Document Template https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_highlevel/ , Assignment 6 Prototyping https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment6/ . 산출물: 2주차 지도 + '기획문서→프로토타입→검증' 흐름도
D15 | 11/18 수 | study | 플레이테스트 설계. 자료: CMS.301 Assignment 7 Playtest https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment7/ , CMS.301 Readings(7주차 Playtesting) https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/readings/ . 산출물: D17에 쓸 테스트 질문지(확인할 질문 1개 + 사전 예상)
D16 | 11/19 목 | study | 제작 과정은 어떻게 평가받나. 자료: CMS.611J Syllabus https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/syllabus/ , Calendar https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/calendar/ , 영상 목록 https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/ . 산출물: 평가 기준 5개(기능20/반복디자인20/관리20/개인 포스트모템20/팀 포스트모템20)와 우리 두 잼 비교
D17 | 11/20 금 | analysis | A5 렌즈 '플레이테스트 관찰'. 대상: 우리 잼 게임(아리스토텔레스 또는 slap jam)을 처음 보는 사람 1명에게 해설 없이 플레이시키고 관찰(사람이 없으면 Gravitas https://store.steampowered.com/app/1067310/Gravitas 를 서로에게 처음 시켜 보고 '친구 간 예비 테스트'라고 표시). D15 질문지 사용. 기록: 막힌 시점·시도한 행동·말한 것
D18 | 11/21 토 | study | 테스트와 QA. 자료: CMS.611J Session 7 https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-7-testing-and-guest-lecture-with-genevieve-conley-of-riot-games/ (1:22:08 — 전체 아님, 플레이테스트 부분 25~30분), Lecture Slides(Testing) https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/lecture-slides-and-readings/ . 산출물: D17 관찰을 강의 기준으로 다시 보기
D19 | 11/22 일 | study | 협업과 일정 관리. 자료: CMS.611J Session 6 Agile Project Management https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-6-agile-project-management/ (1:44:40 — 슬라이드 25분 + 영상 20분만), Lecture Slides(Agile) 위 URL. 산출물: 핸섬가이즈 다음 작업 백로그. + 주간 리뷰 10분
D20 | 11/23 월 | analysis | A6 렌즈 '배운 것을 우리 게임에'. 자료: CMS.301 Assignment 8 https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment8/ . 대상: 우리 게임(잼 게임 또는 Flesh Pit). A1~A5 렌즈 중 2개로 분석 + 바꿀 점 1개와 확인 방법을 1쪽으로
D21 | 11/24 화 | study | 1회독 종료. 자료: 세 강의 Calendar(위 URL들). 산출물: 전체 지도 완성(각 개념이 어느 강의 어느 회차인지), 이틀 전 내용 인출 시험, 2회독 첫 영역 고르기
B1~B5 | 11/25 수 ~ 11/29 일 | buffer | 보강 칸. 밀린 회차를 여기서. 밀린 게 없으면 자유(유튜브·제작)
M1 | 11/30 월 | review | 월간 리뷰 20분: 계획 vs 실제 시간, 정상/최소판/휴식 횟수, 다음 달 계획 보정, 2회독 시작
