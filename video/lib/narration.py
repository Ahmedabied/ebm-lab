"""Voice <-> picture lock. The scene drives the timeline: say(pid) notes the scene time at which that
paragraph's audio starts (after the previous one has finished), until(pid, word) waits until a spoken
word, end(pid) waits for the paragraph to finish. finish() writes audio/<ch>/timeline.json, which
build.sh uses to place each paragraph's audio at the exact offset. If a paragraph's audio does not
exist yet, its duration is estimated (chars / 16 per second) so scenes can be developed first."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__)); AUDIO = os.path.join(HERE, "..", "audio")
GAP = 0.45     # seconds of silence between paragraphs


class Narration:
    def __init__(self, scene, chapter):
        self.scene = scene; self.chapter = chapter
        self.dir = os.path.join(AUDIO, chapter)
        self.man = json.load(open(os.path.join(self.dir, "manifest.json")))
        self.paras = {p["id"]: p for p in self.man["paragraphs"]}
        self.order = [p["id"] for p in self.man["paragraphs"]]
        self.start = {}; self.last_end = 0.0; self.current = None

    def duration(self, pid):
        p = self.paras[pid]
        return p["duration"] if p.get("duration") else len(p["text"]) / 16.0

    def text(self, pid):
        return self.paras[pid]["text"]

    def wait_until(self, t):
        dt = t - self.scene.time
        if dt > 1e-3:
            self.scene.wait(dt)

    def say(self, pid):
        """Start paragraph pid now (or as soon as the previous one has ended). Returns its duration."""
        self.wait_until(self.last_end + (GAP if self.start else 0.0))
        self.start[pid] = self.scene.time
        self.current = pid
        self.last_end = self.start[pid] + self.duration(pid)
        return self.duration(pid)

    def t_word(self, pid, word, occurrence=0):
        """Scene time at which `word` (case-insensitive, punctuation stripped) starts in pid."""
        ws = self.paras[pid].get("words") or []
        norm = lambda s: "".join(ch for ch in s.lower() if ch.isalnum())
        hits = [w for w in ws if norm(w["w"]) == norm(word)]
        if not hits or pid not in self.start:
            # no timestamps: estimate by character position
            txt = self.text(pid); i = txt.lower().find(word.lower())
            frac = (i / max(len(txt), 1)) if i >= 0 else 0.0
            return self.start.get(pid, self.scene.time) + frac * self.duration(pid)
        return self.start[pid] + hits[min(occurrence, len(hits) - 1)]["s"]

    def until(self, pid, word, occurrence=0, lead=0.15):
        """Wait until just before the word is spoken (lead seconds early so the picture lands with it)."""
        self.wait_until(self.t_word(pid, word, occurrence) - lead)

    def remaining(self, pid=None):
        pid = pid or self.current
        return max(0.0, self.start[pid] + self.duration(pid) - self.scene.time)

    def end(self, pid=None, extra=0.0):
        pid = pid or self.current
        self.wait_until(self.start[pid] + self.duration(pid) + extra)

    def finish(self, tail=1.0):
        self.wait_until(self.last_end + tail)
        json.dump({"chapter": self.chapter, "starts": self.start, "total": self.scene.time},
                  open(os.path.join(self.dir, "timeline.json"), "w"), indent=1)
        # every real number the scene showed, for out/PROVENANCE.md (lib.data.note)
        from . import data as _d
        json.dump([{"label": l, "file": f, "field": fi, "value": str(v)} for l, f, fi, v in _d.PROVENANCE],
                  open(os.path.join(self.dir, "provenance.json"), "w"), indent=1)
