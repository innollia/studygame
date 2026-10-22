(async () => {
  const MODE = "list"; // "list" 또는 "read"
  const ONLY = []; // read 모드에서 읽을 섹션 id 목록
  const KNOWN = {}; // list 모드에서 {섹션id: 해시} — 이미 저장된 것

  // 32비트 djb2 해시 (16진수)
  const hashStr = (str) => {
    let h = 5381;
    for (let i = 0; i < str.length; i++) {
      h = ((h << 5) + h + str.charCodeAt(i)) >>> 0;
    }
    return h.toString(16).padStart(8, "0");
  };

  // 노드에서 텍스트 항목 재귀 수집
  const collectItems = (node, out) => {
    const t = node.type;
    if (t === "STICKY" || t === "SHAPE_WITH_TEXT" || t === "TEXT") {
      const raw = t === "TEXT" ? node.characters : node.text?.characters;
      const text = (raw || "").trim().replace(/\r?\n+/g, " / ");
      if (text) {
        const box = node.absoluteBoundingBox || { x: node.x || 0, y: node.y || 0 };
        out.push({
          x: box.x || 0,
          y: box.y || 0,
          a: node.authorName || "",
          k: t === "STICKY" ? "s" : t === "TEXT" ? "t" : "h",
          t: text,
        });
      }
    }
    if (node.children) {
      for (const child of node.children) collectItems(child, out);
    }
  };

  // 최상위 섹션 및 섹션 밖(_loose) 수집
  const rawSections = [];
  const looseItems = [];
  for (const child of figma.currentPage.children) {
    if (child.type === "SECTION") {
      const items = [];
      collectItems(child, items);
      rawSections.push({ id: child.id, name: child.name || "", items });
    } else {
      collectItems(child, looseItems);
    }
  }
  if (looseItems.length > 0) {
    rawSections.push({ id: "_loose", name: "_loose", items: looseItems });
  }

  // (y, x) 정렬 및 해시 계산
  const sections = rawSections.map((sec) => {
    sec.items.sort((p, q) => p.y - q.y || p.x - q.x);
    const joined = sec.items.map((it) => `${it.a}|${it.t}`).join("\n");
    const hash = hashStr(joined);
    return { ...sec, hash };
  });

  if (MODE === "read") {
    const targetSet = new Set(ONLY);
    const filtered = sections
      .filter((sec) => targetSet.has(sec.id))
      .map((sec) => ({
        id: sec.id,
        name: sec.name,
        hash: sec.hash,
        items: sec.items.map(({ a, k, t }) => ({ a, k, t })),
      }));
    return JSON.stringify({ mode: "read", sections: filtered });
  }

  const listResult = sections.map((sec) => {
    const chars = sec.items.reduce((sum, it) => sum + it.t.length, 0);
    const status = !(sec.id in KNOWN)
      ? "new"
      : KNOWN[sec.id] === sec.hash
      ? "same"
      : "changed";
    return {
      id: sec.id,
      name: sec.name,
      count: sec.items.length,
      chars,
      hash: sec.hash,
      status,
    };
  });
  return JSON.stringify({ mode: "list", sections: listResult });
})()
