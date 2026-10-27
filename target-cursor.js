/* React Bits TargetCursor — version JavaScript native, sans React */
(() => {
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  if (!finePointer.matches || reducedMotion.matches) return;

  const root = document.createElement('div');
  root.className = 'target-cursor';
  root.setAttribute('aria-hidden', 'true');
  root.innerHTML = '<span class="target-cursor__corner"></span>'.repeat(4) +
    '<span class="target-cursor__dot"></span><span class="target-cursor__label"></span>';
  document.body.appendChild(root);

  const corners = [...root.querySelectorAll('.target-cursor__corner')];
  const dot = root.querySelector('.target-cursor__dot');
  const label = root.querySelector('.target-cursor__label');
  const angles = [0, 90, 180, 270], quarter = Math.PI / 2;
  const pointer = { x: 0, y: 0, inside: false, pressed: false, seen: false };
  const makeSpring = x => ({ x, v: 0 });
  const cx = makeSpring(0), cy = makeSpring(0), hw = makeSpring(18), hh = makeSpring(18);
  const rotation = makeSpring(0), lock = makeSpring(0), press = makeSpring(0), presence = makeSpring(0);
  let target = null, targetRadius = 0, quarterTurn = 0, spinSpeed = 0, raf = 0, last = 0, lastLabel = '';

  function spring(state, goal, stiffness, damping, dt) {
    const h = dt / 2;
    for (let i = 0; i < 2; i++) {
      state.v += (stiffness * (goal - state.x) - damping * state.v) * h;
      state.x += state.v * h;
    }
  }
  function findTarget(node) { return node?.closest?.('.cursor-target') || null; }
  function lockOn(next) {
    if (next === target) return;
    target = next;
    if (target) {
      quarterTurn = Math.round(rotation.x / quarter);
      targetRadius = parseFloat(getComputedStyle(target).borderTopLeftRadius) || 0;
      spinSpeed = 0;
    }
  }
  function wake() { if (!raf && pointer.inside) raf = requestAnimationFrame(frame); }

  function frame(now) {
    raf = 0;
    const dt = last ? Math.min(.05, (now - last) / 1000) : 1 / 60;
    last = now;
    if (target && !target.isConnected) lockOn(null);
    const rect = target?.getBoundingClientRect();
    const locked = Boolean(rect && pointer.inside);
    const snapW = 4.6 / .2, snapK = snapW * snapW, snapC = 2 * .62 * snapW;
    spring(presence, pointer.inside ? 1 : 0, 260, 32, dt);
    spring(lock, locked ? 1 : 0, snapK, 2 * snapW, dt);
    spring(press, pointer.pressed ? 1 : 0, 900, 40, dt);

    let gx = pointer.x, gy = pointer.y, gw = 18, gh = 18, gr = 2;
    if (locked) {
      const x = rect.left + rect.width / 2, y = rect.top + rect.height / 2;
      gx = x + (pointer.x - x) * .08; gy = y + (pointer.y - y) * .08;
      const odd = Math.abs(quarterTurn) % 2 === 1;
      gw = (odd ? rect.height : rect.width) / 2 + 6;
      gh = (odd ? rect.width : rect.height) / 2 + 6;
      gr = Math.min(targetRadius + 6, 12);
    }
    if (!pointer.seen) { cx.x = gx; cy.x = gy; hw.x = gw; hh.x = gh; pointer.seen = true; }
    const follow = locked ? snapK : 2200, followC = locked ? snapC : 2 * Math.sqrt(2200);
    spring(cx, gx, follow, followC, dt); spring(cy, gy, follow, followC, dt);
    spring(hw, gw, snapK, snapC, dt); spring(hh, gh, snapK, snapC, dt);
    if (locked) spring(rotation, quarterTurn * quarter, snapK, snapC, dt);
    else {
      const speed = Math.PI;
      spinSpeed += (speed - spinSpeed) * (1 - Math.exp(-dt * 3));
      rotation.v = spinSpeed; rotation.x += spinSpeed * dt;
    }

    const squeeze = 1 - press.x * .14, cos = Math.cos(rotation.x), sin = Math.sin(rotation.x);
    const w = Math.max(0, hw.x) * squeeze, h = Math.max(0, hh.x) * squeeze;
    const pts = [[-w,-h],[w,-h],[w,h],[-w,h]];
    const deg = rotation.x * 180 / Math.PI;
    let left = Infinity, top = Infinity;
    corners.forEach((corner, i) => {
      const [lx, ly] = pts[i], x = cx.x + lx*cos - ly*sin, y = cy.x + lx*sin + ly*cos;
      left = Math.min(left, x); top = Math.min(top, y);
      corner.style.transform = `translate3d(${x.toFixed(2)}px,${y.toFixed(2)}px,0) rotate(${(angles[i]+deg).toFixed(2)}deg)`;
      corner.style.borderTopLeftRadius = `${Math.max(0, Math.min(12, locked ? targetRadius + 6 : 2)).toFixed(2)}px`;
    });
    dot.style.transform = `translate3d(${pointer.x}px,${pointer.y}px,0) translate(-50%,-50%) scale(${(1-press.x*.35).toFixed(3)})`;
    const text = locked && target ? target.getAttribute('data-cursor-label') || '' : '';
    if (text && text !== lastLabel) label.textContent = text;
    if (text) lastLabel = text;
    const shown = text ? Math.max(0, Math.min(1, lock.x)) : 0;
    label.style.transform = `translate3d(${left.toFixed(2)}px,${(top-8).toFixed(2)}px,0) translateY(-100%) translateY(${((1-shown)*4).toFixed(2)}px)`;
    label.style.opacity = shown.toFixed(3);
    root.style.opacity = Math.max(0, Math.min(1, presence.x)).toFixed(3);

    const resting = !pointer.inside && presence.x < .002 && Math.abs(presence.v) < .002;
    const spinning = pointer.inside && !locked;
    const moving = Math.abs(cx.v)+Math.abs(cy.v)+Math.abs(hw.v)+Math.abs(hh.v)+Math.abs(rotation.v) > .01 ||
      Math.abs(gx-cx.x)+Math.abs(gy-cy.x) > .05 || Math.abs(lock.v)+Math.abs(press.v)+Math.abs(presence.v) > .001;
    if (!resting && (spinning || moving || locked)) raf = requestAnimationFrame(frame);
    else last = 0;
  }
  function markTargets(scope = document) {
    if (scope.matches?.('.album-card,.photo-item,.featured-photo,.text-link,.topnav a,.theme-toggle,.lb-nav,.lb-close,.lb-fullscreen')) addTarget(scope);
    scope.querySelectorAll?.('.album-card,.photo-item,.featured-photo,.text-link,.topnav a,.theme-toggle,.lb-nav,.lb-close,.lb-fullscreen').forEach(addTarget);
  }
  function addTarget(el) {
    el.classList.add('cursor-target');
    if (el.hasAttribute('data-cursor-label')) return;
    if (el.matches('.album-card')) el.setAttribute('data-cursor-label','Explorer');
    else if (el.matches('.photo-item,.featured-photo')) el.setAttribute('data-cursor-label','Agrandir');
    else if (el.matches('.text-link')) el.setAttribute('data-cursor-label','Découvrir');
  }
  function onMove(e) {
    if (e.pointerType && e.pointerType !== 'mouse') return;
    pointer.x=e.clientX; pointer.y=e.clientY; pointer.inside=true;
    document.documentElement.classList.add('target-cursor-active');
    lockOn(findTarget(e.target)); wake();
  }
  function onDown(e) { if (!e.pointerType || e.pointerType === 'mouse') { pointer.pressed=true; wake(); } }
  function onUp() { pointer.pressed=false; wake(); }
  function onLeave() {
    pointer.inside=false; pointer.pressed=false; pointer.seen=false; lockOn(null);
    document.documentElement.classList.remove('target-cursor-active');
    if (!raf) raf=requestAnimationFrame(frame);
  }
  function onScroll() {
    if (!pointer.inside) return;
    lockOn(findTarget(document.elementFromPoint(pointer.x,pointer.y))); wake();
  }
  markTargets();
  const observer = new MutationObserver(records => records.forEach(record => record.addedNodes.forEach(node => {
    if (node.nodeType === 1) markTargets(node);
  })));
  observer.observe(document.body,{childList:true,subtree:true});
  window.addEventListener('pointermove',onMove,{passive:true});
  window.addEventListener('pointerdown',onDown,{passive:true});
  window.addEventListener('pointerup',onUp,{passive:true});
  window.addEventListener('scroll',onScroll,{passive:true,capture:true});
  document.documentElement.addEventListener('pointerleave',onLeave);
  window.addEventListener('blur',onLeave);
})();
