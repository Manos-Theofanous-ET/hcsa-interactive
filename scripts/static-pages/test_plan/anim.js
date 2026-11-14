/* HCSA test plan: one animation per test, drawn on canvas.
   Every shape is schematic. Rev F dimensions where the drawings give them;
   gaps and deflections are drawn far larger than life so they can be seen.
   No value shown on a bar or plot is a measurement; limits and model
   predictions are labelled as such. */
(function () {
  "use strict";
  var W = 960, H = 460;
  var C = {
    bg: "#0d1014", grid: "rgba(255,255,255,.035)", ink: "#f1efea", ink2: "rgba(241,239,234,.74)",
    ink3: "rgba(241,239,234,.46)", line: "rgba(241,239,234,.22)", acc: "#c9b48f",
    alu: "#55606f", alu2: "#7d8a9c", aluE: "#a9b4c3", steel: "#6b6f76", steel2: "#8f949b",
    force: "#ff8a4c", meas: "#7fc8f8", ok: "#79c48f", bad: "#ef7d6b", warn: "#e6b75c",
    cord: "#141414", cordE: "#d8d2c4", rtv: "#d99a52", glass: "rgba(150,215,235,.55)", glassE: "#9fd8eb",
    water: "rgba(64,132,214,.42)", waterE: "#5b9be0", air: "rgba(127,200,248,.25)"
  };
  var FONT = '"Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif';

  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function ease(t) { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); }
  function seg(t, a, b) { return clamp((t - a) / (b - a), 0, 1); }

  // ---------- drawing helpers ----------
  function G(ctx) { this.c = ctx; }
  G.prototype.font = function (size, weight) { this.c.font = (weight || 400) + " " + size + "px " + FONT; };
  G.prototype.text = function (s, x, y, o) {
    o = o || {}; var c = this.c;
    this.font(o.size || 14, o.weight || 400);
    c.textAlign = o.align || "left"; c.textBaseline = o.base || "alphabetic";
    if (o.bg) {
      var w = c.measureText(s).width, h = (o.size || 14) + 6, x0 = o.align === "center" ? x - w / 2 : o.align === "right" ? x - w : x;
      c.fillStyle = o.bg; c.fillRect(x0 - 5, y - h + 4, w + 10, h + 2);
    }
    c.fillStyle = o.color || C.ink2; c.fillText(s, x, y);
  };
  G.prototype.lines = function (arr, x, y, o) { var lh = (o && o.lh) || 18; for (var i = 0; i < arr.length; i++) this.text(arr[i], x, y + i * lh, o); };
  G.prototype.rect = function (x, y, w, h, fill, stroke, lw) {
    var c = this.c; if (fill) { c.fillStyle = fill; c.fillRect(x, y, w, h); }
    if (stroke) { c.strokeStyle = stroke; c.lineWidth = lw || 1; c.strokeRect(x + .5, y + .5, w - 1, h - 1); }
  };
  G.prototype.line = function (x1, y1, x2, y2, col, lw, dash) {
    var c = this.c; c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2, y2); c.strokeStyle = col; c.lineWidth = lw || 1;
    c.setLineDash(dash || []); c.stroke(); c.setLineDash([]);
  };
  G.prototype.circle = function (x, y, r, fill, stroke, lw) {
    var c = this.c; c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2);
    if (fill) { c.fillStyle = fill; c.fill(); } if (stroke) { c.strokeStyle = stroke; c.lineWidth = lw || 1; c.stroke(); }
  };
  G.prototype.poly = function (pts, fill, stroke, lw) {
    var c = this.c; c.beginPath(); c.moveTo(pts[0][0], pts[0][1]);
    for (var i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath();
    if (fill) { c.fillStyle = fill; c.fill(); } if (stroke) { c.strokeStyle = stroke; c.lineWidth = lw || 1; c.stroke(); }
  };
  G.prototype.arrow = function (x1, y1, x2, y2, col, lw, head) {
    var c = this.c, a = Math.atan2(y2 - y1, x2 - x1), h = head || 11, L = Math.hypot(x2 - x1, y2 - y1);
    if (L < 2) return;
    c.strokeStyle = col; c.fillStyle = col; c.lineWidth = lw || 3; c.lineCap = "round";
    c.beginPath(); c.moveTo(x1, y1); c.lineTo(x2 - Math.cos(a) * h * .8, y2 - Math.sin(a) * h * .8); c.stroke();
    c.beginPath(); c.moveTo(x2, y2);
    c.lineTo(x2 - h * Math.cos(a - .42), y2 - h * Math.sin(a - .42));
    c.lineTo(x2 - h * Math.cos(a + .42), y2 - h * Math.sin(a + .42)); c.closePath(); c.fill(); c.lineCap = "butt";
  };
  // a horizontal bar gauge with an optional limit mark and markers
  G.prototype.bar = function (x, y, w, label, frac, o) {
    o = o || {}; var c = this.c;
    this.text(label, x, y - 8, { size: 13, color: C.ink2 });
    this.rect(x, y, w, 12, "rgba(255,255,255,.06)", C.line);
    var f = clamp(frac, 0, 1.15), col = o.color || C.meas;
    if (o.limit !== undefined && frac > o.limit) col = C.bad;
    this.rect(x + 1, y + 1, Math.min(w - 2, (w - 2) * f / (o.max || 1)), 10, col);
    if (o.limit !== undefined) {
      var lx = x + w * o.limit / (o.max || 1);
      this.line(lx, y - 3, lx, y + 15, C.bad, 2);
      if (o.limitLabel) this.text(o.limitLabel, lx, y + 29, { size: 12, color: C.bad, align: "center" });
    }
    (o.marks || []).forEach(function (m) {
      var mx = x + w * m[0] / (o.max || 1);
      this.line(mx, y - 3, mx, y + 15, m[2] || C.acc, 2, [3, 2]);
      if (m[1]) this.text(m[1], mx, y + 29 + (m[3] || 0), { size: 12, color: m[2] || C.acc, align: "center" });
    }, this);
  };
  // small plot frame; fn(u) returns y in 0..1 for u in 0..uEnd
  G.prototype.plot = function (x, y, w, h, o) {
    var c = this.c; o = o || {};
    this.rect(x, y, w, h, "rgba(255,255,255,.03)", C.line);
    if (o.title) this.text(o.title, x, y - 8, { size: 13, color: C.ink2 });
    if (o.xl) this.text(o.xl, x + w, y + h + 16, { size: 12, color: C.ink3, align: "right" });
    if (o.yl) this.text(o.yl, x + 4, y + 14, { size: 12, color: C.ink3 });
    (o.hlines || []).forEach(function (hl) {
      var yy = y + h - h * hl[0]; this.line(x, yy, x + w, yy, hl[2] || C.bad, 1.5, [5, 4]);
      if (hl[1]) this.text(hl[1], x + w - 4, yy - 5, { size: 12, color: hl[2] || C.bad, align: "right" });
    }, this);
    if (o.fn) {
      var n = o.n || 120, uEnd = clamp(o.uEnd === undefined ? 1 : o.uEnd, 0, 1);
      if (uEnd <= 0) return;
      c.beginPath();
      for (var i = 0; i <= n; i++) {
        var u = uEnd * i / n, v = clamp(o.fn(u), 0, 1.05);
        var px = x + w * u, py = y + h - h * v; if (i === 0) c.moveTo(px, py); else c.lineTo(px, py);
      }
      c.strokeStyle = o.color || C.meas; c.lineWidth = 2.2; c.stroke();
      var ve = clamp(o.fn(uEnd), 0, 1.05); this.circle(x + w * uEnd, y + h - h * ve, 4, o.color || C.meas);
    }
  };
  G.prototype.clock = function (x, y, r, frac, label) {
    this.circle(x, y, r, "rgba(255,255,255,.04)", C.ink3, 1.5);
    var a = -Math.PI / 2 + frac * Math.PI * 2;
    this.line(x, y, x + Math.cos(a) * r * .8, y + Math.sin(a) * r * .8, C.acc, 2.5);
    if (label) this.text(label, x, y + r + 18, { size: 13, color: C.ink2, align: "center" });
  };

  function background(g, scene, t) {
    var c = g.c; c.fillStyle = C.bg; c.fillRect(0, 0, W, H);
    c.strokeStyle = C.grid; c.lineWidth = 1;
    for (var x = 0; x <= W; x += 40) { c.beginPath(); c.moveTo(x + .5, 0); c.lineTo(x + .5, H); c.stroke(); }
    for (var y = 0; y <= H; y += 40) { c.beginPath(); c.moveTo(0, y + .5); c.lineTo(W, y + .5); c.stroke(); }
    var k = phaseAt(scene, t);
    g.text((k + 1) + " / " + scene.phases.length + "   " + scene.phases[k][1], 22, 32, { size: 16, weight: 600, color: C.ink });
    g.text(scene.tag, W - 22, 32, { size: 13, color: C.ink3, align: "right" });
  }
  function phaseAt(scene, t) { var k = 0; for (var i = 0; i < scene.phases.length; i++) if (t >= scene.phases[i][0]) k = i; return k; }

  // =====================================================================
  // T0: glass bar in four-point bending
  // =====================================================================
  var T0 = {
    tag: "schematic; Weibull points are an example, not data", dur: 19, still: 7.5,
    phases: [
      [0, "Set the bar on the supports", "The bar is 1 x 1/8 inch with fine-ground edges and an arris. Two supports below, two loading pins above at half the span."],
      [3, "Load at a fixed stress rate", "The pins press down. Between them the bottom face is in even tension, the highest stress in the bar."],
      [9, "Break: record the load", "The bar breaks somewhere between the pins. Tape on the tension face keeps the pieces together."],
      [11.5, "Find where it started", "Face or edge? Every origin is recorded, because the pane edge sits on the seat."],
      [14.5, "30 or more breaks, then the Weibull fit", "Each break is one point. The slope of the line is m: steep means consistent glass."]
    ],
    draw: function (g, t) {
      var c = g.c, x0 = 120, x1 = 640, ymid = 210, span = x1 - x0;
      var sL = x0 + span * .08, sR = x1 - span * .08, pL = x0 + span * .29, pR = x1 - span * .29;
      var load = t < 3 ? 0 : t < 9 ? seg(t, 3, 9) : 0;
      var broken = t >= 9;
      var slideIn = ease(seg(t, 0, 1.6));
      var dx = (1 - slideIn) * -300;
      var defl = load * 26;
      // supports
      g.poly([[sL, ymid + 22], [sL - 16, ymid + 58], [sL + 16, ymid + 58]], C.steel, C.steel2);
      g.poly([[sR, ymid + 22], [sR - 16, ymid + 58], [sR + 16, ymid + 58]], C.steel, C.steel2);
      g.rect(x0 - 30, ymid + 58, span + 60, 12, "#2a2e35");
      // bar shape: deflection profile of four-point bending (schematic)
      function yb(x) {
        if (x <= sL || x >= sR) return 0;
        var u = (x - sL) / (sR - sL); return Math.sin(Math.PI * u) * defl;
      }
      var crackX = lerp(pL, pR, .62), sep = broken ? ease(seg(t, 9, 10)) * 10 : 0;
      function drawBar(xa, xb, tilt, pivot) {
        c.save();
        if (tilt) { c.translate(pivot, ymid + 18); c.rotate(tilt); c.translate(-pivot, -(ymid + 18)); }
        c.beginPath();
        var n = 60, i, x;
        for (i = 0; i <= n; i++) { x = lerp(xa, xb, i / n); var y = ymid + yb(x) + (broken ? 0 : 0); if (i === 0) c.moveTo(x + dx, y); else c.lineTo(x + dx, y); }
        for (i = n; i >= 0; i--) { x = lerp(xa, xb, i / n); c.lineTo(x + dx, ymid + 18 + yb(x)); }
        c.closePath();
        var gr = c.createLinearGradient(0, ymid, 0, ymid + 18);
        gr.addColorStop(0, "rgba(150,215,235,.35)");
        gr.addColorStop(1, load > 0 ? "rgba(255,138,76," + (0.25 + .6 * load) + ")" : "rgba(150,215,235,.55)");
        c.fillStyle = gr; c.fill(); c.strokeStyle = C.glassE; c.lineWidth = 1.2; c.stroke();
        c.restore();
      }
      if (!broken) drawBar(x0 + 10, x1 - 10);
      else {
        var tl = -sep * .006, tr = sep * .006;
        drawBar(x0 + 10, crackX - 1, tl, sL); drawBar(crackX + 1, x1 - 10, tr, sR);
        // tape
        g.line(crackX - 30 + dx, ymid + 19, crackX + 30 + dx, ymid + 19, C.acc, 2);
        if (t < 10.5) { var fl = 1 - seg(t, 9, 10.5); g.circle(crackX, ymid + 14, 22 * fl + 6, "rgba(255,220,180," + (.5 * fl) + ")"); }
      }
      // loading pins
      var pinY = ymid - 14 + yb(pL);
      [pL, pR].forEach(function (px) { g.circle(px + dx, pinY, 12, C.steel, C.steel2, 1.5); });
      g.rect(pL - 6 + dx, pinY - 70, pR - pL + 12, 10, C.steel);
      g.line(pL + dx, pinY - 60, pL + dx, pinY - 12, C.steel2, 4); g.line(pR + dx, pinY - 60, pR + dx, pinY - 12, C.steel2, 4);
      if (load > 0 && !broken) g.arrow((pL + pR) / 2, pinY - 130, (pL + pR) / 2, pinY - 74, C.force, 4, 14);
      // span labels
      if (t < 9) {
        g.line(sL, ymid + 92, sR, ymid + 92, C.ink3, 1); g.text("support span L", (sL + sR) / 2, ymid + 110, { size: 13, align: "center", color: C.ink3 });
        g.line(pL, ymid - 104, pR, ymid - 104, C.ink3, 1); g.text("load span L/2", (pL + pR) / 2, ymid - 112, { size: 13, align: "center", color: C.ink3 });
      }
      if (load > 0 && !broken) g.text("even tension on the bottom face between the pins", (pL + pR) / 2, ymid + 140, { size: 13, align: "center", color: C.force });
      // cross-section inset with arris
      var ix = 720, iy = 96, s = 7;
      g.text("Section, 25.4 x 3.2 mm", ix, iy - 14, { size: 13, color: C.ink2 });
      var bw = 25.4 * s * .7, bh = 3.2 * s * 1.6, ar = 6;
      g.poly([[ix + ar, iy], [ix + bw - ar, iy], [ix + bw, iy + ar], [ix + bw, iy + bh - ar], [ix + bw - ar, iy + bh], [ix + ar, iy + bh], [ix, iy + bh - ar], [ix, iy + ar]], C.glass, C.glassE, 1.2);
      g.text("arris on every edge, measured", ix, iy + bh + 20, { size: 12, color: C.ink3 });
      if (t >= 11.5) {
        var pulse = .5 + .5 * Math.sin(t * 6);
        g.circle(ix + bw - 3, iy + bh - 3, 6 + 3 * pulse, null, C.force, 2.5);
        g.text("edge origin", ix + bw + 10, iy + bh + 4, { size: 13, color: C.force });
        g.circle(ix + bw * .4, iy + bh, 4, null, C.meas, 2);
        g.text("or a face origin", ix + bw * .4 - 10, iy + bh + 40, { size: 13, color: C.meas });
      }
      // load-time plot
      var px = 700, py = 210, pw = 230, ph = 100;
      g.plot(px, py, pw, ph, {
        title: "Load against time", xl: "time", color: C.force,
        fn: function (u) { var tt = 3 + u * 8; if (tt < 9) return seg(tt, 3, 9) * .92; return 0; },
        uEnd: clamp((t - 3) / 8, 0, 1)
      });
      if (broken && t < 14.5) g.text("break load gives the strength", px + 8, py + 18, { size: 12, color: C.force });
      // Weibull plot (example points)
      if (t >= 14.5) {
        g.rect(690, 70, 250, 345, C.bg);
        var wx = 712, wy = 110, ww = 220, wh = 230, nShow = Math.floor(clamp((t - 14.5) / 3.2, 0, 1) * 30);
        g.plot(wx, wy, ww, wh, { title: "Weibull plot (example points)", xl: "log strength" });
        g.text("log of failure odds", wx + 4, wy + 14, { size: 12, color: C.ink3 });
        function WX(xv) { return wx + ww * (.06 + (xv + .64) / .9 * .88); }
        function WY(yv) { return wy + wh * (.94 - (yv + 4.2) / 5.6 * .88); }
        for (var i = 0; i < nShow; i++) {
          var F = (i + .5) / 30, yv = Math.log(-Math.log(1 - F)), jit = Math.sin(i * 12.9898) * .045;
          g.circle(WX(yv / 7 + jit), WY(yv), 3.5, C.meas); // slope m = 7 in the example
        }
        if (t > 17.8) {
          g.line(WX(-4.2 / 7), WY(-4.2), WX(1.4 / 7), WY(1.4), C.acc, 2);
          g.text("slope = m", wx + 10, wy + 40, { size: 14, color: C.acc, weight: 600 });
        }
        g.text(nShow + " breaks", wx, wy + wh + 36, { size: 13, color: C.ink2 });
      }
    }
  };

  // =====================================================================
  // T1: seam slice, section view, run 1 and run 2
  // =====================================================================
  var T1 = {
    tag: "schematic section; gaps drawn about 150 x", dur: 27, still: 16.5,
    phases: [
      [0, "One slice of the seam, at full size", "Frame A and frame B meet face to face, 180 mm deep. The pull blocks sit in the legs. Slices are 75, 150 and 225 mm long, with 1, 2 and 3 bolts."],
      [4, "Seal it and set the preload", "The two cords go in the glands of frame B, the RTV bead is laid and cured, the bolt goes to 4 kN, and air goes into the space between the cords."],
      [7.5, "Run 1: straight pull at z 90", "The control run. The load is held while the pressure at the port is watched, then released."],
      [13.5, "Run 2: prying pull at z 24", "Pulled near the outer flange, the seam opens about its cabin-side edge, the way cabin pressure opens it. The gap between the cords is read against 0.11 mm."],
      [20.5, "Ramp to failure", "On fresh bolts the load keeps rising: the gap passes 0.11 mm, air gets past the cords and the port pressure falls. That gap is the real sealing limit."]
    ],
    draw: function (g, t) {
      var c = g.c, s = 1.15, J = 350, Z0 = 112; // joint face x, z=0 y
      function Y(z) { return Z0 + z * s; }
      // state by time
      var run1 = t >= 7.5 && t < 13.5 ? Math.sin(Math.PI * seg(t, 8, 13)) : 0;
      var run2 = t >= 13.5 && t < 20.5 ? Math.sin(Math.PI * seg(t, 14, 20)) : 0;
      var fail = t >= 20.5 ? ease(seg(t, 21, 26.5)) : 0;
      var sepU = run1 * 2.2;              // even separation, px
      var th = run2 * .03 + fail * .075;  // rotation about the cabin edge, rad
      var sealed = t >= 4 ? ease(seg(t, 4, 7)) : 0;
      var pivot = [J, Y(180)];
      function frame(side) { // side -1 = A (left), +1 = B (right)
        c.save();
        c.translate(pivot[0], pivot[1]); c.rotate(side * th); c.translate(-pivot[0], -pivot[1]);
        c.translate(side * sepU, 0);
        var web = 20 * s, leg = 200 * s, sgn = side;
        var xw0 = J, xw1 = J + sgn * web, xl = J + sgn * leg;
        var col = C.alu, edge = C.aluE;
        // web
        g.poly([[xw0, Y(0)], [xw1, Y(0)], [xw1, Y(180)], [xw0, Y(180)]], col, edge, 1);
        // flange (z 0-10) and lip (z 170-180) running out as legs
        g.poly([[xw1, Y(0)], [xl, Y(0)], [xl, Y(10)], [xw1, Y(10)]], col, edge, 1);
        g.poly([[xw1, Y(170)], [xl, Y(170)], [xl, Y(180)], [xw1, Y(180)]], col, edge, 1);
        // pull block (4140), 160 tall between the legs, 80 wide at the leg ends
        var bx0 = xl - sgn * 80 * s;
        g.poly([[bx0, Y(10)], [xl, Y(10)], [xl, Y(170)], [bx0, Y(170)]], C.steel, C.steel2, 1);
        // M12 screws through flange and lip
        for (var k = 0; k < 2; k++) { var sx = lerp(bx0, xl, .3 + .4 * k); g.line(sx, Y(-3), sx, Y(26), "#c8ccd2", 2.5); g.line(sx, Y(154), sx, Y(183), "#c8ccd2", 2.5); }
        // glands, cords and RTV in frame B's face
        if (side > 0) {
          [18, 32].forEach(function (z) {
            g.rect(J, Y(z) - 7.1 * s / 2, 4.0 * s * 1.6, 7.1 * s, "#20252c");
            if (sealed > 0) {
              c.save(); c.globalAlpha = sealed;
              c.beginPath(); c.ellipse(J + 3.4, Y(z), 4.6, 5.5, 0, 0, Math.PI * 2); c.fillStyle = C.cord; c.fill(); c.strokeStyle = C.cordE; c.lineWidth = 1.2; c.stroke();
              c.restore();
            }
          });
          c.beginPath(); c.arc(J, Y(42), 3 * s * 1.3, -Math.PI / 2, Math.PI / 2); c.fillStyle = sealed > .5 ? C.rtv : "#20252c"; c.fill();
          // leak port at z 25 through the web to the channel side
          g.line(J, Y(25), xw1, Y(25), C.meas, 2);
        }
        // the bolt hole
        g.rect(Math.min(J, xw1), Y(58) - 4.2 * s, web, 8.4 * s, "#1b1f25");
        c.restore();
        return { xl: xl, bx0: bx0 };
      }
      frame(-1); frame(1);
      // bolt across the joint (drawn between the two rotated webs, approximately)
      var gTop = Math.sin(th) * 180 * s * 2 + sepU * 2; // visual gap at z 0
      var gz = function (z) { return Math.sin(th) * (180 - z) * s * 2 + sepU * 2; };
      var bx0 = J - 20 * s - gz(58) / 2 - 8, bx1 = J + 20 * s + gz(58) / 2 + 8;
      var boltBroken = fail > .96;
      if (!boltBroken) {
        g.line(bx0, Y(58), bx1, Y(58), "#d6dbe2", 7);
        g.rect(bx0 - 8, Y(58) - 10, 8, 20, "#d6dbe2"); g.rect(bx1, Y(58) - 9, 9, 18, "#d6dbe2");
      } else {
        g.line(bx0, Y(58), J - 4, Y(58), C.bad, 7); g.line(J + 4, Y(58), bx1, Y(58), C.bad, 7);
      }
      // the visible gap between the faces (wedge) and air between the cords
      if (gTop > .5) {
        var a1 = J - gz(0) / 2, a2 = J + gz(0) / 2;
        g.poly([[a1, Y(0)], [a2, Y(0)], [J, Y(180)]], "rgba(255,138,76,.18)");
      }
      if (sealed > .8 && fail < .68) {
        g.rect(J - 1.5 - gz(25) / 2, Y(19), 3 + gz(25), Y(31) - Y(19), C.air);
      }
      // leak: particles escaping past the outer cord
      if (fail > .68 && fail < .98) {
        for (var p = 0; p < 9; p++) {
          var ph = ((t * 1.7 + p / 9) % 1);
          g.circle(J + Math.sin(p * 3.1) * 3, Y(25 - ph * 40), 2.2, C.meas);
        }
      }
      // pull arrows: run 1 at z 90, run 2 at z 24 through lug and pin
      var leftEnd = J - 200 * s, rightEnd = J + 200 * s;
      var F1 = run1, F2 = Math.max(run2, fail);
      if (t >= 7.5 && t < 13.5) {
        g.line(leftEnd - 46, Y(90), leftEnd, Y(90), "#c8ccd2", 5); g.line(rightEnd, Y(90), rightEnd + 46, Y(90), "#c8ccd2", 5);
        if (F1 > .02) { g.arrow(leftEnd - 48, Y(90), leftEnd - 48 - 44 * F1, Y(90), C.force, 4); g.arrow(rightEnd + 48, Y(90), rightEnd + 48 + 44 * F1, Y(90), C.force, 4); }
        g.text("M24 rod at z 90", leftEnd, Y(90) - 12, { size: 12, color: C.ink3 });
      }
      if (t >= 13.5) {
        var rl = Math.sin(th) * (180 - 24) * s;
        [[-1, leftEnd - rl], [1, rightEnd + rl]].forEach(function (q) {
          var sd = q[0], ex = q[1];
          g.rect(sd < 0 ? ex - 26 : ex, Y(14), 26, 22, C.steel, C.steel2);
          g.circle(sd < 0 ? ex - 26 : ex + 26, Y(24), 7, "#d6dbe2");
          if (F2 > .02) g.arrow(sd < 0 ? ex - 36 : ex + 36, Y(24), sd < 0 ? ex - 36 - 44 * F2 : ex + 36 + 44 * F2, Y(24), C.force, 4);
        });
        g.text("lug, fork and pin at z 24", leftEnd - 20, Y(0) - 14, { size: 12, color: C.ink3 });
      }
      // labels
      if (t < 4) {
        g.text("frame A", J - 95 * s, Y(100), { size: 15, weight: 600, color: C.ink, align: "center" });
        g.text("frame B", J + 95 * s, Y(100), { size: 15, weight: 600, color: C.ink, align: "center" });
        g.text("pull block", J - 160 * s, Y(180) + 24, { size: 12, color: C.ink3, align: "center" });
        g.text("legs, 200 mm", J + 110 * s, Y(180) + 24, { size: 12, color: C.ink3, align: "center" });
        g.text("outer face, z 0", J, Y(0) - 12, { size: 12, color: C.ink3, align: "center" });
        g.text("cabin face, z 180", J, Y(180) + 24, { size: 12, color: C.ink3, align: "center" });
      } else if (t < 7.5) {
        var lx = J + 20 * s + 30;
        [[18, "cords, z' 18 and 32"], [42, "RTV bead, z' 42"], [58, "bolt, z' 58, 4 kN"], [76, "port between the cords"]].forEach(function (l) {
          g.text(l[1], lx, Y(l[0]) + 4 + (l[0] === 18 ? 6 : 0), { size: 12, color: l[0] === 76 ? C.meas : C.ink2 });
        });
      }
      // right panel: readouts and the slice lengths
      var rx = 700;
      if (t < 4) {
        g.text("Three lengths", rx, 120, { size: 14, weight: 600, color: C.ink });
        [[75, 1], [150, 2], [225, 3]].forEach(function (L, i) {
          var yy = 150 + i * 62, w = L[0] * .7;
          g.rect(rx, yy, w, 30, C.alu, C.aluE); for (var b = 0; b < L[1]; b++) g.circle(rx + w * (b + .5) / L[1], yy + 15, 5, "#d6dbe2");
          g.text(L[0] + " mm, " + L[1] + " bolt" + (L[1] > 1 ? "s" : ""), rx + w + 12, yy + 20, { size: 13 });
        });
        g.text("Same response per bolt at", rx, 352, { size: 13, color: C.ink3 });
        g.text("150 and 225 = the slice speaks", rx, 370, { size: 13, color: C.ink3 });
        g.text("for the whole seam", rx, 388, { size: 13, color: C.ink3 });
      } else {
        var gapF = run1 * .15 + run2 * .78 + fail * 1.5; // in units of the 0.11 mm limit
        g.bar(rx, 120, 230, "Gap between the cords", gapF, { max: 1.6, limit: 1, limitLabel: "0.11 mm limit" });
        var boltF = .25 * sealed + run1 * .05 + run2 * .22 + fail * .8;
        g.bar(rx, 196, 230, "Bolt load", boltF, { max: 1.1, marks: [[.25, "4 kN preload", C.acc]], color: C.acc });
        var pr = sealed * (fail > .68 ? 1 - ease(seg(fail, .68, .95)) * .85 : 1);
        g.bar(rx, 272, 230, "Air pressure between the cords", pr, { max: 1.1, color: C.meas });
        g.plot(rx, 340, 230, 80, {
          title: "Pull against time", color: C.force, xl: "time",
          fn: function (u) { var tt = 4 + u * 23; if (tt < 7.5) return 0; if (tt < 13.5) return Math.sin(Math.PI * seg(tt, 8, 13)) * .22; if (tt < 20.5) return Math.sin(Math.PI * seg(tt, 14, 20)) * .32; return ease(seg(tt, 21, 26.5)) * .95; },
          uEnd: clamp((t - 4) / 23, 0, 1)
        });
        g.text("bars show the shape only, not data", rx, 448, { size: 12, color: C.ink3 });
      }
    }
  };

  // =====================================================================
  // SA-550: face view of the 550 mm article
  // =====================================================================
  var S550 = {
    tag: "schematic face view; 550 mm long", dur: 31, still: 13,
    phases: [
      [0, "Dry fit: do the faces touch?", "No cord yet. A 0.05 mm feeler is tried along the joint; the faces must touch over the whole 550 mm and the holes must line up."],
      [3.5, "Cords in, bolts from the middle out", "The bolts are tightened in small steps from the middle out. At each step the face gap and the inner gap are read, giving squeeze against torque."],
      [8.5, "Bead, cure, end dams", "The RTV566 bead is laid and cured for 24 hours. End dams close the cut ends of the glands."],
      [11, "Leak test: 1 atm, then 2 atm", "Air goes into the space between the cords and is closed off. The pressure decay is logged for an hour, then at 2 atm, then each cord alone."],
      [17, "Shims: the smallest squeeze that seals", "A 0.1 mm and then a 0.2 mm shim under one face lowers the squeeze. The leak test is repeated each time."],
      [22, "Pry it open, read the leak against the gap", "Pulled in prying through the lugs. The gap at which the leak starts to rise is the real sealing limit, to set against the 0.11 mm requirement."],
      [28.5, "Keep it: the ageing sample", "The article stays assembled and is tested again after the slices, to see how the cords and the bead age."]
    ],
    draw: function (g, t) {
      var c = g.c, L = 550, s = 1.1, X0 = 60, Zt = 100, d = 180 * .9;
      function X(x) { return X0 + (x + 275) * s; }  // x from -275 to 275
      function Z(z) { return Zt + z * .9; }
      // frame face
      g.rect(X(-275), Z(0), L * s, d, C.alu, C.aluE, 1.2);
      // end dams
      var dam = ease(seg(t, 9.6, 10.6));
      if (t >= 9.6) { g.rect(X(-275) - 14 - (1 - dam) * 40, Z(-8), 14, d + 16, "#2d3138", C.steel2); g.rect(X(275) + (1 - dam) * 40, Z(-8), 14, d + 16, "#2d3138", C.steel2); }
      // hardpoint block z' 46-106, 200 long, three 40 mm pins at 60 mm pitch
      g.rect(X(-100), Z(46), 200 * s, 60 * .9, "#3a434f", C.aluE, 1);
      [-60, 0, 60].forEach(function (px) { g.circle(X(px), Z(76), 20 * .9 * .9, "#c9ced6", "#eef0f3", 1); });
      g.text("dummy hardpoint, on the line of the pull", X(0), Z(106) + 18, { size: 12, color: C.ink3, align: "center" });
      // bolts at z' 58: two each side
      var bolts = [-137.5, 137.5, -212.5, 212.5];
      var tighten = seg(t, 4, 8.5);
      bolts.forEach(function (bx, i) {
        var on = tighten * 4 > i ? 1 : 0;
        g.circle(X(bx), Z(58), 8, on ? C.acc : "#1b1f25", "#c8ccd2", 1.5);
      });
      // cords
      var cordIn = ease(seg(t, 3.6, 4.6));
      if (cordIn > 0) {
        [18, 32].forEach(function (z) {
          c.save(); c.globalAlpha = cordIn; g.line(X(-275), Z(z), X(-275) + L * s * cordIn, Z(z), C.cordE, 6); g.line(X(-275), Z(z), X(-275) + L * s * cordIn, Z(z), C.cord, 4); c.restore();
        });
      }
      // RTV bead drawn progressively
      var bead = seg(t, 8.6, 10);
      if (bead > 0) g.line(X(-275), Z(42), X(-275) + L * s * bead, Z(42), C.rtv, 4);
      if (t >= 8.6 && t < 11) g.clock(X(250), Z(130), 18, seg(t, 9, 10.8), "cure 24 h");
      // the air between the cords
      var pr = 0;
      if (t >= 11 && t < 17) {
        var u = seg(t, 11, 17);
        pr = u < .45 ? .5 : u < .85 ? 1 : .5;
        var only = u >= .85;
        g.rect(X(-275), Z(21), L * s, Z(29) - Z(21), "rgba(127,200,248," + (.35 + .45 * pr) + ")");
        if (only) g.text("vent one side: each cord alone", X(0), Z(180) + 40, { size: 13, color: C.meas, align: "center" });
      }
      // port (schematic position)
      g.circle(X(-245), Z(25), 4, C.meas); g.line(X(-245), Z(25), X(-245), Z(-24), C.meas, 2);
      g.text("port", X(-245) + 8, Z(-16), { size: 12, color: C.meas });
      // feeler in dry fit
      if (t < 3.5) {
        var st = [-200, 0, 200], k = Math.min(2, Math.floor(t / 1.15));
        st.forEach(function (sx, i) {
          if (i <= k) { g.text("touching", X(sx), Z(180) + 34, { size: 12, color: C.ok, align: "center" }); }
        });
        var fx = X(st[k]);
        g.poly([[fx - 3, Z(180) + 4], [fx + 3, Z(180) + 4], [fx + 3, Z(180) + 20], [fx - 3, Z(180) + 20]], C.acc);
        g.text("0.05 mm feeler", fx + 8, Z(180) + 18, { size: 12, color: C.acc });
      }
      // readouts in the right column
      var px0 = 700, py = 110, pw = 230, ph = 90;
      if (t < 3.5) g.text("joint face of frame B", X(275), Z(0) - 10, { size: 13, color: C.ink2, align: "right" });
      if (t >= 3.5 && t < 11) {
        g.plot(px0, py, pw, ph, {
          title: "Squeeze against torque (shape)", xl: "torque", color: C.acc,
          hlines: [[.72, "design squeeze", C.ok]],
          fn: function (u) { return .72 * (1 - Math.exp(-u * 3.4)) / (1 - Math.exp(-3.4)); }, uEnd: tighten
        });
      }
      if (t >= 11 && t < 22) {
        var shim = t >= 17;
        g.plot(px0, py, pw, ph, {
          title: shim ? "Decay with shims (shape only)" : "Pressure between the cords, 1 h holds", xl: "time", color: C.meas,
          fn: shim ? function (u) { return u < .5 ? .9 - u * .12 : .84 - (u - .5) * .9; }
                   : function (u) { return u < .45 ? .45 - u * .02 : .9 - (u - .45) * .03; },
          uEnd: shim ? seg(t, 17.5, 21.8) : seg(t, 11.2, 16.8)
        });
        if (shim) {
          // section inset showing the shim
          var ix = 230, iy = 330;
          g.text("Section at a shim", ix, iy - 8, { size: 13, color: C.ink2 });
          g.rect(ix, iy, 60, 80, C.alu, C.aluE); g.rect(ix + 66, iy, 60, 80, C.alu, C.aluE);
          g.rect(ix + 60, iy, 6, 80, C.acc);
          g.text(t < 19.5 ? "0.1 mm shim" : "0.2 mm shim", ix + 140, iy + 44, { size: 13, color: C.acc });
        }
      }
      if (t >= 22) {
        var pry = ease(seg(t, 22.5, 28));
        g.plot(px0, py, pw, ph, {
          title: "Leak against gap (shape)", xl: "gap", color: C.meas,
          hlines: [], fn: function (u) { return u < .55 ? .06 + u * .03 : .08 + Math.pow((u - .55) / .45, 2) * .9; }, uEnd: pry
        });
        var kx = px0 + pw * .55; g.line(kx, py, kx, py + ph, C.acc, 1.5, [4, 3]);
        if (pry > .6) g.text("this gap is", kx + 6, py + 16, { size: 12, color: C.acc }), g.text("the measurement", kx + 6, py + 32, { size: 12, color: C.acc });
        // prying arrows along the article (through the lugs on both pull blocks)
        // section inset: the two frames pried open about the cabin edge
        var sx = 300, sy = 312, sh = 110, sw = 50, th = pry * .09;
        g.text("Section: pried open about the cabin edge", sx - 120, sy - 10, { size: 13, color: C.ink2 });
        c.save(); c.translate(sx, sy + sh); c.rotate(-th); g.rect(-sw, -sh, sw, sh, C.alu, C.aluE); c.restore();
        c.save(); c.translate(sx, sy + sh); c.rotate(th); g.rect(0, -sh, sw, sh, C.alu, C.aluE); c.restore();
        g.poly([[sx - Math.sin(th) * sh, sy + (1 - Math.cos(th)) * sh], [sx + Math.sin(th) * sh, sy + (1 - Math.cos(th)) * sh], [sx, sy + sh]], "rgba(255,138,76,.25)");
        var ly = sy + 16;
        g.arrow(sx - sw - 4 - Math.sin(th) * (sh - 16), ly, sx - sw - 14 - 40 * pry, ly, C.force, 3.5);
        g.arrow(sx + sw + 4 + Math.sin(th) * (sh - 16), ly, sx + sw + 14 + 40 * pry, ly, C.force, 3.5);
        g.text("outer face", sx + sw + 60, sy + 6, { size: 12, color: C.ink3 });
        g.text("cabin face", sx + sw + 60, sy + sh, { size: 12, color: C.ink3 });
      }
      if (t >= 28.5) {
        g.rect(60, 300, 620, 140, C.bg);
        g.text("Stays assembled. Tested again after the slices,", 60, 350, { size: 15, color: C.ink2 });
        g.text("to see how the cords and the bead age.", 60, 372, { size: 15, color: C.ink2 });
      }
      // gauge on the right
      var gx = 815, gy = 330;
      g.circle(gx, gy, 38, "rgba(255,255,255,.04)", C.ink3, 1.5);
      var a = Math.PI * .75 + pr * Math.PI * 1.1;
      g.line(gx, gy, gx + Math.cos(a) * 30, gy + Math.sin(a) * 30, C.meas, 3);
      g.text("port pressure", gx, gy + 56, { size: 12, color: C.ink3, align: "center" });
    }
  };

  // =====================================================================
  // T2: quarter-scale panel on water
  // =====================================================================
  var T2 = {
    tag: "schematic section; 5 Oct article, to be redrawn for Rev F", dur: 27, still: 10.5,
    phases: [
      [0, "The panel on the membrane", "A 1:4 hexagon panel, cabin side down, on a 1 mm rubber membrane over water in a welded steel tub. A bridge carries the dial gauge over the hub."],
      [4, "Fill, bleed, check the relief valve", "About 165 litres of water go in from the floor; air is bled from the high point. The relief valve is tested before the panel sees pressure."],
      [7, "Pinned edge: three cycles", "Round bars under the top ring let the edge turn. The pressure goes up in steps and back down, three times. Every gauge is read at every step."],
      [14, "Clamped edge: three cycles", "The bars come out and the ring is tightened again. Three more cycles. The real seat is somewhere between pinned and clamped."],
      [20.5, "Small steps to the top pressure, behind the screen", "Only then does the pressure go up in small steps to the top. Water stores very little energy, which is why the test uses water and not air."]
    ],
    draw: function (g, t) {
      var c = g.c, x0 = 130, x1 = 600, cx = (x0 + x1) / 2, top = 190, floor = 360;
      // pressure staircase in 0..1 (1 = the top pressure)
      function stair(u, n, peak) { var k = Math.floor(u * n * 2), up = k < n ? k + 1 : 2 * n - k - 1; return clamp(up / n, 0, 1) * peak; }
      var P = 0, mode = "pinned";
      if (t >= 7 && t < 14) { var u = seg(t, 7.2, 13.8) * 3 % 1; P = stair(u, 4, .5); }
      if (t >= 14 && t < 20.5) { mode = "clamped"; var u2 = seg(t, 14.2, 20.3) * 3 % 1; P = stair(u2, 4, .5); }
      if (t >= 20.5) { mode = "clamped"; var u3 = seg(t, 21, 26.5); P = .5 + Math.floor(u3 * 10) / 10 * .5; }
      var water = t < 4 ? 0 : ease(seg(t, 4, 6));
      // tub
      g.rect(x0 - 26, top - 6, 22, floor - top + 30, "#3a3f47", C.steel2);
      g.rect(x1 + 4, top - 6, 22, floor - top + 30, "#3a3f47", C.steel2);
      g.rect(x0 - 26, floor, x1 - x0 + 52, 24, "#3a3f47", C.steel2);
      // water
      var wTop = top + 52;
      if (water > 0) g.rect(x0 - 4, lerp(floor, wTop, water), x1 - x0 + 8, floor - lerp(floor, wTop, water), C.water);
      // panel deflection shape (bulges up with pressure)
      var bulge = P * (mode === "pinned" ? 46 : 38);
      function yPanel(x) { var v = (x - x0) / (x1 - x0); var b = mode === "pinned" ? Math.sin(Math.PI * v) : Math.pow(Math.sin(Math.PI * v), 2); return wTop - 2 - bulge * b; }
      // membrane
      if (water > .5) { c.beginPath(); for (var i = 0; i <= 80; i++) { var x = lerp(x0 - 4, x1 + 4, i / 80); var y = yPanel(clamp(x, x0, x1)) + 2; if (i === 0) c.moveTo(x, y); else c.lineTo(x, y); } c.strokeStyle = "#111"; c.lineWidth = 3; c.stroke(); }
      // panes (thin plates) and ribs
      c.beginPath(); for (var j = 0; j <= 80; j++) { var xx = lerp(x0 + 18, x1 - 18, j / 80), yy = yPanel(xx) - 6; if (j === 0) c.moveTo(xx, yy); else c.lineTo(xx, yy); }
      c.strokeStyle = C.aluE; c.lineWidth = 4; c.stroke();
      [.22, .5, .78].forEach(function (v) { var xr = lerp(x0, x1, v), yr = yPanel(xr) - 8; g.rect(xr - 4, yr - 44, 8, 44, C.alu, C.aluE); g.rect(xr - 16, yr - 50, 32, 7, C.alu, C.aluE); });
      // hub
      var hy = yPanel(cx) - 8; g.rect(cx - 12, hy - 58, 24, 58, C.alu2, C.aluE);
      // frame bars at the edge
      [x0, x1 - 18].forEach(function (xf) { g.rect(xf, wTop - 78, 18, 76, C.alu, C.aluE); });
      // top ring and bolts
      g.rect(x0 - 26, wTop - 92, 70, 14, "#3a3f47", C.steel2); g.rect(x1 - 44, wTop - 92, 70, 14, "#3a3f47", C.steel2);
      [x0 - 14, x1 + 14].forEach(function (xb) { g.line(xb, wTop - 100, xb, top + 30, "#c8ccd2", 3); });
      if (mode === "pinned") { g.circle(x0 + 9, wTop - 82, 6, "#c8ccd2"); g.circle(x1 - 9, wTop - 82, 6, "#c8ccd2"); g.text("round bars: edge free to turn", x0 + 20, wTop - 102, { size: 12, color: C.ink3 }); }
      else g.text("clamped: edge held", x0 + 20, wTop - 102, { size: 12, color: C.ink3 });
      // bridge and dial gauge on the hub
      g.rect(x0 + 6, top - 70, x1 - x0 - 12, 8, "#2e333a", C.steel2);
      g.line(cx, top - 62, cx, hy - 58, C.meas, 2);
      g.circle(cx, top - 88, 18, "rgba(255,255,255,.05)", C.meas, 1.5);
      var a = -Math.PI / 2 + bulge / 46 * Math.PI * 1.4; g.line(cx, top - 88, cx + Math.cos(a) * 14, top - 88 + Math.sin(a) * 14, C.meas, 2.5);
      g.text("dial on the hub", cx + 26, top - 84, { size: 12, color: C.meas });
      // strain gauges glow with pressure
      [[.36, 0], [.64, 0], [.22, 1], [.78, 1]].forEach(function (q) { var gx = lerp(x0, x1, q[0]), gy = yPanel(gx) - (q[1] ? 54 : 10); g.rect(gx - 5, gy - 3, 10, 6, "rgba(255,138,76," + (.25 + .75 * P) + ")"); });
      // pipes: relief valve on the left wall, bleed at the high point
      g.line(x0 - 26, floor - 20, x0 - 64, floor - 20, C.waterE, 3); g.rect(x0 - 88, floor - 32, 24, 24, "#2e333a", C.steel2); g.text("relief valve", x0 - 76, floor - 42, { size: 12, color: C.ink3, align: "center" });
      if (t >= 5.6 && t < 7) { var f = seg(t, 5.6, 7); for (var k = 0; k < 6; k++) g.circle(x0 - 92 - f * 20 - k * 3, floor - 22 - k * 6 * f, 2.5, C.waterE); g.text("lifts: valve checked", 14, floor + 46, { size: 12, color: C.ok }); }
      if (t >= 4 && t < 6.2) { for (var b = 0; b < 5; b++) { var ph = (t * 1.3 + b / 5) % 1; g.circle(x1 - 30, lerp(floor - 20, wTop, ph), 3, null, "#cfe6ff", 1); } g.text("bleed", x1 - 50, wTop - 8, { size: 12, color: C.ink3 }); }
      // safety screen
      if (t >= 20.5) { g.rect(640, 120, 10, 290, "rgba(201,180,143,.35)", C.acc); g.text("screen", 645, 112, { size: 12, color: C.acc, align: "center" }); }
      // plan view of the hexagon with its panes and gauges
      var hx = 800, hyy = 120, R = 52;
      g.text("Plan, six panes (5 Oct article)", hx - 70, hyy - 64, { size: 12, color: C.ink3 });
      var hex = []; for (var m = 0; m < 6; m++) { var aa = Math.PI / 6 + m * Math.PI / 3; hex.push([hx + R * Math.cos(aa), hyy + R * Math.sin(aa)]); }
      g.poly(hex, "rgba(150,215,235,.18)", C.aluE, 1.5);
      hex.forEach(function (p) { g.line(hx, hyy, p[0], p[1], C.aluE, 1.5); });
      [[.45, 1], [.45, 4], [.7, 0]].forEach(function (q) { var aa = Math.PI / 6 + (q[1] + .5) * Math.PI / 3; g.rect(hx + R * q[0] * Math.cos(aa) - 4, hyy + R * q[0] * Math.sin(aa) - 3, 8, 6, C.force); });
      // pressure staircase plot
      g.plot(700, 260, 230, 120, {
        title: "Water pressure (October steps)", xl: "time", color: C.waterE, n: 700,
        hlines: [[.5, "1 atm", C.ink3], [1, "2 atm", C.ink3]],
        fn: function (u) {
          var tt = 7 + u * 20, v;
          if (tt < 14) v = stair(seg(tt, 7.2, 13.8) * 3 % 1, 4, .5);
          else if (tt < 20.5) v = stair(seg(tt, 14.2, 20.3) * 3 % 1, 4, .5);
          else v = .5 + Math.floor(seg(tt, 21, 26.5) * 10) / 10 * .5;
          return v;
        }, uEnd: clamp((t - 7) / 20, 0, 1)
      });
      g.text(mode === "pinned" ? "pinned" : "clamped", 700, 410, { size: 13, color: C.ink2 });
      g.text("to be restated against 12.3 psia", 700, 430, { size: 12, color: C.ink3 });
    }
  };

  // =====================================================================
  // T3: the corner, plan view
  // =====================================================================
  var T3 = {
    tag: "schematic plan view; limits and model values from C1 (5 Nov)", dur: 21, still: 15,
    phases: [
      [0, "Three panels meet at one corner", "Two hexagons and a pentagon. Each panel corner is a machined block; ties through the blocks hold the corner shut."],
      [4, "Set the ties by stretch, not torque", "The ties are brought to their preload and the stretch is read on each one, because torque scatters too much."],
      [7.5, "Pull along the seats, in steps", "Each panel is pulled away from the corner along its seat, the way pressure loads it, and held at each step."],
      [16, "Compare with the model", "The tie force and the face opening are compared with the corner model and with their limits."]
    ],
    draw: function (g, t) {
      var c = g.c, cx = 330, cy = 236, R = 140;
      var pre = ease(seg(t, 4, 7)), pull = t >= 7.5 ? Math.floor(seg(t, 7.8, 15.6) * 4.0001) / 4 : 0;
      if (t >= 16) pull = 1;
      var open = pull * 12;
      var names = ["hexagon", "hexagon", "pentagon"];
      for (var i = 0; i < 3; i++) {
        var a0 = -Math.PI / 2 + i * 2 * Math.PI / 3, a1 = a0 + 2 * Math.PI / 3, am = (a0 + a1) / 2;
        var ox = Math.cos(am) * open, oy = Math.sin(am) * open;
        var pts = [[cx + ox, cy + oy]];
        for (var k = 0; k <= 12; k++) { var aa = a0 + (a1 - a0) * k / 12; pts.push([cx + ox + R * Math.cos(aa) * .98, cy + oy + R * Math.sin(aa) * .98]); }
        g.poly(pts, i === 2 ? "rgba(201,180,143,.16)" : "rgba(150,215,235,.12)", C.line, 1);
        // the corner block
        var bpts = [[cx + ox, cy + oy]];
        for (var k2 = 0; k2 <= 6; k2++) { var ab = a0 + .07 + (a1 - a0 - .14) * k2 / 6; bpts.push([cx + ox + 62 * Math.cos(ab), cy + oy + 62 * Math.sin(ab)]); }
        g.poly(bpts, C.alu, C.aluE, 1.2);
        g.text(names[i], cx + ox + 120 * Math.cos(am), cy + oy + 120 * Math.sin(am) + 5, { size: 14, color: C.ink2, align: "center" });
        // pull arrows along the seat
        if (t >= 7.5) {
          var ax = cx + ox + (R + 12) * Math.cos(am), ay = cy + oy + (R + 12) * Math.sin(am);
          g.arrow(ax, ay, ax + Math.cos(am) * (22 + 46 * pull), ay + Math.sin(am) * (22 + 46 * pull), C.force, 4);
        }
        // ties across the face between this block and the next
        var af = a1, n = [Math.cos(af), Math.sin(af)], perp = [-Math.sin(af), Math.cos(af)];
        for (var q = 0; q < 2; q++) {
          var r = 26 + q * 22, mx = cx + n[0] * r, my = cy + n[1] * r;
          var lw = 3 + 2 * pre;
          g.line(mx - perp[0] * 16, my - perp[1] * 16, mx + perp[0] * 16, my + perp[1] * 16, pre > .1 ? C.acc : "#c8ccd2", lw);
        }
      }
      if (t < 4) {
        g.text("corner blocks, machined from plate", cx + 70, cy + 4, { size: 12, color: C.ink3 });
        g.text("seams between the panels", cx - 230, cy + 150, { size: 12, color: C.ink3 });
      }
      // readouts
      var rx = 650;
      var tie = 198 + pull * (214.5 - 198);
      g.bar(rx, 130, 260, "Worst corner tie (kN)", pre ? tie : 0, {
        max: 240, limit: 227, limitLabel: "227 limit", color: C.acc,
        marks: t >= 16 ? [[198, "198 preload", C.ink3, 16], [214.5, "214.5 model at proof", C.meas, -50]] : [[198, "198 preload", C.ink3, 16]]
      });
      g.bar(rx, 230, 260, "Corner faces open (mm)", pull * .55, {
        max: 1, limit: .8, limitLabel: "0.8 the seal takes", color: C.meas,
        marks: t >= 16 ? [[.55, "0.55 model at proof", C.meas, -50]] : []
      });
      g.text("Model values at 0.8 atm, proof pressure.", rx, 320, { size: 13, color: C.ink2 });
      g.text("With the hatch open (1 atm) the tie reaches", rx, 340, { size: 13, color: C.ink3 });
      g.text("226.3 kN, 0.7 kN under the limit.", rx, 360, { size: 13, color: C.ink3 });
      g.text("Runs at 180 and 160 kN preload are on", rx, 392, { size: 13, color: C.ink3 });
      g.text("the laptop now.", rx, 412, { size: 13, color: C.ink3 });
    }
  };

  // =====================================================================
  // Proposed: tap test
  // =====================================================================
  var TAP = {
    tag: "proposed; 600 Hz and Q 10 are hand estimates", dur: 13, still: 6,
    phases: [
      [0, "The pane in its clamp", "One 531 mm pane of 21 mm glass, held by the proposed clamp bars on rubber strips. An accelerometer is glued near the middle."],
      [2.5, "Tap", "A small instrumented hammer taps the pane."],
      [3.5, "It rings, and the ring dies away", "How fast it rings is the first mode. How fast the ring dies away is the damping."],
      [8.5, "Read the frequency", "The spectrum shows the peak; the decay gives the damping. Both replace guesses in the launch vibration model."]
    ],
    draw: function (g, t) {
      var cx = 300, cy = 270, R = 170;
      var tri = [[cx, cy - R], [cx + R * .866, cy + R * .5], [cx - R * .866, cy + R * .5]];
      var ring = t >= 3 ? Math.exp(-(t - 3) * .9) : 0;
      var off = ring * Math.sin(t * 40) * 3;
      g.poly(tri.map(function (p) { return [p[0], p[1] + off * (p === tri[0] ? 0 : 0)]; }), C.glass, C.glassE, 1.5);
      // clamp bars on the edges
      for (var i = 0; i < 3; i++) { var a = tri[i], b = tri[(i + 1) % 3]; g.line(a[0], a[1], b[0], b[1], C.steel2, 9); g.line(a[0], a[1], b[0], b[1], "#262a30", 3); }
      g.rect(cx - 9, cy - 9 + off, 18, 18, C.acc); g.text("accelerometer", cx + 16, cy + 4, { size: 12, color: C.acc });
      // hammer
      var hp = t < 2.5 ? 0 : t < 3 ? seg(t, 2.5, 3) : 1 - seg(t, 3, 3.6);
      var hx = cx - 40, hy = cy - 40 - 60 * (1 - hp);
      g.line(hx - 60, hy - 50, hx, hy, "#c8ccd2", 4); g.circle(hx, hy, 9, C.force);
      if (t >= 3 && t < 3.5) g.circle(hx, hy, 18, null, C.force, 2);
      // time trace
      g.plot(620, 110, 300, 110, {
        title: "Acceleration against time", xl: "time", color: C.meas,
        fn: function (u) { var tt = u * 5; return .5 + .45 * Math.exp(-tt * 1.1) * Math.sin(tt * 34); }, uEnd: t >= 3 ? clamp((t - 3) / 5, 0, 1) : 0
      });
      if (t >= 8.5) {
        g.plot(620, 290, 300, 110, {
          title: "Spectrum", xl: "frequency", color: C.acc,
          fn: function (u) { var d = (u - .45) / .05; return .06 + .85 / (1 + d * d); }, uEnd: seg(t, 8.5, 10.5)
        });
        g.text("first mode", 620 + 300 * .45 + 14, 290 + 22, { size: 12, color: C.acc }); g.text("(hand estimate about 600 Hz)", 620 + 300 * .45 + 14, 290 + 38, { size: 12, color: C.acc });
        g.text("width of the peak = damping", 620 + 300 * .45, 424, { size: 12, color: C.ink3, align: "center" });
      }
    }
  };

  // =====================================================================
  // Proposed: cold soak
  // =====================================================================
  var COLD = {
    tag: "proposed; no chamber yet", dur: 15, still: 8,
    phases: [
      [0, "The 550 article in a cold box", "The assembled 550 article goes into a box packed with dry ice. The port line and the gauge wires come out through the lid."],
      [3, "Cool to minus 40 C", "The part cools slowly. The bolt load, the pressure between the cords and the gap across the joint are read all the way down."],
      [9.5, "Hold, then back to room temperature", "If the pressure holds at minus 40 C with the bolt load as predicted, the cold limit is set by the rubber, not by the squeeze."]
    ],
    draw: function (g, t) {
      var bx = 70, by = 130, bw = 520, bh = 260;
      g.rect(bx, by, bw, bh, "rgba(255,255,255,.03)", C.ink3, 2);
      g.rect(bx - 6, by - 18, bw + 12, 18, "#2e333a", C.steel2);
      for (var i = 0; i < 9; i++) { var x = bx + 20 + i * 56; g.rect(x, by + bh - 54, 40, 34, "rgba(230,240,250,.18)", "rgba(230,240,250,.5)"); g.rect(x + 10, by + 20, 30, 26, "rgba(230,240,250,.18)", "rgba(230,240,250,.5)"); }
      g.rect(bx + 60, by + 96, 400, 70, C.alu, C.aluE); g.line(bx + 60, by + 131, bx + 460, by + 131, "#1b1f25", 2);
      g.text("550 article", bx + 260, by + 136, { size: 14, color: C.ink, align: "center" });
      g.line(bx + 120, by + 96, bx + 120, by - 50, C.meas, 2); g.text("port line out", bx + 128, by - 36, { size: 12, color: C.meas });
      var temp = t < 3 ? 20 : t < 9.5 ? lerp(20, -40, ease(seg(t, 3, 9))) : lerp(-40, 20, ease(seg(t, 10.5, 15)));
      // thermometer
      var tx = 640, ty = 150, th = 200, f = (temp + 50) / 80;
      g.rect(tx, ty, 16, th, "rgba(255,255,255,.04)", C.ink3);
      g.rect(tx + 3, ty + th - th * f, 10, th * f, temp < 0 ? C.meas : C.force);
      g.text(Math.round(temp) + " C", tx + 26, ty + th - th * f + 5, { size: 15, weight: 600, color: C.ink });
      g.plot(720, 150, 210, 90, {
        title: "Part temperature", xl: "time", color: C.meas,
        fn: function (u) { var tt = u * 15, v = tt < 3 ? 20 : tt < 9.5 ? lerp(20, -40, ease(seg(tt, 3, 9))) : lerp(-40, 20, ease(seg(tt, 10.5, 15))); return (v + 50) / 80; }, uEnd: t / 15
      });
      g.plot(720, 300, 210, 90, {
        title: "Pressure between the cords", xl: "time", color: C.ok,
        fn: function () { return .7; }, uEnd: t / 15
      });
      g.text("holds? (prediction filed after the", 720, 414, { size: 12, color: C.ink3 });
      g.text("cold model is rerun with butyl)", 720, 430, { size: 12, color: C.ink3 });
    }
  };

  var SCENES = { t0: T0, t1: T1, t550: S550, t2: T2, t3: T3, tap: TAP, cold: COLD };

  // ---------- player ----------
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function Player(fig) {
    var id = fig.getAttribute("data-scene"); this.scene = SCENES[id]; if (!this.scene) return;
    this.fig = fig; this.cv = fig.querySelector("canvas");
    var dpr = Math.min(window.devicePixelRatio || 1, 2); this.cv.width = W * dpr; this.cv.height = H * dpr;
    this.ctx = this.cv.getContext("2d"); this.ctx.scale(dpr, dpr); this.g = new G(this.ctx);
    this.t = this.scene.still; this.playing = false; this.visible = false; this.last = 0; this.k = -1;
    this.btn = fig.querySelector(".play"); this.title = fig.querySelector(".ph-title"); this.txt = fig.querySelector(".ph-text");
    this.bar = fig.querySelector(".prog i");
    var self = this, steps = fig.querySelector(".steps");
    this.chips = this.scene.phases.map(function (p, i) {
      var b = document.createElement("button"); b.type = "button"; b.textContent = (i + 1) + ". " + p[1];
      b.addEventListener("click", function () { self.t = p[0] + .01; self.render(); });
      steps.appendChild(b); return b;
    });
    this.btn.addEventListener("click", function () { self.playing = !self.playing; self.sync(); if (self.playing) self.loop(); });
    fig.querySelector(".restart").addEventListener("click", function () { self.t = 0; self.playing = true; self.sync(); self.render(); self.loop(); });
    this.render(); this.sync();
  }
  Player.prototype.sync = function () { this.btn.textContent = this.playing ? "Pause" : "Play"; this.btn.setAttribute("aria-pressed", this.playing ? "true" : "false"); };
  Player.prototype.render = function () {
    var s = this.scene; this.g.c.save(); background(this.g, s, this.t); s.draw(this.g, this.t); this.g.c.restore();
    var k = phaseAt(s, this.t);
    if (k !== this.k) {
      this.k = k; this.title.textContent = (k + 1) + ". " + s.phases[k][1]; this.txt.textContent = s.phases[k][2];
      this.chips.forEach(function (b, i) { b.classList.toggle("on", i === k); });
    }
    if (this.bar) this.bar.style.width = (100 * this.t / s.dur).toFixed(1) + "%";
  };
  Player.prototype.loop = function () {
    var self = this; if (this.raf) return;
    function step(ts) {
      self.raf = 0;
      if (!self.playing) return;
      if (!self.visible) { self.last = 0; self.raf = requestAnimationFrame(step); return; }
      var dt = self.last ? Math.min(.05, (ts - self.last) / 1000) : 0; self.last = ts;
      self.t += dt; if (self.t >= self.scene.dur) self.t = 0;
      self.render(); self.raf = requestAnimationFrame(step);
    }
    this.last = 0; this.raf = requestAnimationFrame(step);
  };

  function init() {
    var figs = document.querySelectorAll("figure.anim[data-scene]"), players = [];
    for (var i = 0; i < figs.length; i++) { var p = new Player(figs[i]); if (p.scene) { players.push(p); figs[i].classList.add("live"); } }
    var auto = !reduce && !/[?&]still/.test(location.search);
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          var p = players.filter(function (q) { return q.fig === e.target; })[0]; if (!p) return;
          p.visible = e.isIntersecting;
          if (p.visible && auto && !p.started) { p.started = true; p.t = 0; p.playing = true; p.sync(); p.loop(); }
        });
      }, { threshold: .35 });
      players.forEach(function (p) { io.observe(p.fig); });
    } else players.forEach(function (p) { p.visible = true; });
    // redraw once fonts are in, so canvas labels use the page font
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { players.forEach(function (p) { p.render(); }); });
    window.__hcsaPlayers = players;
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
