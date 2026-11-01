// 피그잼 게임 아이디어 자동 분류: 보드 쪽 읽기·옮기기.
// 로그인된 브라우저의 FigJam 페이지에서 실행한다(`figma` 전역). 러너가 PARAMS를 바꿔 끼운다.
// read:  받는 곳 섹션의 스티키를 [{id, text}]로 돌려준다(반응 스티키 포함).
// apply: 판정 [{id, kind, maturity, platform}]대로 색을 바꾸고 섹션으로 옮긴다.
(async () => {
  const PARAMS = { mode: "read", from: ["게임 아이디어 판"], decisions: [] };

  const INBOX = "게임 아이디어 판";
  const TARGET = { useful: "쓸만한 아이디어", fragment: "게임 아이디어 조각" };
  const COLOR = {
    indie: { r: 1, g: 0.851, b: 0.4 }, // 노랑
    roblox: { r: 1, g: 0.686, b: 0.639 }, // 빨강
    mobile: { r: 0.659, g: 0.855, b: 1 }, // 파랑
    any: { r: 0.902, g: 0.902, b: 0.902 }, // 회색
  };
  const GAP = 48, PAD = 96, COLS = 6, CELL = 240 + GAP;

  const page = figma.currentPage;
  const section = (name) => page.children.find((n) => n.type === "SECTION" && n.name === name);
  const stickies = (sec) => sec.children.filter((n) => n.type === "STICKY");
  const abs = (n) => n.absoluteBoundingBox;

  if (PARAMS.mode === "read") {
    const out = [];
    for (const name of PARAMS.from) {
      const sec = section(name);
      if (!sec) continue;
      for (const s of stickies(sec)) out.push({ id: s.id, text: s.text.characters });
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
    sec.resizeWithoutConstraints(2032, 1200);
    return sec;
  };
  const targets = {
    useful: ensure(TARGET.useful, TARGET.fragment),
    fragment: ensure(TARGET.fragment, INBOX),
  };

  // 반응 스티키·스탬프는 바로 위(겹친) 아이디어에 붙여서 같이 옮긴다.
  const byId = new Map(PARAMS.decisions.map((d) => [d.id, d]));
  const ideaNodes = PARAMS.decisions.filter((d) => d.kind === "idea").map((d) => figma.getNodeById(d.id)).filter(Boolean);
  const parentOf = (n) => {
    const b = abs(n);
    let best = null, bestDy = Infinity;
    for (const p of ideaNodes) {
      if (p.parent !== n.parent) continue;
      const pb = abs(p);
      const dx = Math.abs(pb.x - b.x), dy = b.y - pb.y;
      if (dx < 160 && dy > 0 && dy < pb.height + 240 && dy < bestDy) { best = p; bestDy = dy; }
    }
    return best;
  };
  const followers = new Map(ideaNodes.map((p) => [p.id, []]));
  for (const d of PARAMS.decisions) {
    if (d.kind !== "reaction") continue;
    const n = figma.getNodeById(d.id), p = n && parentOf(n);
    if (p) followers.get(p.id).push(n);
  }
  // 스탬프 하나는 겹친 스티키 중 맨 위에 그려진(나중 순서) 하나에만 붙인다.
  const stamps = new Set(ideaNodes.flatMap((p) => p.parent.children.filter((c) => c.type === "STAMP")));
  for (const st of stamps) {
    const sb = abs(st), cx = sb.x + sb.width / 2, cy = sb.y + sb.height / 2;
    const hits = ideaNodes.filter((p) => {
      const pb = abs(p);
      return p.parent === st.parent && cx > pb.x && cx < pb.x + pb.width && cy > pb.y && cy < pb.y + pb.height;
    });
    const top = hits.sort((a, b) => a.parent.children.indexOf(b) - a.parent.children.indexOf(a))[0];
    if (top) followers.get(top.id).push(st);
  }

  // 대상 섹션에서 이번에 옮기지 않는 것들 아래 줄부터 채운다.
  const moving = new Set([...byId.keys(), ...[...followers.values()].flat().map((f) => f.id)]);
  const nextRow = {};
  for (const [k, sec] of Object.entries(targets)) {
    const stay = sec.children.filter((c) => !moving.has(c.id));
    const bottom = Math.max(PAD - GAP, ...stay.map((c) => c.y + c.height));
    nextRow[k] = { y: bottom + GAP, col: 0, rowH: 0 };
    // 맨 아래 것이 스티키 줄이고 자리가 남았으면 그 줄을 이어서 채운다.
    const lowest = stay.reduce((a, c) => (!a || c.y + c.height > a.y + a.height ? c : a), null);
    if (lowest && lowest.type === "STICKY") {
      const row = stay.filter((c) => c.type === "STICKY" && Math.abs(c.y - lowest.y) < 10);
      const col = Math.max(...row.map((c) => Math.ceil((c.x + c.width - PAD + GAP) / CELL)));
      if (col < COLS) nextRow[k] = { y: lowest.y, col, rowH: Math.max(...row.map((c) => c.height)) };
    }
  }
  const moved = [];
  for (const p of ideaNodes) {
    const d = byId.get(p.id), sec = targets[d.maturity], cur = nextRow[d.maturity];
    const group = followers.get(p.id);
    const oldX = p.x, oldY = p.y, oldParent = p.parent;
    const offs = group.map((f) => ({ f, dx: f.x - oldX, dy: f.y - oldY }));
    const extraH = Math.max(0, ...offs.map((o) => o.dy + o.f.height - p.height));
    const span = Math.ceil((p.width + GAP) / CELL);
    if (cur.col > 0 && cur.col + span > COLS) { cur.y += cur.rowH + GAP; cur.col = 0; cur.rowH = 0; }
    p.fills = [{ type: "SOLID", color: COLOR[d.platform] }];
    if (oldParent !== sec) sec.appendChild(p);
    p.x = PAD + cur.col * CELL;
    p.y = cur.y;
    for (const o of offs) {
      if (o.f.parent !== sec) sec.appendChild(o.f);
      o.f.x = p.x + o.dx;
      o.f.y = p.y + o.dy;
    }
    cur.rowH = Math.max(cur.rowH, p.height + extraH);
    cur.col += span;
    moved.push(p.id);
  }
  for (const sec of Object.values(targets)) {
    const w = Math.max(sec.width, ...sec.children.map((c) => c.x + c.width + PAD));
    const h = Math.max(sec.height, ...sec.children.map((c) => c.y + c.height + PAD));
    sec.resizeWithoutConstraints(w, h);
  }
  return JSON.stringify({ moved: moved.length });
})();
