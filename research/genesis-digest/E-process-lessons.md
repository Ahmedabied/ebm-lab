# E — Genesis process lessons: the human and working-method story

Source: `/home/abied/genesis-archive` (read-only). All paths below are relative to
`/home/abied/genesis-archive/docs/`. Citations are `path:line`. Anything marked **[interpretation]**
or **[synthesis]** is mine, not the archive's.

---

## 0. The one-paragraph version

Genesis began on 2026-08-11 as a two-hour, eight-test numpy sketch with a clear and exciting idea
(`sessions/2026-08-11_session-03.md:10-34`). Ten sessions later, on 2026-08-16, it had 50 commits,
483 tests that took ~14 minutes to run, 42 frozen corpora, 24 research reports, and five waves tagged,
three of them (B, C, D) only on **amended** gates (`START-HERE.md:39-43`, `:75-85`). The energy-based
"left brain", the thing the new EBM lab is about, was milestone **M2** from day one
(`GENESIS.md:9-10`, `GENESIS.md:97-100`) and was never reached. Sessions 09-12 ran back to back in
about 29 hours (2026-08-14 ~22:30 to 2026-08-16 03:35; `sessions/2026-08-14_session-09.md:13`,
`sessions/2026-08-15_session-12.md` A16 close). The project ended on Ahmed's pacing rule: *"we finish
this wave today and we wait for next week reset for the next wave, the project is becoming token
intensive."* (`SESSION-12-ORDERS.md:87-89`).

---

## 1. Timeline: one paragraph per session

**Session 03 (2026-08-11): the idea.** Ahmed pivoted away from the LLM "house": the subconscious-as-LLM
is *"lost in a prompt and is asked to guess reality"* (`sessions/2026-08-11_session-03.md:3-4`). The
plan was a physics-first world, evolved creatures, language grown from survival pressure, and no LLMs
in the loop. The addendum was "energy models for the analytical brain" (`:7-8`). v0 was built in ~2 hours
(`:10`). The first run died out in one season because metabolic heat was ~15x too weak. *"The bug was
in thermodynamics, not in prose"* (`:20-23`). Shipped: 6 files, 8/8 tests, a 2-founder run that
roughly followed the Fibonacci curve (`:26-34`). **[interpretation]** This is the session that sounds
most like fun: small, fast, surprising, and easy to read.

**Session 04 (2026-08-11): research.** Ahmed's brief was *"make the research worth it, sonnet 5 agents
for online searching with your directions"* (`sessions/2026-08-11_session-04.md:8-9`). Eleven parallel
Sonnet research agents wrote ~33k words (`:11-17`). Out of that came the M1 rulings (salt as the finite
resource, pain as a reflex layer, gloom as a bistable sub-drive), seven real v0 bugs, and a protocol
change from 6-season runs to 11-24 seasons (`:22-61`). Wave order A-E stayed open for his call (`:63-67`).

**Session 05 (2026-08-11): body research and the plan.** Eight more Sonnet agents wrote ~2,000 lines
(`sessions/2026-08-11_session-05.md:8-12`). The agents checked each other's work: five reports had
claimed the same genome index (`:15-20`). The big measured finding was that a seed is a *world*, not a
replicate (8/10 vs 0/10 survival depending on the world; `:172-194`), which added a blocking
calibration wave A.5. Output: `RESEARCH-BODY.md`, `PLAN.md` (Waves A to I) and `EXECUTE.md`, a
cold-startable runbook (`:229-244`). Five items went into PLAN §9 for Ahmed, including whether Wave G,
*"a loaded gun"*, should run at all (`:220-227`).

**Session 06 (2026-08-11, unattended night): Wave A build.** Opus executor, Sonnet implementers
(`sessions/2026-08-11_session-06.md:3-6`). Scope grew twice because of measured bugs: a forager energy
leak (2.8% of intake) and a paternity slot bug (`:22-26`, `:50`, `:72`). The A.5 gate first failed at
30% (`:79`). The cause was the screening criterion (a short screen picks worlds that boom and then
crash), so the screen was lengthened and the gate then passed at 87% (`:124-135`). Shipped: tags
`wave-A`, `wave-A5`, 72/0 tests (`:95-115`). A watching session raised the possibility that
`lexicon_agreement` was inflated by default rows (`:137-173`). That kind of artifact came back again and again.

**Session 07 (2026-08-12, 02:41 onward): Wave B (drives).** Nine commits, 72 → 213 tests, ~466 cells
against a ~410 budget (`sessions/2026-08-12_session-07.md:286-300`). It hit a **hard stop**: the
`G_GLOOM_SICK` guardrail number the runbook depended on did not exist in the research corpus (`:47`,
`:122-140`). Wave B was **deliberately left untagged** (`:474-505`). The journal also corrected its own
timestamps, which had been estimated rather than read from the clock (`:58`).

**Session 08 (2026-08-12): Wave C (salt).** Ahmed overrode the B3 block: *"wave A and Wave B Are dont
[done] Time to go full on the next"* and then *"start implementing … do not stop untill all metrics
satisfy our goal with wave C fully autonumous"* (`sessions/2026-08-12_session-08.md:204`). The journal
was careful to record this as a ruling **inferred from direction**, not a verbatim ruling (`:206`).
C1-C6 shipped. Two calibration blocks (405 + 360 cells) found that the salt gate behaves like *"a
timer, not a resource mechanism"*. Salt was never used up (0/405 exhausted) (`:104-111`, `:280-293`).
There was also a fixture audit that found three tests that could never fail (`:331`, A44),
and a disclosed git-history rewrite that led to the rule "post-commit fix is a new commit" (`:202`).

**Session 09 (2026-08-14 ~22:30, unattended): tag A-C, benchmark.** New shape: **Fable orchestrates,
Opus 5 labours**, with a mandatory research seat (`SESSION-09-ORDERS.md:23-46`). Wave B was tagged on
an amended gate (scope cut). C7 shipped, CAL-3 scored 4 green / 2 red, and **Wave C was left untagged
again** (`sessions/2026-08-14_session-09.md:29-41`, `:709-722`). `BENCHMARKS.md` was built, 775 lines
(`:723-725`). Nine Opus agents (`:739-740`). A test run was found to have destroyed a Wave A artifact
(`:220-235`).

**Session 10 (2026-08-15 08:15-14:40): Wave C tagged, Wave D designed.** Ahmed: *"tag wave c and start
wave D."* (`SESSION-10-ORDERS.md:69`). C8 (place memory) and C9 shipped. The pre-registered headline
read 1.043x against a ≥1.5x bar, so `wave-C` was tagged on the amended gate, "road 2"
(`sessions/2026-08-15_session-10.md:567-575`). At 12:35 Ahmed typed live: *"continue but once
everything is tagged and final dont start on wave D right away each wave needs a fresh session a full
wave can never start with ctx above 10%"* (`:414-417`). Wave D was designed (WAVE-D.md 785+ lines,
EXECUTE-WAVE-D.md 993+ lines) but not started (`:577-582`). Twelve Opus agents, +690 cells (`:592-597`).

**Viewer session 01 (2026-08-15 18:58-20:20, parallel side quest).** Ahmed's ask: *"can we ground the
map a little bit more ... let me choose the view of the wave instead of random values so i can see the
evolution of waves and make the map more accurate so i can be kept in the loop in my own project"*
(`VIEWER-SESSION-01-ORDERS.md:7-11`). The old map **invented** dots when there was no trace
(`:44-59`). Shipped: a wave picker over one real, fully traced run per tag, a SHOWCASE/ILLUSTRATION
badge, an auto re-run when master moves, and a remote page of ~72 KB (`viewer/SESSIONS/2026-08-15_viewer-01.md:8-28`).
The viewer is a read-only stdlib server behind a Cloudflare Worker (`viewer/README.md:1-30`).

**Session 11 (2026-08-15 15:52-22:48): Wave D, D0-D5.** Six gates went green. Two bars failed as
written and were re-argued as Amendments 2 and 3 (`sessions/2026-08-15_session-11.md:447`, `:764`,
`:980-991`). The Opus writers took 63, 65, 93 and 104 minutes per package (`:402`, `:512`, `:613`,
`:694`). There was a /tmp quota outage (`:675-690`). At 22:28 Ahmed, relayed by Vesper: *"the work will
start getting sloppy, stop after the test document and open a new session to finish the wave the right
way."* (`:838-851`). The session ended "STOPPED AT BOUNDARY". Thirteen Opus agents (`:1005-1011`).

**Session 12 (2026-08-15 22:53 to 08-16 03:35): finish Wave D.** A fresh-eyes review found D6's
"pileup" story was wrong (ghost fights against absent holders), so D6.1 was redone
(`sessions/2026-08-15_session-12.md:137`, `:201`, `:245`). D7 (`give`) was struck for scheduling
reasons (`:459`, `:616`). The wave gate came back with **items 1 and 2 RED**: the prestige mechanism
did not move fitness, and holds fell 89% → 56% (`START-HERE.md:78-85`). `wave-D` was tagged on
Amendment 2 with those items "struck as findings" (`:77-79`). Ahmed then typed *"document will close this session"*
(`sessions/2026-08-15_session-12.md:647`). Fable's context at close was ≈40% (`:643`).

---

## 2. Ahmed's rulings and preferences about how to work

**Model split: "Fable rules, Opus labours."** Short form in `START-HERE.md:67-68`. Long form:
*"You are the brain and the orchestrator. You are not the labourer … You stay on Fable, at max effort …
The work is done by Opus 5 subagents … Push token-heavy reading down to the agents. Fable's weekly cap
is the scarce resource in this house (it hit 99% today)."* (`SESSION-09-ORDERS.md:23-35`). Before this,
sessions 04-06 used Sonnet agents (`sessions/2026-08-11_session-04.md:8-9`; `SESSION-06-ORDERS.md:127`).

**A subagent's report is evidence, not truth.** Figures are re-derived by command
(`SESSION-09-ORDERS.md:48-50`).

**One wave per fresh session.** *"each wave needs a fresh session a full wave can never start with ctx
above 10%"* (`sessions/2026-08-15_session-10.md:416-417`); *"One wave per session. That is Ahmed's
standing rule."* (`SESSION-11-ORDERS.md:31`).

**Stop at a boundary, not at exhaustion.** *"the work will start getting sloppy…"*
(`sessions/2026-08-15_session-11.md:840-841`). This was turned into a standing rule: past ~50% context, stop at
the next package boundary, and *"That is not failure; it is the design."* (`SESSION-12-ORDERS.md:93-99`;
KG form at `sessions/2026-08-15_session-12-KG-DEFERRED.md:20`).

**Token pacing.** *"we finish this wave today and we wait for next week reset for the next wave, the
project is becoming token intensive."* (`SESSION-12-ORDERS.md:87-89`; `START-HERE.md:71-72`). Budget
pressure shows up in almost every set of orders: *"4% of the weekly budget remains"*
(`SESSION-06-ORDERS.md:125`), the 99% cap (`SESSION-09-ORDERS.md:33-34`), the viewer sharing the budget
with session 11 (`VIEWER-SESSION-01-ORDERS.md:33`), and *"~64% with 6 days to reset. You are a finish,
not a start — be lean."* (`SESSION-12-ORDERS.md:153-154`).

**Unattended and decide-don't-ask.** *"Nobody is going to answer a question … do not stop to ask.
Decide, write the argument down, proceed."* (`SESSION-09-ORDERS.md:10-14`). Ahmed watched "occasionally,
by screenshot" (`:10`). Live typed instructions override the orders (`SESSION-12-ORDERS.md:151-152`).

**Which decisions are his.** Delegated rulings must be marked `RULED (delegated)` *"never as if Ahmed
ruled it. He will read them later and he wants to see the argument, not the conclusion."*
(`SESSION-09-ORDERS.md:104-106`). Never delegated: Wave G's yes, tagging on an artifact, touching the
house, any LLM below L6 (`:108-125`). His standing list: `COURT_MARGIN`, `SALT_CONFIRM_DELTA`,
`G_GLOOM_DEFEAT`, Wave G, whether a red item 2 carries the tag, the recalibration knobs
(`START-HERE.md:113-117`; `PLAN.md:719-761`).

**One writer per tree.** *"One writer per tree at a time. Parallel is for read-only work, or give a
writer its own `git worktree`"* (`SESSION-11-ORDERS.md:19-20`; also `SESSION-10-ORDERS.md` §0).

**A research seat every session.** Ahmed asked for it by name. *"This is not optional and it is not
filler"* (`SESSION-09-ORDERS.md:37-43`). Later called *"the highest-leverage seat on the team"*
(`SESSION-10-ORDERS.md:18-20`).

**Honesty over tags.** *"If a wave cannot honestly earn its tag, it stays untagged and you say why —
that outcome is a success of the method"* (`SESSION-09-ORDERS.md:112-115`). But also: *"He has read the
refusal and he is not asking you to fake it — he is telling you the wave is finished being open."*
(`SESSION-10-ORDERS.md:69-71`).

**He wants to see it.** The viewer ask, *"so i can be kept in the loop in my own project"*
(`VIEWER-SESSION-01-ORDERS.md:9-11`), and *"he wants to watch it evolve without having to read
`git log`"* (`:171-176`).

**Tone.** Relayed in his words: *"believe in yourselves, and enjoy this — it is genuinely a beautiful
project."* (`SESSION-09-ORDERS.md:187-188`; repeated in SESSION-10:153, SESSION-11:133, SESSION-12:166,
VIEWER:175). Wave D was the wave *"Ahmed is more excited about … than anything else in the project"*
(`SESSION-10-ORDERS.md:77-79`).

Provenance note: the orders for sessions 09-11 say "Written … by Ahmed, relayed from the laptop"
(`SESSION-09-ORDERS.md:3`). Sessions 12 and the viewer were written by Vesper, his laptop Claude, "on
Ahmed's instruction" (`SESSION-12-ORDERS.md:3`). So the orders' prose is not all his verbatim words.
Only the italic quotes above are.

---

## 3. What drove scope and token blow-up; productive vs grinding

### Evidence

- **The method grew heavier on every pass.** Journal sizes went from 48 → 77 → 119 → 195 → 556 → 339
  → 742 → 599 → 1053 → 647 lines (+723 for the session-12 gate report). Design docs reached
  WAVE-D 1002 and PLAN 761 lines. Each wave had pre-registered gates, canaries, a three-arm A/B,
  amendments, BENCHMARKS rows with re-derivation commands, KG promotion and a START-HERE rewrite (see
  the close-out list at `sessions/2026-08-15_session-12.md` A16, lines 564-646).
- **Small changes made the whole world run differently.** Any change to the genome width, the cap or
  the RNG draws "re-rolls every universe", so every corpus had to be re-minted and every gate re-scored
  (`sessions/2026-08-12_session-08.md:194`, `:212`; `sessions/2026-08-12_session-07.md:501-503`).
- **The test suite and the sweeps got slow.** Tests grew from 8 to 483 and from 31.7 s to ~14 min
  (`START-HERE.md:39-40`). A 75-cell three-arm mint took ~25 min per arm (`START-HERE.md:100-101`). A
  regime map took 109 min against 66 budgeted (`sessions/2026-08-15_session-10.md:554`).
- **Wave C ground on through three sessions.** C1-C9 and CAL-1..4 ran across sessions 08-10. Every
  parameter was swept and *"none of them changes finding"* (`sessions/2026-08-12_session-08.md:293`).
  The tag finally came on an amendment (`sessions/2026-08-15_session-10.md:567-575`).
- **Bars were re-argued after they failed.** This happened in D2, D5 and the wave gate
  (`sessions/2026-08-15_session-11.md:447`, `:764`; `START-HERE.md:77-79`). Session 12 then found two
  of Amendment 3's own numbers wrong (`sessions/2026-08-15_session-12.md:94`).
- **The headline result came back negative.** The prestige mechanism moved the cue but not fitness,
  and the D-build cost a third of the births (`START-HERE.md:80-85`; `PLAN.md` §9 item 6).
- **Ahmed stopped being able to see his own project.** The map was inventing dots, and he asked to be
  *"kept in the loop in my own project"* (`VIEWER-SESSION-01-ORDERS.md:9-11`, `:44-59`).
- **The original goal was crowded out.** The LLM-free subconscious with an EBM left brain (M2) and
  Panksepp right brain (M3) (`GENESIS.md:92-104`) stayed behind Waves A to I, and only A-D were done.

### What made sessions productive

- **Small and fast.** Session 03 took ~2 h, was explained by one function read, and gave a vivid story
  (`sessions/2026-08-11_session-03.md:18-24`).
- **Research seats that changed decisions.** Reports 20-24 changed rulings before code was written
  (`SESSION-11-ORDERS.md:16-18`; `sessions/2026-08-15_session-11.md:205`).
- **Measured surprises.** Session 05's world-vs-founder finding and session 06's diagnosis of the
  failed gate (`sessions/2026-08-11_session-06.md:124-135`).
- **A fresh-eyes review.** Session 12's review of D6 caught a wrong story
  (`sessions/2026-08-15_session-12.md:137`).
- **Clean boundaries.** Stopping at a boundary kept session 12 at ≈40% context (`:643`).

### What made sessions grind

- Calibrating a mechanism that could not measure what it was built for (salt).
- Gates and canaries too small to see the real effect: *"a 15-cell one-pop canary cannot see a
  wave-level demographic drift"* (`START-HERE.md:120-122`).
- Bookkeeping layers on every session: KG, BENCHMARKS, START-HERE, PLAN, amendments.
- Waiting on detached jobs and fighting the tooling (§4).

### Where the fun went **[interpretation, labelled] — RETRACTED by Ahmed 2026-10-13**

> Ahmed: "genises was never menat to be fun my job sucks my soul out im soo proud of gnises its my favourite
> ever project, but i need a real goal and a real plan with it, it is not a small project i belive its a
> research lab grade". The burnout came from his job. The interpretation below is wrong; it is kept as a record.


The archive never records Ahmed saying he lost passion. That comes from him now, not from the files.
What the files do show is a move from **a creature you could watch** (session 03: extinction, the
thermodynamics bug, a Fibonacci population) to **an audit trail you had to read**: 1,000-line journals
of gate numbers, amendments and re-derivations, written for a reader who "watch[es] occasionally, by
screenshot" (`SESSION-09-ORDERS.md:10`).

The project ran unattended at night, and decisions were "RULED (delegated)" for him to read later. That
made sense for throughput, but it put him **outside** the loop. The viewer request is the clearest
sign he felt that. The encouragement repeated in five sets of orders ("enjoy it… beautiful project")
was written for the agents, while Ahmed's own live inputs were mostly about stopping: "don't start D",
"stop, it'll get sloppy", "wait for the reset", "close this session".

Rigor itself (pre-registration, no tagging on artifacts) was not the problem. It is what kept the
negative results honest. **What hurt** was rigor at the scale of *re-minting whole universes*,
combined with Ahmed *not being the one doing the learning*.

---

## 4. Operational traps (cited)

- **`rm` with a shell-variable path freezes an unattended run.** The harness delete guard raises a
  permission prompt. This happened twice and cost ~80 minutes of idle box (`SESSION-11-ORDERS.md:74-84`).
  Safe forms: literal paths, `find /literal -delete`, `mktemp -d`. The rule must be in every agent's
  prompt (`sessions/2026-08-15_session-11-briefs/D5-brief.md:3-4`).
- **/tmp is a quota'd tmpfs shared across sessions.** EDQUOT made every Bash call return exit 1 with no
  output, because tool output is captured under /tmp (`sessions/2026-08-15_session-11.md:675-690`).
  Keep scratch on /home (`SESSION-12-ORDERS.md:128-129`).
- **The MemPalace writer lock.** `mempalace_kg_add` returned "Peer MCP writer active" all night, so KG
  promotion was deferred to a file (`sessions/2026-08-15_session-12.md:606-611`;
  `sessions/2026-08-15_session-12-KG-DEFERRED.md:1-3`).
- **Pattern-based `pkill -f` killed another agent's test run.** Rule: kill by PID only. Two agents on
  one repo (a worktree sharing `.git`) stretched a sweep from ~15 to 27m24s
  (`sessions/2026-08-12_session-08.md:224`).
- **A wait loop whose command line matches its own `pgrep -f` pattern never exits**
  (`START-HERE.md:122-123`).
- **Never edit the repo while a sweep runs.** `sweep.py` spawns `run.py` per cell, so later cells pick
  up the edits (`sessions/2026-08-12_session-07.md:55`, `:451-452`).
- **The foreground timeout is 600 s.** Long suites must run detached and be polled
  (`START-HERE.md:39-40`). A ~50 min background-job ceiling killed a sweep mid-way. Make sweeps
  resumable (`sessions/2026-08-11_session-06.md:88`).
- **Tools that read the wrong files still return a number.** `roster.py` resolved a renamed corpus to
  the wrong directory with exit 0 (`sessions/2026-08-14_session-09.md:208-218`). `holds.py` scored a
  passing corpus at 47.3% (`sessions/2026-08-12_session-08.md:96`, A26). `canary.py`'s VERDICT line applied
  retired bars (`START-HERE.md:120`).
- **Tools that write over their own inputs.** `tests.py` wrote into `runs/` and destroyed a Wave A
  artifact. `roster.py --out` and `analyze.py --json` default to overwriting what they check
  (`sessions/2026-08-14_session-09.md:220-243`).
- **Tests that can never fail.** Three were found by mutation. Two were invisible to the whole
  370-assertion suite (`sessions/2026-08-12_session-08.md:331-339`, A44).
- **Metric artifacts from default values.** `argmax` of an all-zero lexicon row reads as perfect
  agreement (`sessions/2026-08-11_session-06.md:137-160`). Rule: *"Ask what a denominator does when the
  treatment works. Size-control every rate."* (`SESSION-12-ORDERS.md:122-123`).
- **Re-minting into an existing label dir.** `sweep.py` resumes by cell name and skips (`START-HERE.md:123-124`).
- **Journal timestamps written from estimates** ran up to 17 min fast (`sessions/2026-08-12_session-07.md:58`).
- **History rewrite** led to the rule "a post-commit fix is a new commit" (`sessions/2026-08-12_session-08.md:202`).
- **Shared box.** The live house, other Claude sessions and the viewer all compete for CPU. Rules: nice,
  12 workers, `--no-optional-locks` for read-only git (`VIEWER-SESSION-01-ORDERS.md:20-34`).

---

## 5. Recommendations for the EBM lab **[synthesis, mine]**

1. **Ahmed in the loop, live, by default.** Genesis optimised for unattended nights, and Ahmed ended up
   reading results later. For a learning project, the default should be live, short sessions where he
   predicts what will happen before each run and then sees it. Unattended runs only for long training
   jobs with a known shape.
2. **Something visible from day one.** Every experiment should produce a plot, an energy landscape or a
   small animation, not just a number in a journal. The viewer came too late. A notebook or one-page
   HTML that redraws after each run is enough.
3. **Learning goals, not gates.** Each session should have one question that teaches an EBM idea
   (contrastive divergence, Langevin sampling, score matching, a sleep/replay phase) and one picture
   that answers it. Keep pre-registration light: write the prediction in one line before the run.
4. **Keep it small enough to re-run in seconds.** A test suite under ~30 s, models trainable on CPU in
   under a minute, and no runs that "re-roll every universe". Design the lab so adding a new model node
   does not invalidate past results (fixed seeds per component, versioned checkpoints).
5. **Hard budget per session, written at the top.** Something like "this session: ≤ N agent dispatches,
   ≤ X% of weekly budget". Stop at a boundary when it's reached. Ahmed already invented the boundary
   rule. Use it from session 1, not session 11.
6. **Fewer bookkeeping layers.** One `STATE.md` plus one short journal per session (one screen at the
   top: what we tried, what we learned, what surprised us). Skip KG promotion, BENCHMARKS tables and
   amendment chains unless a result is actually going to be cited.
7. **Use agents for reading, not for doing the learning.** Fable-rules/Opus-labours saved Fable tokens,
   but it also meant the understanding lived in subagent reports. For the EBM lab, the core math and the
   first implementation of each idea should be done together in the main conversation. Delegate
   literature searches and boilerplate.
8. **Keep the research seat, scoped.** One targeted question per session, answered in ≤ 1 page.
   Genesis's reports grew to 51-83 DOIs (`sessions/2026-08-15_session-12.md:137`; `sessions/2026-08-15_session-11.md:205`).
9. **Keep the honesty rules, scaled down.** Re-derive numbers by command, size-control rates, check
   whether a metric can be fooled by default values, and never claim more than was measured. These were
   Genesis's best habits. They are cheap at small scale.
10. **Carry the operational guards over from the start:** no `rm` with variables, scratch on /home, one
    writer per tree, kill by PID, nothing written into the inputs, detach and poll anything over 10
    minutes, resumable jobs.
11. **Make "fun" checkable.** At each session close, ask Ahmed one question: "did you learn something
    and enjoy it?" Two "no"s in a row trigger a re-scope, the way a red gate did in Genesis.
12. **Honour the origin.** The EBM lab is Genesis's M2 (`GENESIS.md:97-100`). Its first milestone could
    be the exact test M2 set: an EBM that beats a simple argmax baseline *"AT SURVIVING, not at looking
    clever"*. That is small, concrete, and it closes an old loop.
