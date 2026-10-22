# 리서치 7 — 대학 공개강의 자료 정밀 매핑

조사일: 2026-10-22 (한국시간)  
대상: innollia/studygame, research/prompts.md #7, data/plan.json D1~D21  
성격: **조사 결과/계획 수정 제안**. 원본 data/plan.json은 변경하지 않음.

## 핵심 결론 5줄

1. **MIT CMS.608(2014)**의 강의 자료는 영상이 아닌 **오디오 중심**이고, 공식 진도표에 현재 오디오 접근 불가라고 공지되어 있다. D2의 '영상 1개 시청'은 그대로 시행할 수 없으므로 한국어 K-MOOC 차시 또는 CMS.611J 영상을 지정해야 한다. [608-C]
2. **MIT CMS.301(2016)**에는 현재 공개 사이트 탐색 메뉴상 강의 영상이 없고, **26회 수업 주제 + 읽기 목록 + 8개 과제**가 핵심이다. D8·D14·D15에 적합한 과제는 5·6·7번이다. [301-C][301-A]
3. **MIT CMS.611J(2014)**은 영상 26개(세션 1~20, 22~27; 세션 21 영상 없음)가 공개되어 있다. 기존 계획의 영상 링크 /pages/lecture-videos/ 대신 **/video_galleries/lecture-videos/** 를 사용해야 한다. [611-V]
4. **K-MOOC 게임컨셉디자인**은 15주·총 VOD 24시간 59분이며 현재 표시된 운영 기간은 2026-10-18~2027-01-31이다. 공개 강의계획서에 주차별 차시명이 있지만 **개별 영상 길이는 보이지 않는다**. [KM]
5. **에듀코카 4편(pSeq 1044·1045·1046·794)**의 직접 상세 페이지는 조사 환경에서 열리지 않아 **영상 길이·접근 가능성 모두 미확인**이다. 길이를 임의로 기입하지 않고 대체 과목을 제공한다. [EDU]

## 표 읽는 법

- **실제 영상 길이**는 플레이어/공식 제공처에서 확인한 재생 시간만 기입. 확인되지 않은 영상에는 **미확인**, 영상이 없는 텍스트·PDF에는 **비영상**.
- **권장 분량**은 하루 공부시간 75/90분 안에서 자료를 읽거나 부분 시청할 **운영 제안**이지 원자료의 실제 길이가 아니다.
- MIT 강의의 영문 원제는 공식 강의계획/과제 목록을 기준으로 했다. 나열된 교재 장은 일부 유료 도서에 속하므로 공개 강의계획에 있다는 이유만으로 무료 전문이 있다고 보지 않는다.
- K-MOOC 강의계획서는 **각 주차 안에서 1-1, 1-2, 1-3 번호를 다시 사용**한다. 예컨대 '6주 1-1'은 6주 메커니즘 첫 차시를 말한다.
- 아래 날짜는 data/plan.json에 적힌 **기존 날짜**이고, 잼·휴식일 충돌에 따라 재편성할지는 별도 작업이다.

## A. 강의별 실제 목차·자료 표

### A-1. MIT CMS.608 Game Design — 2014 봄

공식: [Syllabus](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/syllabus/) · [Calendar](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/calendar/) · [Readings](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/readings/) · [Audio Lectures](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/video_galleries/audio-lectures/) · [Assignments and Student Work](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/assignments-and-student-work/). [608-C][608-A]

| Session | 공식 Calendar의 수업 주제/활동 | 중요 읽기·연결 자료 | 녹음 길이 |
|---|---|---|---|
| 1 | Course Introduction & Overview; What is a Game? | Challenges for Game Designers, ch.1 The Basics; [과제 1](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmentone/) | 접근 불가 |
| 2 | Meaningful Decisions, Visibility | Donald Norman, The Psychopathology of Everyday Things | 접근 불가 |
| 3 | Prototyping; Playtest | Game Design Workshop, Prototyping / Playtesting | 접근 불가 |
| 4 | Mechanics, Dynamics, and Aesthetics: The MDA Framework | [MDA: A Formal Approach to Game Design and Game Research (PDF)](https://www.cs.northwestern.edu/~hunicke/MDA.pdf) | 접근 불가 |
| 5 | Imperfect Information and Dice; Playtest | David Parlett, The Role of Dice | 접근 불가 |
| 6 | Constraints and Usability | Donald Norman, Knowing What To Do | 접근 불가 |
| 7 | Assignment 1 due; Assignment 2 team formation | [과제 2 Experience and Aesthetics](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmenttwo/) | 접근 불가 |
| 8 | Assignment 1 report and changelog | Challenges for Game Designers, ch.2 Game Design Atoms | 접근 불가 |
| 9 | Randomness and Player Choice | John Kaufeld, Randomness, Player Choice, and Player Experience | 접근 불가 |
| 10 | History of American Board Games | Philip Orbanes, Learning the Game 1898–1910 | 접근 불가 |
| 11 | Game, Play, Sport—Definitions; Playtest | David Parlett, Welcome Aboard | 접근 불가 |
| 12 | Game Lab (공식 표의 별도 세션 제목 없음) | Salen & Zimmerman, Games as Systems of Information | 접근 불가 |
| 13 | Cybernetics and Multiplayer | Costikyan & Davidson, The 3 Player Problem | 접근 불가 |
| 14 | Adding and Cutting Mechanics; Playtest | Challenges for Game Designers, ch.14 Adding and Subtracting Mechanics | 접근 불가 |
| 15 | Assignment 2 game due and presentation | Assignment 3 안내 시작 | 접근 불가 |
| 16 | Simulation and Assignment 3 | [과제 3 Perspective](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmentthre/); Gonzalo Frasca, Simulation 101 | 접근 불가 |
| 17 | Guest lecture: Game Makers Guild and Games By Playdate | 공식 진도표 | 접근 불가 |
| 18 | Guest lecture: Geneva University of Art and Design | 공식 진도표 | 접근 불가 |
| 19 | Space Control; Pitch and playtest | David Parlett, Space Control | 접근 불가 |
| 20 | Cooperative Games; Playtest | Cooperation and Engagement (외부 영상) | 접근 불가 |
| 21 | Social Play | Salen & Zimmerman, Games as Systems of Information | 접근 불가 |
| 22 | Changing Rules | Peter Olotka, Fair Isn’t Funny | 접근 불가 |
| 23 | De Koven / Changing Rules II | Bernard De Koven, Changing the Game | 접근 불가 |
| 24 | Indie Games; final playtest; guest Jesper Juul | 공식 진도표 | 접근 불가 |
| 25 | Final work session | 공식 진도표 | 접근 불가 |
| 26 | Final Presentations; changelogs/report due | 공식 진도표 | 접근 불가 |

정확한 오디오 파일별 제목은 [Audio Lectures](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/video_galleries/audio-lectures/)에 남아 있지만 **웹페이지에 접근 불가 안내가 있으므로 실제 재생 가능한 영상/오디오로 지정하지 않는다**. 강의계획표에는 1부 Game Mechanics, 2부 Meaningful Decisions in Gameplay, 4부 The MDA Framework 같은 녹음 제목이 있다. 수업 교재 [CGD], [GDW] 등의 정독 분량·열람 권한은 별도 확인이 필요하다. [608-C]

**공식 과제 원문** (모두 웹페이지에서 PDF 링크를 제공):
| 과제 | 실제 제목 | 정확한 위치 | 형태 |
|---|---|---|---|
| 1 | Single Mechanic Game | [원문 PDF 안내](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmentone/) | 텍스트/PDF |
| 2 | Experience and Aesthetics | [원문 PDF 안내](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmenttwo/) | 텍스트/PDF |
| 3 | Perspective | [원문 PDF 안내](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmentthre/) | 텍스트/PDF |

학생작품은 [Assignments and Student Work](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/assignments-and-student-work/)에서 선택한다. 공개본의 상당수는 게임의 규칙/설명서 PDF 형태이므로 **'학생 작품을 반드시 PC에서 플레이할 수 있다'는 기존 D5 기대는 보장되지 않는다**. 규칙서를 읽고 가능하면 최소 구성품으로 재현/테스트한다.

### A-2. MIT CMS.301 Introduction to Game Design Methods — 2016 봄

공식: [Syllabus](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/syllabus/) · [Calendar](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/calendar/) · [Readings](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/readings/) · [Assignments](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/). 공개 탐색 메뉴에 Lecture Videos 항목은 없다. [301-C][301-R][301-A]

| 주차 | 실제 수업(Session) 제목 | 해당 주차 읽기/활동 | 영상 |
|---|---|---|---|
| 1 | S1 Course Presentation; S2 Contexts of Play | Gaver et al. Design: Cultural Probes; Cultural Probes and the Value of Uncertainty | 없음 |
| 2 | S3 Crit Session 1; S4 The Building Blocks of Game Design | Antoine Bauza, Takenoko Rules; Takenoko - How To Play | 본강의 영상 없음; 외부 참고영상 별도 |
| 3 | S5 Gaming Session | 지정 읽기 없음 | 없음 |
| 4 | S6 Crit Session 2; S7 Design Process I | Buley, The User Experience Team of One ch.6; Design Process I Lecture Slides | 없음 |
| 5 | S8 Crit Session 3; S9 Design Process II | Challenges for Game Designers ch.1; How Brainwriting can Neutralize the Loudmouths | 없음 |
| 6 | S10 Crit Session 4; S11 Prototyping | Fullerton, Game Design Workshop ch.7 | 없음 |
| 7 | S12 Crit Session 5; S13 Playtesting | Playtesting Resources; Niedenthal, Real-time Sweetspot: The Multiple Meanings of Game Company Playtests | 없음 |
| 8 | S14 Crit Session 6; S15 Game Design Research | Fallman, The Interaction Design Research Triangle; Eladhari/Ollila, Design for Research Results | 없음 |
| 9 | S16 Gaming Session 1; S17 Gaming Session 2 | 지정 읽기 없음 | 없음 |
| 10 | S18 Crit Session 7: Concept; S19 Low Fidelity Prototyping | 지정 읽기 없음 | 없음 |
| 11 | S20 Crit Session 8: First Iteration Prototype | 지정 읽기 없음 | 없음 |
| 12 | S21 Gaming Session 3; S22 Cross Section Testing | 지정 읽기 없음 | 없음 |
| 13 | S23 Crit Session 9: Second Iteration Prototype; S24 Group Based Consultation | 지정 읽기 없음 | 없음 |
| 14 | S25 Final Presentations; S26 Final Presentations (cont.) | 지정 읽기 없음 | 없음 |

**8개 공식 과제 목록** ([원본 목록](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/)):
| 번호 | 공식 제목 | 연결 URL | 형식/길이 |
|---|---|---|---|
| 1 | People in My Life Through Games | [전체 과제 목록](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/) | PDF, 동영상 길이 해당 없음 |
| 2 | Board Game Analysis (Solution 포함) | [전체 과제 목록](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/) | PDF |
| 3 | Scrabbleship | [전체 과제 목록](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/) | PDF |
| 4 | Research | [전체 과제 목록](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/) | PDF |
| 5 | Game Design Document & Pitch | [과제 5 PDF](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment5/), [High Level Design Document Template](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_highlevel/) | PDF |
| 6 | Prototyping a Game | [과제 6 PDF](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment6/) | PDF |
| 7 | Playtest | [과제 7 PDF](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment7/) | PDF |
| 8 | Explorative Game Design Project, Steps 1–4 Overview | [과제 8 PDF](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment8/) | PDF; 4단계 발표·보고 지침 추가 있음 |

주의: 공개된 출처가 **과제 PDF**인 경우 '학습 영상 길이'는 해당 없음. 글 읽는 시간은 개인차가 커서 운영상 배정할 수 있을 뿐 출처가 알려주는 숫자가 아니다.

### A-3. MIT CMS.611J Creating Video Games — 2014 가을

공식: [Syllabus](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/syllabus/) · [Calendar](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/calendar/) · [Lecture Videos — 올바른 주소](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) · [Lecture Slides and Readings](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/lecture-slides-and-readings/). [611-V][611-S]

영상 아래의 시간은 **실제 확인된 재생시간**. 미확인은 원래 길이가 0이라는 뜻이 아니다.

| Session | 공식 동영상 제목(장별 실제 공개 내용) | 직접 URL/자료 | 실제 길이 |
|---|---|---|---|
| 1 | Introduction; Guest Pablo Suarez; Game Engines; Meaningful Decisions in Games | [Session 1](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-1-introduction/) | 미확인 |
| 2 | Project 1; Brainstorming and Low-Fidelity Prototyping | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | **1:10:16** [MIT Learn](https://learn.mit.edu/news/how-mit-open-learnings-opencourseware-is-fueling-one-learners-passion-for-learning?resource=10039&resource_title=game-mechanics-brainstorming) |
| 3 | Revision Control; Game Engines; Vision Statement | [Session 3](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-3-game-engines/) | **56:06** [MIT Learn](https://learn.mit.edu/video/10040/session-3-revision-control-game-engines-vision-statement?playlist=10037) |
| 4 | Project 2 Intro; Elevator Pitches; Digital Prototypes; Team Choice | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | **44:56** [MIT Learn](https://learn.mit.edu/video/10041/session-4-project-2-intro-project-2-elevator-pitches?playlist=10037) |
| 5 | Agile Software Development | [Session 5](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-5-agile-software-development/) | 미확인 |
| 6 | Agile Project Management | [Session 6](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-6-agile-project-management/) | **1:44:40** [MIT Learn](https://learn.mit.edu/video/10043/session-6-agile-project-management?playlist=10037) |
| 7 | Quality Assurance; Playtesting by Genevieve Conley; Focus Testing Results | [Session 7](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-7-testing-and-guest-lecture-with-genevieve-conley-of-riot-games/) | **1:22:08** [MIT Learn](https://learn.mit.edu/video/10044/session-7-quality-assurance-playtesting-by-genevieve-conley?playlist=10037) |
| 8 | Project 2 Presentations; Project 3; Digital Prototype with User Interference | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 9 | Guest Lecture – Hidetaka “SWERY” Suehiro | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | **56:53** [MIT Learn](https://learn.mit.edu/c/unit/see?resource=10046&resource_title=session-1-introduction-guest-pablo-suarez-red-cross-red) |
| 10 | Project 3 Check-In; UI and Usability | [Session 10](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-10-ui-and-usability/) | **1:28:29** [MIT Learn 검색 결과에서 확인](https://learn.mit.edu/) |
| 11 | Game Development and Best Practices by Tim Cowan | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 12 | Project 3 Presentations; Project 4 Topics; Project 4 Brainstorming | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 13 | Project 4 Planning and Team Formation; Serious Games | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 14 | Aesthetics | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 15 | Freedoms of Play; Project 4 Playtesting; Status Report | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 16 | Team Dynamics | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 17 | Working with Artists by Luigi Guatieri | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 18 | Fiction and Narrative in Video Games | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 19 | Working with Sound Designers by Richard Ludlow and Andy Forsberg | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 20 | Writing in Games by Heather Albano and Laura Baldwin | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 21 | Guest Lecture: Blizzard Entertainment | [Calendar](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/calendar/) | **영상 미공개** |
| 22 | Project 4 Check-in Presentations; Scope | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 23 | Project 4 Feedback; Team Discussions | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 24 | Running a Game Studio (Guest Lecture) | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 25 | Getting Players to Play Your Game by Sean Baptiste | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 26 | Final Presentation Rehearsal | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |
| 27 | Final Presentations | [동영상 목록](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | 미확인 |

공식 슬라이드/읽기 페이지의 주제별 **정확한 항목명**(동영상 아닌 자료): Introduction, Project 1 Introduction, Project 4 Introduction, Back of the Box, High Level Design Document, Choice and Conflict, Brainstorming, Paper Prototyping, Prototyping Map, Testing, Game Engines, Version Control, Coding Tips, Vision Statement, Agile Project Management, Agile Software Development, Team Dynamics. 전체 정확한 파일 위치는 [Lecture Slides and Readings](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/lecture-slides-and-readings/)에 있다. [611-S]

### A-4. K-MOOC 게임컨셉디자인(계명대학교)

[공식 강의 상세 및 강의계획서](https://www.kmooc.kr/view/course/detail/21313). 총 15주; 학습 인정 39시간 / **VOD 실제 합계 24시간 59분**. 2026년 10월 22일 기준 강좌 상단 현행 일정 2026-09-18~12-31 수강신청, 2026-10-18~2027-01-31 운영. 설명 본문에 **오래된 2025~2026년 일정이 함께 남아 있으므로** 페이지 하단 현행 모집 표기를 따른다. 한국어 강좌 및 한국어 자막이 공식 표기되어 있다. 공개 소개화면에서 개별 영상 길이·개별 공개 영상 URL은 미확인. [KM]

| 주차 | 주제 | 공식 차시명(차시번호는 각 주차에서 1-1, 1-2, 1-3으로 반복) | 차시별 실제 길이 |
|---|---|---|---|
| 1 | 게임 디자인이란? | 게임 디자인의 개념과 게임 디자이너가 하는 일 / 게임 기획에 대한 이해 / 게임 기획자가 되기 위해서 갖추어야 할 능력 | 미확인 |
| 2 | 컨셉의 정의와 국가별 컨셉기획서 | 컨셉의 의미 / 아이디어의 도출 방법 / 일본·북미·한국 국가별 컨셉기획서의 특징 | 미확인 |
| 3 | 게임 장르 분석 | 게임의 장르 구분 / 게임 장르의 핵심 요소 / 게임 장르별 기획 방식 | 미확인 |
| 4 | 게임 세계관 설정 | 세계관의 기본 개념 / 세계관의 주요 구성 요소 / 성공적인 게임 세계관 예시와 실습 | 미확인 |
| 5 | 캐릭터 설정 | 캐릭터의 개요 / 캐릭터 설계의 핵심 요소 / 캐릭터 설계의 기본 원칙 | 미확인 |
| 6 | 게임 매커니즘 설계 | 메카닉스와 매커니즘의 개요 / 시스템 규칙 기획 / 게임 구성 요인 설계 | 미확인 |
| 7 | 게임 스토리텔링 창작 | 서사 구조와 내러티브 구조 / 게임의 시나리오 전달 방식 / 게임 스토리텔링과 게임 시나리오 작성 | 미확인 |
| 8 | 게임 컨셉디자인 사례 | 게임 디자이너 커리어 1 / 커리어 2 / 커리어 3 | 미확인 |
| 9 | 레벨 디자인의 이해 | 레벨 디자인의 개요와 기본 개념 / 레벨 기획 및 초반 설계 / 공간의 유형과 내비게이션 기법 | 미확인 |
| 10 | UI/UX 이론과 게임 디자인 | UI/UX 개요 / UI/UX의 설계 방법 / 성공적인 UI와 UX 사례 | 미확인 |
| 11 | 플레이어 몰입과 게임 경험 | 몰입 이론의 개요 / 몰입감을 높이는 게임 설계 요소 / 플레이어 유형과 피로도를 고려한 게임 디자인 | 미확인 |
| 12 | 창의성과 아이디어 | 창의성과 아이디어 / 기확자를 위한 프로토타입(원문 표기) / 비디오게임과 게임 산업 | 미확인 |
| 13 | 새로운 게임 컨셉디자인을 위한 준비 | 게임 디자인의 시작 / 클래식과 장르의 중요성 / 비디오 게임의 구조 | 미확인 |
| 14 | 같힌 세계에서 열린 세계로의 게임의 확장(원문 표기) | 비디오 게임의 확장 / 아케이드 게임 너머 / 몰입의 시대, 게임의 진화 | 미확인 |
| 15 | 학생 기획서/게임 프로토타입 사례 | 학생 Prototypes1 / 학생 Prototypes / 학생 Prototypes + 기말과제 | 미확인 |

### A-5. 에듀코카 공개강의 4편: 확인 결과

| pSeq | 원래 plan.json의 제목(공식 사이트 제목 재검증 미완료) | 정확한 사용자 지정 URL | 실제 길이 | 상태 |
|---|---|---|---|---|
| 1044 | 장르에 대한 이해 | [상세 페이지](https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=1044) | **미확인** | 직접 페이지 조회 실패 |
| 1045 | 실시간 게임의 이해 — 이스 | [상세 페이지](https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=1045) | **미확인** | 직접 페이지 조회 실패 |
| 1046 | 턴방식 게임의 이해 — 히어로즈 오브 마이트 앤 매직 | [상세 페이지](https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=1046) | **미확인** | 직접 페이지 조회 실패 |
| 794 | 인디게임 제작 | [상세 페이지](https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=794) | **미확인** | 직접 페이지 조회 실패 |

오류가 발생했다는 사실만 확인했으므로 **삭제/폐강/로그인 필요/무료/실제 분량** 중 무엇이 원인인지 단정하지 않는다. 본인 브라우저에서 페이지를 열고 플레이어 재생 시간을 확인하기 전까지 필수 학습자료로 배정하지 않는 것을 권장한다. 사전 확인 실패 시 K-MOOC의 3주·6주·12주 강의와 MIT 과제 자료로 대체.

## B. 21일 계획 날짜별 정밀 매핑 (data/plan.json에 대한 패치 제안)

각 행의 **시간**은 기존 계획 시간(교재/영상의 길이가 아님). 실행 권고에서는 처음에 확정된 한 자료를 지정하고, 학습자료 확인에 시간을 소모하지 않게 했다. 복기·게임 분석 과제 자체는 원본 유지.

| 일차/날짜 | 기존 시간 | 정확히 열 자료 — 제목 및 URL | 권장 사용 분량과 확인 상태 | 결과물/메모 |
|---|---:|---|---|---|
| D1 10/23 | 75분 | [CMS.608 Syllabus](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/syllabus/), [CMS.608 Calendar S1~4](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/calendar/), [K-MOOC 1주 강의계획](https://www.kmooc.kr/view/course/detail/21313) | 문서 20+20분, 목차 확인 15분, 남은 20분 논의; **전부 비영상** | 강의 위치와 1회독 목표 지도 |
| D2 10/24 | 90분 | **기본:** [K-MOOC 6주 1-1 '메카닉스와 매커니즘의 개요'](https://www.kmooc.kr/view/course/detail/21313) + [CMS.608 Calendar S2 'Meaningful Decisions, Visibility'](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/calendar/). **영어 영상 옵션:** [CMS.611J Session 1 Meaningful Decisions](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-1-introduction/) | K-MOOC 차시 길이 **미확인**, 권장 30~45분만 시청; 문서 10분; 용어 정리/사례 20~30분. CMS.608 오디오 재생에 의존하지 않음 | 기계적 규칙과 의미 있는 선택을 실제 게임에서 1개씩 |
| D3 10/25 | 90분 | [CMS.608 Assignment 1: Single Mechanic Game](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmentone/) | 과제 PDF 10분(비영상); 게임 플레이 20분; 각자 분석 40분; 비교 20분 | A1: 아안 백지, 파이 학습지 |
| D4 10/26 | 75분 | [K-MOOC 3주 1-1 '게임의 장르 구분' + 3주 1-2 '게임 장르의 핵심 요소'](https://www.kmooc.kr/view/course/detail/21313) | 두 차시 실제 길이 **미확인**; 최대 45~50분 시청 + 25분 장르 비교. 길면 첫 차시만 우선 | 장르와 핵심 메커니즘 비교 |
| D5 10/27 | 75분 | [CMS.608 Assignment 2: Experience and Aesthetics](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/resources/mitcms_608s14_asigmenttwo/), [학생작품 목록](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/assignments-and-student-work/) | 과제 지시문 15분 + 작품 **규칙/설명서** 30분 + 실제 가능 여부 따라 규칙 시험/토론 30분; 모두 비영상 | 작품 디지털 플레이 가능 여부는 보장되지 않음 |
| D6 10/28 | 75분 | [CMS.608 Calendar S4 MDA](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/calendar/)에 연결된 [MDA: A Formal Approach to Game Design and Game Research (PDF)](https://www.cs.northwestern.edu/~hunicke/MDA.pdf) | MDA PDF 핵심 부분 10~15분(비영상); 분석게임 20분 + FigJam 분류/비교 40분 | A2: Mechanics → Dynamics → Aesthetics. **잼 복기 날짜와 충돌** |
| D7 10/29 | 75분 | [CMS.608 Calendar S1~9](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/calendar/) + [K-MOOC 1·3·6주 목차](https://www.kmooc.kr/view/course/detail/21313) | 두 목록의 **목차 재검토 20분** + 1주 지도 40분 + 상호 설명 15분 | 한 장 학습 지도; **이날 다음 잼 시작일과 충돌** |
| D8 10/30 | 75분 | [CMS.301 Calendar S1~15](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/calendar/) + [CMS.301 Assignments 1~8](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/) | Calendar 15분, 과제 목록 30분, 방법론 지도 30분(비영상) | 8개 과제 제목·관계도 |
| D9 10/31 | 90분(30분 최소판) | 원안: [에듀코카 1044 '장르에 대한 이해'](https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=1044); **검증된 대체:** [K-MOOC 3주 1-3 '게임 장르별 기획 방식'](https://www.kmooc.kr/view/course/detail/21313) | KOCCA 길이/접근 **미확인**. 대체 차시도 실제 길이 미확인, **시청 20분 내 + 10분 회상**을 최소판으로 편성 | 게임잼/개인 게임 마감 때문에 최소판 허용 |
| D10 11/01 | 90분 | **준비자료:** [K-MOOC 9주 1-1 '레벨 디자인의 개요와 기본 개념'](https://www.kmooc.kr/view/course/detail/21313) | 실제 길이 **미확인**; 자료 또는 이전 학습 개념 10분 + 게임 25분 + 시스템/레벨 분석 55분 | A3; **같은 날 게임잼 종료 및 복기 일정과 충돌** |
| D11 11/02 | 75분 | 원안: [KOCCA 1045 이스](https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=1045) 또는 [1046 히어로즈](https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=1046). **접근 실패 시 기본:** [K-MOOC 6주 1-2 '시스템 규칙 기획'](https://www.kmooc.kr/view/course/detail/21313) | KOCCA 두 영상 길이 **미확인**. K-MOOC 한 차시를 먼저 보고 20분 사례 비교; 총 75분 안에서 중단 | 실시간/턴제 차이 사례 2개 |
| D12 11/03 | 75분 | [Game Balance Concepts — Level 1: Intro to Game Balance](https://gamebalanceconcepts.wordpress.com/2010/07/07/level-1-intro-to-game-balance/) | 정확한 1주차 글 30~40분(비영상, **권장**); 두 게임 사례 비교/설명 35~45분 | 선택지의 비용/효용 한 쌍 분석 |
| D13 11/04 | 75분 | [K-MOOC 10주 1-1 UI/UX 개요 + 10주 1-2 UI/UX의 설계 방법](https://www.kmooc.kr/view/course/detail/21313), [Balance Concepts Level 1](https://gamebalanceconcepts.wordpress.com/2010/07/07/level-1-intro-to-game-balance/) | 차시별 영상 길이 **미확인**. 원안 분석에 집중: 지난 강의 메모 10분, 게임 20분, 분석 45분. K-MOOC는 사전/시간 여유 시 | A4 UI/UX·밸런스 |
| D14 11/05 | 75분 | [CMS.301 Assignment 5: Game Design Document & Pitch](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment5/), [High Level Design Document Template](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_highlevel/), [Assignment 6: Prototyping a Game](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment6/) | 세 PDF 각 10~15분 = 40분(비영상); 연결 관계/상호 설명 35분. 원안의 KOCCA 794는 접근 미확인이라 보조로만 | '기획 문서 → 프로토타입 → 검증' 흐름도 |
| D15 11/06 | 75분 | [CMS.301 Assignment 7: Playtest](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment7/) 및 [CMS.301 Readings Week 7](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/readings/) | 과제 PDF 20분 + 읽기 주제 20분 + 질문 초안 35분(운영 제안); **11/06 휴식일과 명백히 충돌 — 별도 재편성 필요** | 체크리스트/질문지. **휴식 원칙을 덮어쓰지 말 것** |
| D16 11/07 | 90분 | [CMS.611J Syllabus](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/syllabus/), [Calendar](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/calendar/), [Lecture Videos gallery](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) | Syllabus 20분 + Calendar 25분 + **목차** 25분 + 우리 팀 사례 정리 20분. 이날 영상 전체 시청 불필요 | 5개의 프로젝트 평가 항목과 현재 개발과정 비교 |
| D17 11/08 | 90분 | [CMS.301 Assignment 7: Playtest](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment7/) | 지침 재확인 10분, 첫 플레이 20분, 역할 교대 20분, 상호 관찰 정리 40분(비영상) | A5: 관찰/발언/해석 구별 |
| D18 11/09 | 75분 | [CMS.611J Session 7: Quality Assurance; Playtesting by Genevieve Conley; Focus Testing Results](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-7-testing-and-guest-lecture-with-genevieve-conley-of-riot-games/) + [Testing slides](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/lecture-slides-and-readings/) | **실제 전체 길이 1:22:08 > 75분**. 강의 전체를 필수화하지 말고 **Testing slides 20분 + 영상 중 플레이테스트 설명 부분 25~30분(정확한 시작/끝 시각 미확인) + D17 비교 25분** | 그날 본 부분·건너뛴 부분을 기록 |
| D19 11/10 | 75분 | **기본:** [CMS.611J Agile Project Management slides](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/lecture-slides-and-readings/) + [Session 6: Agile Project Management](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-6-agile-project-management/); **관련:** [Session 5: Agile Software Development](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/resources/lecture-5-agile-software-development/) | Session 6 **실제 1:44:40**로 75분 초과. **슬라이드 25분 + Session 6 선택 부분 20분(구간 미확인) + 우리 백로그 작성 30분** 권장 | 백로그와 당장 다음 1~3일 할 일 |
| D20 11/11 | 75분 | [CMS.301 Assignment 8: Explorative Game Design Project, Steps 1–4](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment8/) + [CMS.611J High Level Design Document](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/lecture-slides-and-readings/) | 과제·문서 구조 20분(비영상), 기존 게임에 적용 40분, 상호 평가 15분. KOCCA 794는 길이 미확인으로 제외 | A6 기존 게임의 목표·근거·개선 1쪽 |
| D21 11/12 | 75분 | [CMS.608 Calendar](https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/calendar/) + [CMS.301 Assignments](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/) + [CMS.611J Calendar](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/calendar/) | 공식 목차 대조 25분 + 전체 개념 지도 35분 + 다음 2회독 영역 지정 15분. 전부 비영상 | 완강 체크가 아니라 '강의별 위치를 아는가' 점검 |

### 중요한 변경 후보와 미확인 항목

1. **D2 CMS.608 영상**: 원본 계획에서 잘못 기대한 자료. K-MOOC 6주 1-1이나 CMS.611J Session 1로 보완. 오디오가 복구되었다는 증거가 나올 때까지 그 오디오를 필수로 배정하지 않음. [608-C][611-V]
2. **D16~19 CMS.611J 링크**: /pages/lecture-videos/가 아니라 [영상 갤러리](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/) 사용. 7번 82분, 6번 104분은 계획상 75분을 초과한다. [611-V]
3. **K-MOOC 접근**: 강의계획서는 로그인 없이 읽히지만 실제 각 차시 재생은 수강신청/로그인 상태에 따라 달라질 수 있다. 조사자가 개별 영상을 열고 길이를 확인하지 못했다. [KM]
4. **KOCCA**: 해당 네 상세 페이지의 **길이, 현재 운영, 제목 최신성 전부 미확인**. 수동 확인 전까지 계획에서 **선택적** 출처로 취급한다. [EDU]
5. **일정 충돌**: 프로젝트 공통 배경에 10/23~27 게임잼, 10/28 복기, 10/29~11/01 두 번째 잼, 11/01 복기, 11/06 휴식이 잡혀 있다. 반면 data/plan.json은 그 기간에 학습 D1~D15를 날짜 고정으로 배치한다. 이번 작업은 자료를 정밀 매핑하는 조사이므로 일정 자체를 무단 수정하지 않는다.

## C. 영어 자료 자막·한국어 대안

| 영어 원자료 | 한국어 자막 여부 | 바로 쓸 한국어 대체 | 동일성에 대한 주의 |
|---|---|---|---|
| MIT CMS.608 오디오 | **적용 불가(오디오 접근 불가)** | [K-MOOC 1주·3주·6주](https://www.kmooc.kr/view/course/detail/21313) | 비디오 복제가 아니라 주제 대응 |
| MIT CMS.301 수업/과제 PDF | 영상 없음. 문서의 공식 한국어 번역은 **미확인** | PDF 제목·목적을 한국어로 정리 + [K-MOOC 12주 프로토타입](https://www.kmooc.kr/view/course/detail/21313) | 공식 과제의 수행 기준과 한국어 강의는 다름 |
| MIT CMS.611J Session 1 의미 있는 선택 | 공식 한국어 자막 **미확인** | [K-MOOC 6주 1-1 메카닉스와 매커니즘의 개요](https://www.kmooc.kr/view/course/detail/21313) | Meaningful Decisions와 Mechanism 개념은 겹치지만 같지 않음 |
| MIT CMS.611J Session 7 테스트 | 공식 한국어 자막 **미확인** | [CMS.301 과제 7 Playtest](https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/resources/mitcms_301s16_assigment7/) 지시문을 번역해 사용 | 영어 읽기 회피에는 도움이 되지만 한국어 음성 강의 대체는 아님 |
| MIT CMS.611J Session 10 UI/Usability | 공식 한국어 자막 **미확인** | [K-MOOC 10주 1-1/1-2/1-3](https://www.kmooc.kr/view/course/detail/21313) | UI/UX 내용 대응 |
| MIT CMS.611J Session 6 Agile PM | 공식 한국어 자막 **미확인** | [CMS.611J Agile Project Management slides](https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/lecture-slides-and-readings/)의 항목을 한국어로 번역·팀 백로그 실습 | 슬라이드도 영어이므로 별도 번역 필요 |
| MDA 논문 | 한국어 공식 번역 **미확인** | [원문 MDA PDF](https://www.cs.northwestern.edu/~hunicke/MDA.pdf)에서 세 용어 중심 부분만 한국어로 요약하여 분석 보드에 사용 | MDA 개념과 K-MOOC 메커니즘 차시는 1:1 대응하지 않음 |

MIT OCW 영상 상세 페이지에서 영어 Transcript·영어 자막 관련 UI를 볼 수 있으나, **한국어 자막 제공 사실은 검증하지 못했다**. 브라우저에서 자동번역/자막 확장 기능을 쓸 수 있더라도 이는 MIT의 공식 한국어 자막 제공과 구분할 것. 영어 영상의 실제 분량이 75분을 넘는 날은 자막 유무와 관계없이 **전체 시청 필수**로 지정하지 않는다.

## D. 바로 옮길 운영 규칙 (매니저용)

- **학습자(아안/파이), 공부 시작 2분:** 오늘 볼 자료를 열기 전에 이전 회차 개념 하나를 각자 무자료로 말함. 오늘 지정한 제목과 링크 하나만 열어 자료찾기 시간을 줄인다.
- **학습자, 30~45분:** 원문이 길면 **정해 둔 '주제' 부분만** 보고 종료. 영상 전체 시청률과 실제 학습 완료를 구분한다. 아직 영상 구간 시작·끝을 확인하지 못한 경우 임의 타임스탬프를 찍지 않는다.
- **자료 열람 후 10분:** 각자 '원문 주장 1개 / 게임에서 보인 사례 1개 / 검증할 의문 1개' 기록. 단순 요약만으로 통과 처리하지 않는다.
- **분석날(아안 백지, 파이 학습지):** 원안 20~30분 플레이를 우선하고, 강의는 지난 회차에서 배운 원리를 *적용*하기 위한 짧은 사전 자료로만 사용한다.
- **KOCCA 강의가 열리지 않으면:** 즉시 위 매핑의 K-MOOC 대체 차시로 전환. KOCCA 자체를 확인하지 못했으면 제목·영상 길이·수강 방식에 **미확인** 라벨을 유지한다.
- **1회독 성공 기준:** 21일 학습 종료 시 강좌/과제 목록을 구분하고, 자신이 적용한 개념이 **어떤 공식 자료의 어느 회차인지** 추적할 수 있으면 성공. 15주 K-MOOC 45차시와 MIT 세 강좌의 전 자료 완주는 요구하지 않는다.

## 원문 출처 (모두 2026-10-22 조회)

- [608-C] MIT CMS.608 **Calendar** — 목차 26회, 읽기, 오디오 미제공 안내: https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/calendar/
- [608-A] MIT CMS.608 **Assignments and Student Work** — 과제 3개/학생작품: https://ocw.mit.edu/courses/cms-608-game-design-spring-2014/pages/assignments-and-student-work/
- [301-C] MIT CMS.301 **Calendar** — 26회 수업/14주: https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/calendar/
- [301-R] MIT CMS.301 **Readings** — 주별 읽기 목록: https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/readings/
- [301-A] MIT CMS.301 **Assignments** — 과제 8개: https://ocw.mit.edu/courses/cms-301-introduction-to-game-design-methods-spring-2016/pages/assignments/
- [611-V] MIT CMS.611J **Lecture Videos** — 공식 영상 전체 목록/누락 세션21: https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/video_galleries/lecture-videos/
- [611-S] MIT CMS.611J **Lecture Slides and Readings** — 주제별 PDF와 참고 읽기: https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/lecture-slides-and-readings/
- [611-C] MIT CMS.611J **Calendar** — 프로젝트·스프린트 일정: https://ocw.mit.edu/courses/cms-611j-creating-video-games-fall-2014/pages/calendar/
- [611-T] MIT Learn, Session 6 공식 재생시간 1:44:40: https://learn.mit.edu/video/10043/session-6-agile-project-management?playlist=10037
- [611-T2] MIT Learn, Session 7 공식 재생시간 1:22:08: https://learn.mit.edu/video/10044/session-7-quality-assurance-playtesting-by-genevieve-conley?playlist=10037
- [KM] K-MOOC 계명대 게임컨셉디자인 **강의계획서** — 15주 차시명/공식 운영 기간/전체 영상 시간: https://www.kmooc.kr/view/course/detail/21313
- [EDU] 에듀코카 지정 강의 상세 URL 4개 — 직접 조회 실패, 시간 미확인: https://edu.kocca.kr/edu/onlineEdu/openLecture/view.do?menuNo=500085&pSeq=1044 (pSeq 1045, 1046, 794 동일 양식)
- Game Balance Concepts, **Level 1: Intro to Game Balance**: https://gamebalanceconcepts.wordpress.com/2010/07/07/level-1-intro-to-game-balance/
