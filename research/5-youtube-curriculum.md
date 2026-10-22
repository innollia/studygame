# 리서치 05 — 파이의 유튜브 학습 커리큘럼

- 조사일: 2026-10-22
- 프로젝트: innollia/studygame
- 원 질문: [research/prompts.md — 5번](https://github.com/innollia/studygame/blob/main/research/prompts.md)
- 대상: 아안·파이의 게임기획 독학 중 **파이의 학교 시간 유튜브 학습**
- 주의: 영상 속 정보의 옳고 그름까지 실험 검증한 문서는 아니다. 채널 존재·영상 제목·업로드 기록과 학습 효용에 대한 **운영 판단을 구별**한다.

## 핵심 결론 5줄

1. **게임디자인 영상 → 본인이 직접 해 본 게임 장면과 비교**를 주축으로 하고, 구현 튜토리얼은 그 장치의 작동 이유를 이해하는 데 보조적으로 사용한다. 프로젝트의 '분석 우선' 목표에 맞춘 운영 제안이다.
2. 한국어로 UI와 Git 등 기본 어휘를 쌓고, 영어 Game Maker's Toolkit·Design Doc로 서로 다른 게임에서 공통 설계 원리를 찾는다.
3. 능동 시청의 최소 단위는 **자료를 닫고 핵심 주장 1개를 복원 → 실제 장면에서 근거 1개 확인 → 의문 1개 적기**다. 영상 도중 짧은 기억 검사의 학습상 이점에는 실험 근거가 있다.[R1][R2]
4. 매일 '깊게 보기' 1편 + '빠르게 훑기' 1~2편을 기본값으로 권고하지만 **최적 영상 수가 실험으로 입증된 것은 아니다**. 잼 기간에는 깊게 보기조차 생략 가능하다.
5. 2026년 업로드가 확인되는 채널과 그렇지 않은 채널을 나누어 쓴다. 갱신이 느린 좋은 기초 영상은 여전히 쓸 수 있지만, **AI 모델·가격·엔진 버전 정보는 원문 날짜와 공식 문서로 다시 확인**해야 한다.

## (a) 분야별 추천 채널·재생목록

표의 '활동'은 2026-10-22에 웹으로 확인 가능한 가장 최근의 **확인된 업로드 예시**이며, 반드시 실제 최종 업로드 날짜라는 뜻은 아니다. '미확인'을 최신 업로드가 없었다는 뜻으로 읽지 말 것. 난이도는 **파이에게 권장하는 시작 난이도**다. 구독자 수는 선발 기준에서 배제했다.

| 분야 | 채널·채널 주소 / 재생목록 | 언어 · 난이도 | 왜 보는가 / 처음 볼 영상 1개 | 2026년 활동 확인 |
|---|---|---|---|---|
| 게임개발 | [골드메탈](https://www.youtube.com/@goldmetal) · [Unity 입문 재생목록](https://www.youtube.com/playlist?list=PLO-mt5Iu5TeZa9dsqMVvXuSfVxwR_2AOz) | 한 · 초급 | Unity 오브젝트/스크립트와 입력·충돌·UI를 **순서대로** 익히기. 첫 영상: [2D 플랫포머 시리즈 시작](https://youtu.be/v_Y5FH_tCpc). 버전이 오래되었을 가능성에 유의.[C1] | **미확인**: 2026년에도 채널은 조회되지만 2026년 신규 강좌 게시일을 확인하지 못함.[C2] |
| 게임개발 | [Brackeys](https://www.youtube.com/@Brackeys) | 영 · 초급 | Godot에서 조작·적·점수·사운드·내보내기가 어떻게 연결되는지 전체 구조 보기. 첫 영상: [How to make a Video Game — Godot Beginner Tutorial](https://www.youtube.com/watch?v=LOhfqjmasi0) (77분, 필요한 구간만).[C3] | **확인**: 2026-01-18 Godot VFX, 2026-09-23 게임잼 작품 소개.[C4] |
| 게임개발 | [GDQuest](https://www.youtube.com/@Gdquest) · [공식 무료 입문 과정](https://www.gdquest.com/tutorial/godot/2d/first-2d-game-godot-4/) | 영 · 초~중 | Godot 프로젝트가 게임 루프로 완성되는 과정을 더 상세히 본다. 첫 영상: [Your First 2D Game From Zero in Godot 4](https://www.youtube.com/watch?v=GwCiGixlqiU). 공식 Godot 문서에서도 초보용 자료로 언급.[C5] | **미확인**: 2026년 채널 신규 업로드 날짜는 확인되지 않음. 확인된 입문 영상은 2023년 제작.[C5] |
| 게임디자인 | [Game Maker's Toolkit](https://www.youtube.com/@gmtk) | 영 · 초~중 | 선택·규칙·레벨·프로토타입을 **왜** 설계하는지 추적. 첫 영상: [Game Dev 101 — Where do game ideas come from?](https://www.youtube.com/watch?v=0m60QbT85Tc). 게임 한 장면을 근거로 주장하는 구성 자체가 분석의 모델.[C6] | **확인**: 2026-07-06 게임잼 관련 장편 등 2026년 게시 기록.[C7] |
| 게임디자인 | [Design Doc](https://www.youtube.com/@DesignDoc) | 영 · 초~중 | 사례를 여러 게임에서 비교해 **좋은/나쁜 디자인을 구분하는 기준** 배우기. 첫 영상: [Great and Terrible UX Design in Games](https://www.youtube.com/watch?v=o86rWZlF30g) (2026-03-31). UI/UX 영역에도 연결.[C8] | **확인**: 2026-03-31 업로드.[C8] |
| UI/UX | [디자인베이스](https://www.youtube.com/@designbase) | 한 · 초급 | UI 화면 구성과 프로토타이핑 도구 문법 익히기. 첫 영상: [2026 피그마 최신 강의 — 입문 1-1](https://www.youtube.com/watch?v=1Sqzinh-Loc) (2026-08-07). **피그마를 쓰는 법과 게임 HUD를 평가하는 법은 다름**을 구분.[C9] | **확인**: 2026-08-07 업로드.[C9] |
| UI/UX | [Nielsen Norman Group (NNgroup)](https://www.youtube.com/@NNgroup) | 영 · 중 | 인터페이스를 사람에게 테스트하고 관찰·해석하는 방법 학습. 첫 영상: [Common mistakes in usability testing](https://www.youtube.com/watch?v=LKaCtvvhbcg). 웹·서비스 중심이므로 게임 UX에 옮길 때 검증 필요.[C10] | **확인**: 연구기관 사이트에 2026-10-19 UX 영상 및 여러 2026년 영상 게시.[C11] |
| UI/UX | [Figma 공식](https://www.youtube.com/@Figma) | 영 · 초급 | 컴포넌트·화면 구조·프로토타입 제작을 도구 공식 설명으로 학습. 첫 영상: [Figma Design for beginners 1/13](https://www.youtube.com/watch?v=zzhSFobLkYw) (2025-07-28). 화면 버튼 UI와 HUD 시안을 직접 비교할 때만 우선순위 높음.[C12] | **2026 업로드 미확인**: 확인된 공식 입문 콘텐츠는 2025년.[C12] |
| 개발자 범용지식 | [얄팍한 코딩사전](https://www.youtube.com/@yalco-coding) | 한 · 초급 | Git의 저장·되돌리기·브랜치·충돌 해결처럼 2인 게임개발에 곧바로 필요한 공통 언어. 첫 영상: [2026 Git & GitHub 기초](https://www.youtube.com/watch?v=GWNkIeVtlpI) (2시간 10분; **부분 시청**).[C13] | **확인**: 2026-06-11 Git 강의, 2026-10-15 업로드 기록.[C13][C14] |
| 개발자 범용지식 | [CS50 (Harvard)](https://www.youtube.com/@cs50) · [2026 공식 목차](https://cs50.harvard.edu/x/) | 영 · 초~중 | 자료구조·알고리즘의 개념과 추상화 훈련. 첫 영상: [CS50x 2026 Lecture 5 — Data Structures](https://www.youtube.com/watch?v=PmAI76OGE_E). **초심자라면 먼저 공식 Week 0**을 보는 편이 적절; Lecture 5는 이후 참고용.[C15] | **확인**: 2026-01-01 강의 영상, 2026 공식 과정 개설.[C15] |
| 개발·기술 교양 | [코딩애플](https://www.youtube.com/@codingapple) | 한 · 초급 | 개발·AI·보안 개념을 짧게 접하는 탐색용. 첫 영상: [토큰이 비싸서 화난 개발자들이 하는 짓](https://ranktube.co.kr/video/2-3F7y5AKJw) (2026-07-29, 통계/영상 안내). 다만 **이 채널의 기술 뉴스 영상은 독립 검증 전에는 학습 사실로 암기하지 않음**.[C16] | **확인**: 2026-10-16 업로드까지 확인.[C17] |
| AI 개발·도구 | [Hugging Face](https://www.youtube.com/@HuggingFace) · [Post-training Agents 재생목록](https://www.youtube.com/playlist?list=PLo2EIpI_JMQvQZm-kVlz4wY1vWF0LBcf5) | 영 · 중~상 | '코딩 에이전트가 모델과 도구를 어떻게 연결하는가' 같은 구조적 지식을 얻는 심화 자료. 첫 영상: [Training Agents 1 — fine-tune a coding agent](https://www.youtube.com/watch?v=rNgUoH7Wbv8). **기초 AI 트렌드 입문용은 아님**.[C18] | **확인**: 2026-10-20 게시된 Hugging Face 정리글에서 이 시리즈를 안내.[C18] |
| AI 기술 동향 | [AI Explained](https://www.youtube.com/@aiexplained-official) | 영 · 중 | 신모델의 주장·성능·한계를 논문/공식 발표와 대조하는 탐색 출처. 첫 영상: [2026-01-28 모델·자동화 전망 해설](https://www.youtube.com/watch?v=Iar4yweKGoI). 미래 예측은 **영상 제작자의 해석**으로만 취급.[C19] | **확인**: 2026-01-28 영상, 2026-10-01 신규 소식 기록.[C19][C20] |

### 우선순위와 빼야 할 것

- **필수 축**: Game Maker's Toolkit → Design Doc → NNgroup. 첫 Deepest Sword 분석의 '맵 반복', '체크포인트', '사운드·클릭 피드백'을 여러 게임의 사례와 비교하기 좋다.
- **기초 보완**: Git이 낯설다면 얄팍한 코딩사전 → Godot라면 Brackeys 또는 GDQuest, Unity라면 골드메탈. **엔진 하나를 선택**해 과제 없이 두 엔진을 동시에 장시간 따라 하지 않는다.
- **도구 보완**: Figma가 필요할 때 디자인베이스; UI 분석은 Design Doc·NNgroup에서 먼저 생각할 문제를 얻는다.
- **뉴스/발견**: 코딩애플·AI Explained는 탐색용. Hugging Face의 훈련 심화 과정은 당장 알 필요가 없는 세부 구현까지 학습 범위를 넓힐 수 있으니 2회독 이후 선택 과제로 둔다.
- 강의 제목·업로드의 최신성이 **정보의 정확성을 보장하지 않는다**. 영상에 등장한 가격, 제품 지원 기능, 벤치마크 수치는 공식 발표를 다시 확인한다.

## (b) 학교 시간에 짧게 끊어 보고 능동적으로 시청하는 법

### 왜 그냥 보기만 해서는 부족한가

- Dunlosky 등(2013)의 광범위한 학습기법 리뷰에서 **인출 연습과 간격을 두고 다시 공부하기는 높은 유용성**을 평가받았다. 단순 재독과 밑줄은 낮은 유용성으로 평가됐다. 이는 유튜브 게임디자인 영상만을 시험한 결과는 아니다.[R1]
- Szpunar 등(2013)은 온라인 강의 중간에 짧은 기억 검사를 배치한 실험에서 주의 이탈 감소·학습 향상을 보고했다. 단순 시청 대신 '보고 → 닫고 → 꺼내기'를 쓰는 직접적 근거다.[R2]
- Brame(2016)은 교육용 영상 설계에서 인지 부하·참여·능동학습을 함께 고려하라고 권한다.[R3]
- Guo 등(2014)의 대규모 MOOC 분석에서 짧은 영상은 **시청 참여(engagement)**가 높았다. 이를 '6분 이하만 보면 장기 학습이 최적'이라는 뜻으로 바꾸면 안 된다.[R4]
- 영상 요약 3줄, 특정 하루 편수, 아래 시간표 자체는 **연구에서 검증한 최적 처방이 아닌 이 프로젝트의 실행 규칙**이다.

### 학교에서 45분 확보한 날 — 기본안

| 구간 | 파이가 할 일 | 남는 결과 |
|---|---|---|
| 0~8분 | 가벼운 탐색 영상 1개. 이해할 용어와 모르는 용어 분리 | '오늘 더 볼 질문' 한 줄 |
| 8~28분 | 핵심 영상 1개를 구간별로 시청. 영상 중간에 30초 멈춰 방금 배운 원리 꺼내기 | 주장과 근거 각각 한 줄 |
| 28~36분 | 다른 게임의 특정 장면을 떠올려 **배운 원리가 통하는지/안 통하는지** 적기. 실제 장면을 못 떠올리면 '검증 필요' 기록 | 적용/반례 한 줄 |
| 36~41분 | 두 번째 짧은 탐색 영상 또는 첫 영상의 핵심 구간 재검토 | 새로운 사실이 있으면 1개 추가 |
| 41~45분 | 디스코드용 시청 카드 게시. 막힌 부분 한 줄 | 링크, 3줄, 적용 1개 |

**짧은 날 15분**: 핵심 영상 8분(필요한 구간) + 자료 없이 2분 회상 + 실제 게임 연결 3분 + 기록 2분.

**긴 날 75분**: 기본안 45분을 먼저 완료하고, 나머지 30분은 관심 주제의 서로 다른 설명 2개를 비교하거나 깊게 본 영상의 남은 분량 시청. 자동 재생으로 채우지 않는다.

**영상이 60~120분이라도 1편을 한 번에 끝낼 의무가 없다.** 자막과 편집된 구간별로 주제를 끊는다. 브라키스 영상 전체를 보기보다 '플레이어 이동'·'사운드'처럼 당시 분석 주제에 해당하는 장만 먼저 본다.

### Deepest Sword 첫 회차와 연결할 예시

- Game Maker's Toolkit에서 '아이디어/메커니즘'을 본 날: **검이 길어지면 같은 길을 지나가는 선택이 어떻게 바뀌는가?** 영상에서 말한 '기존 장치를 변형해 게임을 만드는 방법'과 비교한다. 이것은 *적용 과제*이며 영상이 Deepest Sword를 직접 다뤘다는 주장이 아니다.
- Design Doc에서 UX 사례를 본 날: **체크포인트가 불필요한 재시도를 줄였다는 근거**와 다른 게임의 대조 사례를 찾는다. 자신의 플레이 경험과 추론을 분리한다.
- NNgroup에서 테스트 진행 방법을 본 날: **대상을 유도하는 질문 없이** '어떤 버튼을 누르려고 했는가'부터 관찰하도록 제안한다. 웹 UX 실험을 게임에 적용하는 것은 추가 검증이 필요하다.

## (c) 디스코드 기록 양식

학교 시간용 4~6줄. **깊게 본 영상에만 의무적으로 작성**하고, 훑은 영상은 제목/링크만 보관한다.

> **#파이-유튜브 · 2026-10-23**
>
> **깊게 본 영상:** 제목 + URL (실제로 본 00:00~00:00)  
> **1. 주장:** 영상이 설명하는 핵심 원리 1개  
> **2. 근거:** 영상 속 장면/데이터 1개 (없으면 '근거 제시 없음')  
> **3. 의문:** 다른 설명 또는 반례 1개 (없으면 '아직 모름')  
> **내 게임 적용:** 우리가 만든 게임/분석한 게임의 장면 1개 + 검증할 행동  
> **훑어본 영상:** 제목 + URL 1~2개 (없으면 생략)

구분: **영상에서 확인 / 내 해석 / 아직 검증 안 됨**. 본인이 정말 이해했는지는 이틀 뒤 영상 없이 같은 개념을 다른 게임에 다시 적용할 때 판정한다.

### 아안·매니저와 공유할 때

- **파이**: 평일 학교 여유 시간에 영상 기록 1카드. 바쁘면 '짧은 날'로 축소, 잼 날에는 기록 의무 없음.
- **아안**: 함께 하는 시간 중 주 2회, 파이 카드에서 1개를 골라 **어떤 화면/행동이 근거인지** 3분 질문한다. 시험처럼 몰아붙이거나 정답을 먼저 주지 않는다.
- **매니저**: 파이의 답변을 **관찰/추론/검증 계획**으로 나눠 한 번 피드백한다. 단순 영상 개수는 학습 점수에 반영하지 않는다.
- **두 사람**: 다음 게임 분석 회차에서 지난 영상의 원리 하나를 **다른 게임에 적용**한다. 처음 5분 자료 없이 기억해보고 필요 시 원본과 대조한다.

## (d) '최대한 많이 보기'와 깊이의 균형

| 방식 | 추천 역할 | 위험과 보완 |
|---|---|---|
| **탐색**: 5~10분 또는 긴 영상 일부 | 새로운 용어·도구·뉴스 발견, 모르는 영역 찾기 | 쇼츠·기술 뉴스만 이어 보면 아는 느낌이 커짐. 그날의 깊게 볼 주제로 연결 |
| **깊게 보기**: 한 주제당 15~25분 | 설명 근거를 이해하고 게임 장면에 적용 | 본 뒤 자료 없이 원리 복원. 어렵다면 완성된 예시부터 다시 |
| **비교**: 비슷한 주제 영상 2편 | 서로 다른 설계 원리/주장의 충돌 찾기 | 입문 개념이 없는 상황에서 대조 영상부터 무작정 늘리지 않기 |
| **실습/검증**: 5~20분 | 실제 UI 화면·게임 동작과 맞는지 확인 | 게임을 AI로 고치기만 하고 '왜'를 남기지 않는 패턴 피하기 |

**운영 기본값:** 학교에서 확보한 **학습 가능 시간 45분 기준, 2~3편/일(깊이 1, 탐색 1~2)**. 이 숫자는 연구 근거를 갖춘 '적정량'이 아니라 과제의 지속성을 고려한 시작점이며, 장편일 경우 **부분 시청도 한 세션**으로 센다. 일주일 운영 후 과부하, 실제 기억/적용률을 근거로 증감한다.

**게임잼(10/23~27, 10/29~11/1):** 유튜브는 막힌 작업을 해결하는 5~15분짜리 필요한 부분만. 필요 없는 트렌드 소비는 중단.

**복기(10/28, 11/1):** 잼에서 발생한 실수와 연결되는 학습 영상 하나를 선택하고 '영상의 원리가 우리 게임의 어느 문제를 설명하는가?'를 기록. **11/6은 쉬는 날**이므로 시청 의무를 배정하지 않는다.

### 첫 2주 분야 순환 예시(학교 시간 기준, 제안)

| 날짜 | 우선 시청 | 연결 과제 |
|---|---|---|
| 10/23 금 (잼) | 필요 시 Brackeys/골드메탈 특정 구현 구간 | 당장 막힌 원인 1개만 해결 |
| 10/26 월 (잼) | 필수 시청 없음 | 게임 제작 결정 한 줄이면 충분 |
| 10/28 수 (복기) | Design Doc UX | 이번 잼에서 플레이어가 막힌 순간 하나 해석 |
| 10/29 목 (잼) | 필요 시 얄코 Git 충돌 부분 | 협업 문제 발생 시만 |
| 10/30 금 (잼) | 필수 시청 없음 | 잠깐 테스트만 |
| 11/02 월 | Game Maker's Toolkit | 게임의 중심 선택과 대가 1개 |
| 11/03 화 | 디자인베이스 | 게임 UI 화면에서 정보 우선순위 점검 |
| 11/04 수 | NNgroup | 관찰 질문과 유도 질문 차이 |
| 11/05 목 | 얄팍한 코딩사전 | Git 저장·브랜치·충돌 개념 |
| 11/06 금 (휴식) | **의무 없음** | 자율 휴식 |

나머지 날은 프로젝트의 공식 21일 커리큘럼을 우선하고 YouTube는 **병행 수업**으로 다룬다. 학교 시간이 시험·수행평가로 줄어들면 **과제량을 자동 축소**한다.

## 채널 선택을 평가하는 5개 질문

1. **사실 근거**: 영상이 실제 플레이 장면/코드/데이터와 원본 출처를 보여 주는가?
2. **원리 설명**: '이렇게 하면 된다'를 넘어 왜 그런지 말하는가?
3. **검증 가능성**: 파이가 다른 게임이나 자신의 프로젝트에서 확인할 수 있는가?
4. **초보 적합성**: 어려운 단어를 설명하고, 재현 가능한 단계가 있는가?
5. **최신성**: 엔진 버전·AI 기능 같은 빠른 정보가 현재 공식 문서와 일치하는가?

구독자 수, 쇼츠 조회수, 편집 재미는 이 평가를 대신하지 않는다. 이러한 5개 기준은 연구에 직접 등장하는 표준 척도가 아니라 **본 프로젝트의 채널 선택 루브릭 제안**이다.

---

## 출처

### 학습법 원문
- **[R1]** Dunlosky et al. (2013), *Improving Students' Learning With Effective Learning Techniques*. https://doi.org/10.1177/1529100612453266
- **[R2]** Szpunar, Khan & Schacter (2013), *Interpolated memory tests reduce mind wandering and improve learning of online lectures*, PNAS. https://pmc.ncbi.nlm.nih.gov/articles/PMC3631699/
- **[R3]** Cynthia Brame (2016), *Effective Educational Videos: Principles and Guidelines*. https://doi.org/10.1187/cbe.16-03-0125
- **[R4]** Guo, Kim & Rubin (2014), *How video production affects student engagement*. https://doi.org/10.1145/2556325.2566239

### 채널·영상 검증
- **[C1]** 골드메탈 Unity 기초 재생목록 소개(과거 교육 콘텐츠): https://ojh0616.tistory.com/entry/%EA%B3%A8%EB%93%9C%EB%A9%94%ED%83%88-%EA%B0%95%EC%9D%98 ; 시리즈 첫 영상 링크 안내: https://dolearn.ai/learning2/watch_video?uid=GHUJMXtHKL0
- **[C2]** 골드메탈 채널 집계(2026-10-19 기준): https://www.socialerus.com/Kr/YouTube/Channel/UCw_N-Q_eYJo-IJFbNkhiYDA
- **[C3]** Brackeys 첫 Godot 입문 영상(2024-04-28): https://www.youtube.com/watch?v=LOhfqjmasi0
- **[C4]** Brackeys 최근 업로드 연혁: https://www.chronotube.com/channels/UCYbK_tjZ2OrIZFBvU6CCMiA
- **[C5]** Godot 공식 추천 자료와 GDQuest 공식 프로젝트: https://docs.godotengine.org/en/stable/community/tutorials.html ; https://www.gdquest.com/tutorial/godot/2d/first-2d-game-godot-4/
- **[C6]** GMTK Game Dev 101 영상: https://www.youtube.com/watch?v=0m60QbT85Tc
- **[C7]** GMTK 최근 업로드 연혁: https://www.chronotube.com/channels/UCqJ-Xo29CKyLTjn6z2XwYAw
- **[C8]** Design Doc 2026-03-31 UX 분석 영상: https://www.youtube.com/watch?v=o86rWZlF30g
- **[C9]** 디자인베이스 2026-08-07 Figma 입문: https://www.youtube.com/watch?v=1Sqzinh-Loc
- **[C10]** NNgroup 사용성 테스트 진행 실수: https://www.youtube.com/watch?v=LKaCtvvhbcg
- **[C11]** Nielsen Norman Group 최신 게시 동영상 모음: https://www.nngroup.com/articles/?asset=videos
- **[C12]** Figma 2025 공식 입문 영상: https://www.youtube.com/watch?v=zzhSFobLkYw
- **[C13]** 얄팍한 코딩사전 2026-06-11 Git: https://www.youtube.com/watch?v=GWNkIeVtlpI
- **[C14]** 얄팍한 코딩사전 2026-10-15 최근 영상 기록: https://creatorafterwork.com/channel/UC2nkWbaJt1KQDi2r2XclzTQ/videos/
- **[C15]** CS50 2026 공식 커리큘럼: https://cs50.harvard.edu/x/ ; 영상: https://www.youtube.com/watch?v=PmAI76OGE_E
- **[C16]** 코딩애플 예시 2026-07-29 영상: https://ranktube.co.kr/video/2-3F7y5AKJw
- **[C17]** 코딩애플 2026-10 업로드 목록: https://ranktube.co.kr/channel/UCSLrpBAzr-ROVGHQ5EmxnUg
- **[C18]** Hugging Face 2026-10-20 에이전트 훈련 영상·재생목록 공식 안내: https://huggingface.co/blog/huggingface/train-agents
- **[C19]** AI Explained 2026-01-28 업로드: https://www.youtube.com/watch?v=Iar4yweKGoI
- **[C20]** AI Explained 2026-10-01 최근 영상 기록: https://tarronkayaua.github.io/aua-ai-hub/news/videos/

**확인 한계:** 전체 2026년 업로드 이력을 YouTube API로 일괄 전수조사하지 않았다. 위에 명시한 '확인'은 인용한 영상/공개 기록의 날짜에 한정한다. 일부 영상의 한국어 자막 지원 여부는 확인하지 못했으므로 영어 영상은 자막을 전제로 한 필수 과제로 지정하지 않는다.