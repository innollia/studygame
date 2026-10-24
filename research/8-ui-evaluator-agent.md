# 리서치 08 — 게임 UI/UX 평가 서브에이전트 설계 (2026-10-24)

외부 조사 에이전트의 결과를 매니저가 요약해 저장했다. 원문은 6-2절(서브에이전트 초안) 중간에서 잘려서 왔다. 그래서 학습 루브릭, 블라인드 비교 절차, 검증 계획은 원문이 아니라 매니저가 프롬프트 요구에 맞춰 보충했다(.claude/agents/game-ui-critic.md, eval-cases/README.md). 인용 링크는 원문 그대로다.

## 핵심 결론 5줄 (원문)
1. 추천 구성은 C안: 단일 평가 에이전트 + 관점별 순차 검사 + 근거 검증 패스. 여러 전문 에이전트를 병렬로 돌리는 것이 낫다는 근거는 확인되지 않았다.
2. 게임 UI는 Nielsen 일반 휴리스틱만으로 부족하다. 게임 고유의 조작, 상태 전달, 학습, 몰입, 접근성을 함께 봐야 한다.
3. AI의 UI 평가 능력은 실제로 확인됐지만 전문가 대체 수준인지는 불확실하다. 전문가가 찾은 문제의 21.2%만 찾은 연구(Guerino 외 2025)와 기준 문제의 73~77%를 찾은 연구(Zhong 외 2025)가 함께 있다.
4. 스크린샷, 영상, 직접 플레이는 평가할 수 있는 범위가 다르다. 스크린샷으로 조작 반응이나 재미를 단정하지 못하게 하는 것이 핵심 설계 조건이다.
5. 학습용에서는 AI 평가를 정답이 아니라 "세 번째 평가"로 다룬다. 학생 독립 평가 → AI와 대조 → 직접 관찰·실험으로 결론.

## 평가 체계
- Nielsen 10(1994), Federoff(2002), Desurvire HEP(2004)·PLAY(2009), Pinelle 외(2008, 게임 리뷰 108개에서 게임 전용 휴리스틱 10개), Hodent(2017, 사용성 7원칙 + engage-ability: 동기·감정·게임 흐름).
- Pinelle P1~P10: 일관된 반응 / 조절 가능성 / NPC 예측 가능성 / 시야 / 반복 구간 건너뛰기 / 직관적·변경 가능한 입력 / 조작 감도 / 게임 상태 표시 / 도움말 / 해석 쉬운 시각 표현. P8·P10은 거의 모든 게임에서 검사할 가치가 높고, P3는 해당될 때만 본다.
- PLAY: "사용하기 어려움"과 "도전적임"은 다르다.
- HUD 4분류(diegetic / non-diegetic / spatial / meta)는 Fagerholt & Lorentzon(2009)의 단순화다. 원문은 더 복잡하다. HUD 종류 자체에 점수를 매기지 말고, 정보를 제때 전달하면서 의도한 경험을 유지하는지를 묻는다.
- WCAG 2.2 대비(일반 글자 4.5:1, 큰 글자·UI 3:1)는 게임에 그대로 합격·불합격으로 쓰지 않는다. 움직이는 배경, 효과, 도트 폰트 때문이다. 원본 색상값으로 계산했을 때만 수치를 쓴다. Xbox Accessibility Guidelines도 법적 판정표가 아니라 실무 기준이다.
- 운영용 체크리스트 C01~C17과 필요 입력(S/V/P/D)은 game-ui-critic.md에 그대로 옮겼다.

## LLM UI 평가 연구
| 연구 | 결과 | 해석 |
|---|---|---|
| UICrit (2024) | 모바일 UI 983개, 비평 3,059개. 유사 사례와 시각 힌트를 넣은 프롬프트로 기본 대비 55% 상대 향상 | 좋은 예시와 위치 표시가 도움 |
| Guerino 외 (2025) | GPT-4o가 전문가 발견 문제의 21.2%만 찾음. 목록에 없는 문제 27개, 허위 양성 있음 | 많이 찾는다고 정확한 것은 아님 |
| Zhong 외 (2025) | 앱 2개에서 기준 문제 73%, 77% 발견(사람 평가자 5명 집계는 57%, 63%) | 조건에 따라 높을 수 있음 |
| Criticmate (2026) | 인식 → 의미 → 문제 예측 단계별 평가가 한 번에 하는 평가보다 전문가에 가까움 | 단계별 검사에 근거 |

- 연구마다 대상과 기준이 달라 수치를 직접 비교할 수 없다. 게임 UI(실시간 액션 등)에 대한 직접 증거는 미확인이다.
- 자주 틀리는 것: 없는 문제를 지적함, UI 요소를 잘못 앎, 위치를 잘못 지목함, 화면 사이의 흐름을 놓침, 장르 관례를 오해함, 심각도를 과대평가함, 이미지로 손맛을 추측함.
- 효과 있는 기법: 유사 전문가 비평 예시 2~4개, 영역·좌표 기록, 문제 찾기와 위치 지정을 분리, 관찰 → 의미 → 평가 순서, 체크리스트 연결. 검증 패스와 확신도 표시는 합리적이지만 효과는 미확인이다.
- 항목마다 문제 개수를 강제하면 허위 양성이 생긴다.
- 원본 해상도를 유지하고, 작은 UI는 잘라서 따로 준다(Claude 비전 문서: 축소하면 위치 정밀도가 떨어진다).

## 구성안 비교 (원문, 비용은 추정)
- A 단일 체크리스트: 싸고 단순하다.
- B 병렬 전문 에이전트: 범위가 넓을 수 있지만 중복과 허위 양성이 늘고 비싸며, 근거가 미확인이다.
- C 단일 다단계(추천): 관찰 → 관점별 검사(가독성·위계 → 조작·피드백 → 온보딩·일관성 → 접근성·입력) → 근거 검증·중복 병합 → 심각도·수정안 → (학습 모드) 학생 평가와 대조.
- 심각도는 Nielsen 0~4를 쓰고, 확신도는 따로 매긴다.

## 구현 (원문 6절 요약)
- 첫 버전은 서브에이전트 파일 하나(.claude/agents/game-ui-critic.md). 기준이 커지면 스킬로 분리한다. 스킬은 지식과 절차를 담고, 서브에이전트는 독립된 문맥·모델·도구를 가진 작업자다.
- 원문은 Playwright MCP(npx @playwright/mcp@latest)로 웹 빌드를 직접 조작하는 안을 냈다. 매니저 판단으로 첫 버전에서는 빼고 매니저가 캡처해서 넘긴다. 이유는 버전을 고정하지 않은 패키지를 매번 받는 위험과 디스코드 호출 경로에서 브라우저를 쓸 수 없다는 점이다.

## 출처 (원문 링크)
Nielsen https://www.nngroup.com/articles/ten-usability-heuristics/ · Pinelle https://doi.org/10.1145/1357054.1357282 · HEP https://doi.org/10.1145/985921.986102 · PLAY https://doi.org/10.1007/978-3-642-02774-1_60 · Hodent https://celiahodent.com/gamers-brain-part-3-ux-engagement-immersion-retention-gdc17-talk/ · Beyond the HUD https://publications.lib.chalmers.se/records/fulltext/111921.pdf · WCAG 2.2 https://www.w3.org/TR/WCAG22/ · GAG https://gameaccessibilityguidelines.com/ · XAG https://learn.microsoft.com/en-us/xbox/accessibility/guidelines · UICrit https://arxiv.org/abs/2407.08850 · Guerino https://arxiv.org/abs/2506.16345 · Zhong https://arxiv.org/abs/2507.02306 · Criticmate https://doi.org/10.1145/3772318.3790929 · Claude vision https://platform.claude.com/docs/en/build-with-claude/vision-coordinates · Claude Code subagents https://code.claude.com/docs/en/sub-agents
