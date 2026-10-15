#!/usr/bin/env bash
# Build the lesson. Usage:
#   ./build.sh render ql|qm|qh [chapters...]   # render scenes (ql=480p15 for QC, qh=1080p60 final)
#   ./build.sh mux   ql|qm|qh [chapters...]    # place each paragraph's audio at its timeline offset
#   ./build.sh concat ql|qm|qh                 # join chapters -> out/ebm-lab-lesson-01.mp4 + chapters.txt
#   ./build.sh qc    ql|qm|qh chapter          # contact sheet of frames every 10 s -> out/qc/
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
MANIM=.venv/bin/manim; PY=.venv/bin/python
cmd=$1; q=${2:-ql}; shift 2 || true
case $q in ql) dir=480p15; fps=15;; qm) dir=720p30; fps=30;; qh) dir=1080p60; fps=60;; esac
ALL=(00 01 02 03 04 05 06 07 08 09)
chs=("$@"); [ ${#chs[@]} -eq 0 ] && chs=("${ALL[@]}")
case $cmd in
render)
  for c in "${chs[@]}"; do
    echo "== render $c ($q)"; $MANIM -$q --fps $fps --disable_caching -o ch$c.mp4 scenes/ch$c.py Ch$c 2>&1 | grep -E "File ready|Error|Traceback|error" || true
  done;;
mux)
  for c in "${chs[@]}"; do
    vid=media/videos/ch$c/$dir/ch$c.mp4; tl=audio/$c/timeline.json; man=audio/$c/manifest.json
    $PY - "$vid" "$tl" "$man" "out/ch$c.$q.mp4" <<'PY'
import json, sys, subprocess, os
vid, tl, man, out = sys.argv[1:5]
starts = json.load(open(tl))["starts"]; paras = json.load(open(man))["paragraphs"]
inputs = ["-i", vid]; filt = []; labels = []
k = 1
for p in paras:
    if p["id"] not in starts or not p.get("file"): continue
    f = os.path.join(os.path.dirname(man), p["file"]); ms = int(round(starts[p["id"]] * 1000))
    inputs += ["-i", f]; filt.append(f"[{k}]aresample=48000,adelay={ms}|{ms}[a{k}]"); labels.append(f"[a{k}]"); k += 1
if not labels: print("no audio for", man); sys.exit(0)
filt.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,aresample=48000[aout]")
cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[aout]",
       "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out]
subprocess.run(cmd, check=True); print("muxed", out)
PY
  done;;
concat)
  : > out/concat.txt; : > out/chapters.txt; t=0
  for c in "${ALL[@]}"; do
    f=out/ch$c.$q.mp4; [ -f "$f" ] || continue
    echo "file '$(pwd)/$f'" >> out/concat.txt
    title=$(grep -m1 '^# ' script/${c}_*.md | sed 's/^# [0-9]* — //')
    printf "%02d:%02d:%02d %s\n" $((t/3600)) $(((t%3600)/60)) $((t%60)) "$title" >> out/chapters.txt
    d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f"); t=$(python3 -c "print(int($t + $d + 0.5))")
  done
  ffmpeg -y -loglevel error -f concat -safe 0 -i out/concat.txt -c copy out/ebm-lab-lesson-01.$q.mp4
  echo "wrote out/ebm-lab-lesson-01.$q.mp4"; cat out/chapters.txt;;
qc)
  c=${chs[0]}; mkdir -p out/qc/$c; rm -f out/qc/$c/*.png
  src=out/ch$c.$q.mp4; [ -f "$src" ] || src=media/videos/ch$c/$dir/ch$c.mp4
  ffmpeg -y -loglevel error -i "$src" -vf "fps=1/10,scale=640:-1" out/qc/$c/f%03d.png
  n=$(ls out/qc/$c/f*.png | wc -l); cols=4; rows=$(( (n + cols - 1) / cols ))
  ffmpeg -y -loglevel error -pattern_type glob -i "out/qc/$c/f*.png" -vf "tile=${cols}x${rows}:padding=4:color=black" out/qc/$c/sheet.png
  echo "out/qc/$c/sheet.png ($n frames, every 10 s)";;
esac
