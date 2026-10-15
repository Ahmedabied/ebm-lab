"""Narration audio for the lesson. One file per script paragraph, cached by (engine, voice, text) hash so
re-running after a script edit only regenerates the paragraphs that changed (and never re-spends
ElevenLabs characters on an unchanged paragraph).

  uv run --project . python tts.py kokoro 02 03 ...      # local voice (free)
  uv run --project . python tts.py eleven 00 01           # ElevenLabs v4 (10k chars/month on the free tier)
  uv run --project . python tts.py manifest               # (re)write every chapter's manifest.json

Outputs per chapter: audio/<chapter>/<pNN>.wav|mp3, <pNN>.json {text, duration, words:[{w,s,e}]},
and audio/<chapter>/manifest.json listing the paragraphs in order with their viz notes.
"""
import sys, os, re, json, hashlib, glob, time
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "script"); AUDIO = os.path.join(HERE, "audio")
ELEVEN_VOICE = ("Bella", "hpp4J3VqNfWAUOO0d1Us")        # professional, bright, warm, educational (brief: Bella or Alice over Jessica)
ELEVEN_MODEL = "eleven_v4"
KOKORO_VOICE = "af_heart"                              # Kokoro-82M, grade-A American female


def parse(chapter_file):
    s = open(chapter_file).read()
    head = s.split("\n## ", 1)[0]
    voice = re.search(r"^voice:\s*(\w+)", head, re.M).group(1)
    title = re.search(r"^# (.+)$", head, re.M).group(1).strip()
    paras = []
    for m in re.finditer(r"^## (p\d+)\s*\|\s*viz:\s*(.*?)\n(.*?)(?=^## |\Z)", s, re.S | re.M):
        pid, viz, text = m.group(1), m.group(2).strip(), " ".join(m.group(3).split())
        paras.append({"id": pid, "viz": viz, "text": text})
    return title, voice, paras


def chapters(ids):
    out = []
    for f in sorted(glob.glob(os.path.join(SCRIPT, "[0-9][0-9]_*.md"))):
        cid = os.path.basename(f)[:2]
        if not ids or cid in ids:
            out.append((cid, f))
    return out


def key(engine, voice, text):
    return hashlib.sha1(f"{engine}|{voice}|{text}".encode()).hexdigest()[:12]


def write_manifest(cid, f, title, voice, paras, ext):
    d = os.path.join(AUDIO, cid); os.makedirs(d, exist_ok=True)
    items = []
    for p in paras:
        meta = os.path.join(d, p["id"] + ".json")
        info = json.load(open(meta)) if os.path.exists(meta) else {}
        want = key("eleven", ELEVEN_VOICE[1], p["text"]) if voice == "eleven" else key("kokoro", KOKORO_VOICE, p["text"])
        if info.get("hash") != want:          # stale recording of an older text: treat as missing
            info = {}
        has = bool(info) and os.path.exists(os.path.join(d, p["id"] + "." + ext))
        items.append({**p, "file": p["id"] + "." + ext if has else None,
                      "duration": info.get("duration"), "words": info.get("words"), "hash": info.get("hash")})
    json.dump({"chapter": cid, "title": title, "voice": voice, "paragraphs": items},
              open(os.path.join(d, "manifest.json"), "w"), indent=1)


def run_kokoro(ids):
    import numpy as np, soundfile as sf
    from kokoro import KPipeline
    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for cid, f in chapters(ids):
        title, voice, paras = parse(f)
        if voice != "kokoro":
            print(f"skip {cid}: voice is {voice}"); continue
        d = os.path.join(AUDIO, cid); os.makedirs(d, exist_ok=True)
        for p in paras:
            k = key("kokoro", KOKORO_VOICE, p["text"]); meta = os.path.join(d, p["id"] + ".json")
            if os.path.exists(meta) and json.load(open(meta)).get("hash") == k:
                continue
            t0 = time.time(); chunks = []; words = []; offset = 0.0
            for r in pipe(p["text"], voice=KOKORO_VOICE, speed=1.0):
                a = r.audio.numpy(); 
                if r.tokens:
                    for tk in r.tokens:
                        if tk.start_ts is not None and tk.text.strip():
                            words.append({"w": tk.text, "s": round(offset + float(tk.start_ts), 3), "e": round(offset + float(tk.end_ts), 3)})
                chunks.append(a); offset += len(a) / 24000
            audio = np.concatenate(chunks)
            sf.write(os.path.join(d, p["id"] + ".wav"), audio, 24000)
            json.dump({"hash": k, "engine": "kokoro", "voice": KOKORO_VOICE, "text": p["text"],
                       "duration": round(len(audio) / 24000, 3), "words": words}, open(meta, "w"), indent=1)
            print(f"{cid}/{p['id']}: {len(audio)/24000:.1f}s in {time.time()-t0:.1f}s ({len(p['text'])} chars)")
        write_manifest(cid, f, title, voice, paras, "wav")


def run_eleven(ids, dry=False):
    import requests, base64
    keyv = [l.split("=", 1)[1].strip().strip('"') for l in open(os.path.join(HERE, ".env")) if l.startswith("ELEVENLABS_API_KEY")][0]
    total = 0
    for cid, f in chapters(ids):
        title, voice, paras = parse(f)
        if voice != "eleven":
            print(f"skip {cid}: voice is {voice}"); continue
        d = os.path.join(AUDIO, cid); os.makedirs(d, exist_ok=True)
        for p in paras:
            k = key("eleven", ELEVEN_VOICE[1], p["text"]); meta = os.path.join(d, p["id"] + ".json")
            if os.path.exists(meta) and json.load(open(meta)).get("hash") == k:
                continue
            total += len(p["text"])
            if dry:
                print(f"would send {cid}/{p['id']} ({len(p['text'])} chars)"); continue
            r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE[1]}/with-timestamps",
                              headers={"xi-api-key": keyv, "Content-Type": "application/json"},
                              params={"output_format": "mp3_44100_128"},
                              json={"text": p["text"], "model_id": ELEVEN_MODEL,
                                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "speed": 1.0}},
                              timeout=180)
            if r.status_code != 200:
                print("ERROR", cid, p["id"], r.status_code, r.text[:300]); sys.exit(1)
            j = r.json()
            mp3 = base64.b64decode(j["audio_base64"])
            open(os.path.join(d, p["id"] + ".mp3"), "wb").write(mp3)
            al = j.get("alignment") or j.get("normalized_alignment")
            words = chars_to_words(al) if al else []
            import mutagen.mp3
            dur = mutagen.mp3.MP3(os.path.join(d, p["id"] + ".mp3")).info.length
            json.dump({"hash": k, "engine": "eleven", "voice": ELEVEN_VOICE[0], "model": ELEVEN_MODEL, "text": p["text"],
                       "duration": round(dur, 3), "words": words}, open(meta, "w"), indent=1)
            print(f"{cid}/{p['id']}: {dur:.1f}s ({len(p['text'])} chars)")
        write_manifest(cid, f, title, voice, paras, "mp3")
    print("characters sent" if not dry else "characters that would be sent", total)


def chars_to_words(al):
    chars, starts, ends = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    words = []; cur = ""; s = None
    for c, cs, ce in zip(chars, starts, ends):
        if c.isspace():
            if cur: words.append({"w": cur, "s": round(s, 3), "e": round(e, 3)}); cur = ""
            continue
        if not cur: s = cs
        cur += c; e = ce
    if cur: words.append({"w": cur, "s": round(s, 3), "e": round(e, 3)})
    return words


if __name__ == "__main__":
    cmd, ids = sys.argv[1], sys.argv[2:]
    if cmd == "kokoro": run_kokoro(ids)
    elif cmd == "eleven": run_eleven(ids)
    elif cmd == "eleven-dry": run_eleven(ids, dry=True)
    elif cmd == "manifest":
        for cid, f in chapters(ids):
            title, voice, paras = parse(f); write_manifest(cid, f, title, voice, paras, "mp3" if voice == "eleven" else "wav")
            print("manifest", cid, len(paras))
