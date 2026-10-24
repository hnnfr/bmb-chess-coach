#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Render a chess_engine.py analysis (plus optional narrative annotations) into
a single self-contained, interactive HTML artifact: a replayable board with
forward/backward navigation and an eval graph.

This is a pure, deterministic transformation — JSON in, HTML out — which is
why it is a script. The narrative text for each turning point is judgment
and comes from the capability prompt as the `annotations` input; this script
never invents commentary, it only lays out what it is given.

Usage:
    uv run render_board.py <analysis.json> [--annotations annotations.json] -o out.html

    analysis.json:     chess_engine.py's JSON output
    annotations.json:  optional {"<ply>": "narrative text"} map, keyed by ply number
"""

import argparse
import json
from pathlib import Path

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Game Analysis — __SUBJECT__</title>
<style>
  :root { --bg:#0f1b2d; --panel:#16263d; --ink:#e9eef6; --ink-dim:#9fb0c7; --line:#294366;
          --accent:#b66d46; --light:#e9dcc9; --dark:#5a7a94; --tp:#d8c24a; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font:15px/1.5 -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
  .wrap { max-width: 920px; margin: 0 auto; padding: 24px 18px 60px; }
  h1 { font-size: 20px; margin: 0 0 4px; }
  .meta { color: var(--ink-dim); font-size: 13px; margin-bottom: 18px; }
  .layout { display: flex; gap: 20px; flex-wrap: wrap; }
  .board-col { flex: 0 0 auto; }
  .side-col { flex: 1 1 320px; min-width: 280px; }
  #board { display: grid; grid-template-columns: repeat(8, 44px); grid-template-rows: repeat(8, 44px);
           border: 2px solid var(--line); border-radius: 6px; overflow: hidden; }
  .sq { display: flex; align-items: center; justify-content: center; font-size: 28px; user-select: none; }
  .sq.light { background: var(--light); color: #2a2a2a; }
  .sq.dark { background: var(--dark); color: #1a1a1a; }
  .controls { display: flex; gap: 8px; margin-top: 10px; }
  button { font: inherit; cursor: pointer; border-radius: 8px; border: 1px solid var(--line);
           background: var(--panel); color: var(--ink); padding: 8px 14px; }
  button:disabled { opacity: 0.4; cursor: default; }
  button.tp { border-color: var(--tp); color: var(--tp); }
  .movelabel { margin-top: 8px; font-size: 14px; color: var(--ink-dim); }
  .panel { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 14px; margin-bottom: 14px; }
  .panel h2 { font-size: 12px; text-transform: uppercase; letter-spacing: .05em; color: var(--ink-dim); margin: 0 0 8px; }
  #eval-graph { width: 100%; height: 90px; display: block; }
  #annotation { min-height: 60px; }
  #annotation.empty { color: var(--ink-dim); font-style: italic; }
  .tp-list { list-style: none; margin: 0; padding: 0; max-height: 180px; overflow-y: auto; }
  .tp-list li { padding: 6px 8px; border-radius: 6px; cursor: pointer; font-size: 13px; }
  .tp-list li:hover { background: var(--line); }
  .tp-list li.active { background: var(--accent); color: #1a0e07; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Game Analysis</h1>
  <div class="meta" id="meta">__META__</div>
  <div class="layout">
    <div class="board-col">
      <div id="board"></div>
      <div class="controls">
        <button id="first">⏮</button>
        <button id="prev">◀</button>
        <button id="next">▶</button>
        <button id="last">⏭</button>
      </div>
      <div class="movelabel" id="movelabel"></div>
    </div>
    <div class="side-col">
      <div class="panel">
        <h2>Evaluation (White's perspective)</h2>
        <svg id="eval-graph"></svg>
      </div>
      <div class="panel">
        <h2>Turning Points</h2>
        <ul class="tp-list" id="tp-list"></ul>
      </div>
      <div class="panel">
        <h2>Notes on this position</h2>
        <div id="annotation" class="empty">No note for this move.</div>
      </div>
    </div>
  </div>
</div>

<script type="application/json" id="game-data">__DATA__</script>
<script>
(function () {
  "use strict";
  var data = JSON.parse(document.getElementById("game-data").textContent);
  var moves = data.moves;
  var turningPoints = data.turning_points || [];
  var annotations = data.annotations || {};
  var PIECES = { K:"♔",Q:"♕",R:"♖",B:"♗",N:"♘",P:"♙", k:"♚",q:"♛",r:"♜",b:"♝",n:"♞",p:"♟" };
  var START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
  var boardEl = document.getElementById("board");
  var idx = -1; // -1 = start position, 0..moves.length-1 = after that move

  function fenAt(i) { return i < 0 ? START_FEN : moves[i].fen_after; }

  function renderBoard(fen) {
    var rows = fen.split(" ")[0].split("/");
    boardEl.innerHTML = "";
    for (var r = 0; r < 8; r++) {
      var file = 0;
      for (var c = 0; c < rows[r].length; c++) {
        var ch = rows[r][c];
        if (/[1-8]/.test(ch)) {
          for (var k = 0; k < parseInt(ch, 10); k++) { addSquare(r, file, ""); file++; }
        } else {
          addSquare(r, file, PIECES[ch] || "");
          file++;
        }
      }
    }
  }

  function addSquare(r, file, glyph) {
    var sq = document.createElement("div");
    var light = (r + file) % 2 === 0;
    sq.className = "sq " + (light ? "light" : "dark");
    sq.textContent = glyph;
    boardEl.appendChild(sq);
  }

  function renderEvalGraph() {
    var svg = document.getElementById("eval-graph");
    var w = 300, h = 90;
    svg.setAttribute("viewBox", "0 0 " + w + " " + h);
    var vals = [0].concat(moves.map(function (m) { return m.eval_after_white_cp; }));
    var clamped = vals.map(function (v) { return Math.max(-800, Math.min(800, v)); });
    var n = clamped.length;
    var pts = clamped.map(function (v, i) {
      var x = n <= 1 ? 0 : (i / (n - 1)) * w;
      var y = h / 2 - (v / 800) * (h / 2 - 4);
      return x.toFixed(1) + "," + y.toFixed(1);
    });
    var tpMarks = turningPoints.map(function (ply) {
      var i = ply; // ply is 1-indexed into moves == index i in the (0-padded) vals array
      var x = n <= 1 ? 0 : (i / (n - 1)) * w;
      var y = h / 2 - (clamped[i] / 800) * (h / 2 - 4);
      return '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="3.5" fill="#d8c24a" />';
    }).join("");
    svg.innerHTML =
      '<line x1="0" y1="' + (h/2) + '" x2="' + w + '" y2="' + (h/2) + '" stroke="#294366" stroke-width="1" />' +
      '<polyline points="' + pts.join(" ") + '" fill="none" stroke="#e9eef6" stroke-width="1.5" />' +
      tpMarks;
  }

  function renderTpList() {
    var ul = document.getElementById("tp-list");
    ul.innerHTML = "";
    if (!turningPoints.length) {
      ul.innerHTML = "<li>No turning points flagged.</li>";
      return;
    }
    turningPoints.forEach(function (ply) {
      var m = moves[ply - 1];
      var li = document.createElement("li");
      li.textContent = ply + ". " + (m ? m.san : "?") + " (" + (m ? m.delta_for_mover_cp : "?") + " cp for mover)";
      li.addEventListener("click", function () { goTo(ply - 1); });
      ul.appendChild(li);
    });
  }

  function update() {
    renderBoard(fenAt(idx));
    var label = idx < 0 ? "Start position" :
      ("Move " + moves[idx].ply + ": " + moves[idx].mover + " played " + moves[idx].san +
       " (" + moves[idx].delta_for_mover_cp + " cp for mover)");
    document.getElementById("movelabel").textContent = label;

    var ply = idx + 1;
    var note = annotations[String(ply)];
    var box = document.getElementById("annotation");
    if (note) { box.textContent = note; box.classList.remove("empty"); }
    else { box.textContent = "No note for this move."; box.classList.add("empty"); }

    document.getElementById("first").disabled = idx <= -1;
    document.getElementById("prev").disabled = idx <= -1;
    document.getElementById("next").disabled = idx >= moves.length - 1;
    document.getElementById("last").disabled = idx >= moves.length - 1;

    document.querySelectorAll(".tp-list li").forEach(function (li, i) {
      li.classList.toggle("active", turningPoints[i] === ply);
    });
  }

  function goTo(i) { idx = Math.max(-1, Math.min(moves.length - 1, i)); update(); }

  document.getElementById("first").addEventListener("click", function () { goTo(-1); });
  document.getElementById("prev").addEventListener("click", function () { goTo(idx - 1); });
  document.getElementById("next").addEventListener("click", function () { goTo(idx + 1); });
  document.getElementById("last").addEventListener("click", function () { goTo(moves.length - 1); });

  renderEvalGraph();
  renderTpList();
  update();
})();
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("analysis", help="Path to chess_engine.py's JSON output")
    parser.add_argument("--annotations", help="Path to a JSON map of {ply: narrative text}")
    parser.add_argument("-o", "--output", required=True, help="Output HTML file path")
    args = parser.parse_args()

    analysis = json.loads(Path(args.analysis).read_text(encoding="utf-8"))
    annotations = {}
    if args.annotations:
        annotations = json.loads(Path(args.annotations).read_text(encoding="utf-8"))

    data = dict(analysis)
    data["annotations"] = annotations

    subject = f"{analysis.get('white', '?')} vs {analysis.get('black', '?')}"
    meta = f"{subject} · result: {analysis.get('result', '?')} · depth {analysis.get('depth', '?')}"

    html = (
        HTML_TEMPLATE
        .replace("__SUBJECT__", subject)
        .replace("__META__", meta)
        .replace("__DATA__", json.dumps(data))
    )
    Path(args.output).write_text(html, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
