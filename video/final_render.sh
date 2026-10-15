#!/usr/bin/env bash
# Final build: render all chapters at 1080p60 in parallel (P at a time), then mux, concat, provenance.
set -euo pipefail; cd "$(dirname "$0")"
P=${P:-5}; Q=${Q:-qh}
printf "%s\n" 00 01 02 03 04 05 06 07 08 09 | xargs -P "$P" -I{} bash -c "./build.sh render $Q {} > /tmp/claude-1000/render-{}.log 2>&1; echo 'done {}'"
./build.sh mux "$Q" && ./build.sh concat "$Q" && .venv/bin/python provenance.py
echo FINAL_BUILD_DONE
