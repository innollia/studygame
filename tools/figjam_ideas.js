// 피그잼 게임 아이디어 자동 분류: 보드 쪽 읽기·옮기기.
// 로그인된 브라우저의 FigJam 페이지에서 실행한다(`figma` 전역). 러너가 PARAMS를 바꿔 끼운다.
// 겹치거나 붙어 있는 것(스티키·그림·스탬프·글)은 아이디어 하나로 보고 한 묶음으로 옮긴다.
// read:  받는 곳 섹션의 묶음을 [{id, ids, text}]로 돌려준다(id = 묶음의 맨 위 스티키).
// apply: 판정 [{id, ids, kind, maturity, platform}]대로 스티키 색을 바꾸고 묶음째 옮긴다.
(async () => {
  const PARAMS = { mode: "read", from: ["게임 아이디어 판"], decisions: [] };

  const TARGET = { useful: "쓸만한 아이디어", fragment: "게임 아이디어 조각" };
  const COLOR = {
    indie: { r: 1, g: 0.851, b: 0.4 }, // 노랑
    roblox: { r: 1, g: 0.686, b: 0.639 }, // 빨강
    mobile: { r: 0.659, g: 0.855, b: 1 }, // 파랑
    any: { r: 0.902, g: 0.902, b: 0.902 }, // 회색
  };
  const JOIN = 24, GAP = 48, PAD = 96, WIDTH = 6 * 288;

  const page = figma.currentPage;
  const section = (name) => page.children.find((n) => n.type === "SECTION" && n.name === name);
  const box = (ns) => {
    const x = Math.min(...ns.map((n) => n.x)), y = Math.min(...ns.map((n) => n.y));
    return { x, y, w: Math.max(...ns.map((n) => n.x + n.width)) - x, h: Math.max(...ns.map((n) => n.y + n.height)) - y };
  };

  // 섹션 안 노드를 겹침·근접(JOIN px)으로 묶는다.
  const clusters = (sec) => {
    const items = sec.children.filter((c) => c.type !== "CONNECTOR");
    const par = items.map((_, i) => i);
    const find = (i) => (par[i] === i ? i : (par[i] = find(par[i])));
    for (let i = 0; i < items.length; i++)
      for (let j = i + 1; j < items.length; j++) {
        const a = items[i], b = items[j];
        if (a.x - JOIN < b.x + b.width && b.x - JOIN < a.x + a.width && a.y - JOIN < b.y + b.height && b.y - JOIN < a.y + a.height)
          par[find(i)] = find(j);
      }
    const groups = {};
    items.forEach((c, i) => (groups[find(i)] = groups[find(i)] || []).push(c));
    return Object.values(groups)
      .map((ns) => ({ ns, st: ns.filter((n) => n.type === "STICKY").sort((p, q) => p.y - q.y || p.x - q.x) }))
      .filter((g) => g.st.length > 0);
  };

  if (PARAMS.mode === "read") {
    const out = [];
    for (const name of PARAMS.from) {
      const sec = section(name);
      if (!sec) continue;
      for (const g of clusters(sec))
        out.push({ id: g.st[0].id, ids: g.ns.map((n) => n.id), text: g.st.map((s) => s.text.characters).join("\n---\n") });
    }
    return JSON.stringify(out);
  }

  // apply
  const ensure = (name, nearName) => {
    let sec = section(name);
    if (sec) return sec;
    const near = section(nearName);
    sec = figma.createSection();
    sec.name = name;
    sec.x = near ? near.x + near.width + 200 : 0;
    sec.y = near ? near.y : 0;
    sec.resizeWithoutConstraints(PAD * 2 + WIDTH, 1200);
    return sec;
  };
  const targets = { fragment: ensure(TARGET.fragment, PARAMS.from[0]) };
  targets.useful = ensure(TARGET.useful, TARGET.fragment);

  const ideas = PARAMS.decisions.filter((d) => d.kind === "idea")
    .map((d) => ({ d, ns: d.ids.map((id) => figma.getNodeById(id)).filter(Boolean) }))
    .filter((g) => g.ns.length);
  const moving = new Set(ideas.flatMap((g) => g.ns.map((n) => n.id)));

  // 대상 섹션에서 옮기지 않는 것들 아래, 새 줄부터 왼쪽→오른쪽으로 채운다.
  const cursor = {};
  for (const [k, sec] of Object.entries(targets)) {
    const stay = sec.children.filter((c) => !moving.has(c.id));
    cursor[k] = { x: PAD, y: Math.max(PAD - GAP, ...stay.map((c) => c.y + c.height)) + GAP, rowH: 0 };
  }
  // 스탬프는 붙은 스티키를 따라 FigJam이 알아서 옮긴다. 직접 옮기면 두 번 움직인다.
  for (const g of ideas) g.ns = g.ns.filter((n) => n.type !== "STAMP");
  for (const { d, ns } of ideas) {
    const sec = targets[d.maturity], cur = cursor[d.maturity], b = box(ns);
    if (cur.x > PAD && cur.x + b.w > PAD + WIDTH) { cur.y += cur.rowH + GAP; cur.x = PAD; cur.rowH = 0; }
    for (const n of ns) {
      const dx = n.x - b.x, dy = n.y - b.y;
      if (n.type === "STICKY") n.fills = [{ type: "SOLID", color: COLOR[d.platform] }];
      if (n.parent !== sec) sec.appendChild(n);
      n.x = cur.x + dx;
      n.y = cur.y + dy;
    }
    cur.x += b.w + GAP;
    cur.rowH = Math.max(cur.rowH, b.h);
  }
  for (const sec of Object.values(targets)) {
    if (!sec.children.length) continue;
    const b = box(sec.children);
    sec.resizeWithoutConstraints(Math.max(sec.width, b.x + b.w + PAD), Math.max(sec.height, b.y + b.h + PAD));
  }
  return JSON.stringify({ moved: ideas.length });
})();
