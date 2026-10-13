# D — How Genesis kept its numbers honest: corrections, verification machinery, traps

Source: `/home/abied/genesis-archive` (read-only). All citations are `docs/<file>:<line>` relative to
that root. Every number below was read in the cited line; nothing is computed or estimated here.
Section 4 is **my synthesis**, not something Genesis wrote.

---

## 1. Corrections and retractions: each claimed number, how it was caught, the true number, the lesson

### 1.1 Denominator artifacts (the biggest class)

| # | What was claimed | How caught | True number | Lesson | Cite |
|---|---|---|---|---|---|
| C1 | Wave B headline: "Gene effect: births +78.9%" | Re-derivation pass that requires a per-adult-season twin for every raw total | Treat ran **1.780x** base's adult-seasons. Size-controlled: **0.5973 / 0.5942 / 0.5887** births per adult-season, i.e. **+0.5%**. One death cause (exposure) **flipped sign**: +49.6% raw became **-15.9%** per adult-season | A raw total from an arm that grows the population measures the population, not the effect. Standing rule (c): a raw total never appears without its rate in the same row | `docs/BENCHMARKS.md:60-64`, `:418-420` |
| C2 | Journal A11: Wave C deaths **540 854 / 511 735**, cause shares 60.2/17.0/13.1/9.0/0.8 | Assembler re-ran on the last season row and checked one cell: `deaths` is a **cumulative** counter (exposure 9 -> 48 -> 87 across s1/s12/s24) | Summing it over 24 rows inflated the denominator ~**10.1x** and re-weighted causes toward early seasons. True: **53 309 / 49 127**, shares **64.9 / 12.8 / 11.8 / 9.7 / 0.9** | Know whether a field is a per-period delta or a running total before you aggregate. The run total of a cumulative counter is `rows[-1]` | `docs/BENCHMARKS.md:567-574`, `:1051` |
| C3 | `holds.py` on `wave-c-base`: `cells=150 holds=71 (47.3%) extinct=75`, plus a phantom world `wNone` | Noticed when a new sidecar type (`.archive.jsonl`) appeared; old frozen corpora had no sidecars so the tool kept "working" there | **94.7%**. The hold count was right; the denominator and extinction count were not. Against a 60% bar, a passing corpus would have been recorded as a red gate | A reader whose file filter predates a new output type **silently rescopes instead of crashing**. Any new file/key/event kind triggers an audit of every tool | `docs/EXECUTE-WAVE-C.md:1445-1455`, `docs/BENCHMARKS.md:110-114` |
| C4 | Salt mass-sensitivity read via `saltcal.py --mass` `gb_rate` (refusals per adult-season): 0.91x / 1.18x / 0.82x | Pilot re-read (journal A3) correlated it with courtship attempts | `gb_rate` correlated with attempts per adult-season at **Pearson r = 0.99991**; it measured how often bodies **courted**, not how often the gate **refused**. View retired with a banner; numbers left unchanged and still reproducing | A rate whose denominator is the wrong unit can be almost perfectly explained by a nuisance variable. Correlate every instrument against its obvious confounder | `docs/BENCHMARKS.md:1204-1212`, `docs/tools/README.md:95-110` |
| C5 | CAL-3 contact bar B1 read **1.2946x** (HARD RED vs >=2.0x) | Numerator/denominator decomposed | Numerator up **1.5887x**, denominator (agent-ticks) up **1.0770x** because the fix improved demography; 5/60 post cells censored at full consumption; uncensored-only ratio **1.5133x**. Verdict kept HARD RED because the bar was frozen; diagnosis recorded "so the next calibration fixes the instrument rather than the number" | Instruments confound exactly when the treatment works. Do not re-score; fix the instrument for the next pre-registration | `docs/BENCHMARKS.md:670`, `docs/EXECUTE-WAVE-D.md:941-945` |
| C6 | Refusal fraction as the scarcity reading | Post-hoc, labelled observation on units | One `kind:'mating'` event is a pair-**tick**, so refused pairs keep courting while passing pairs conceive once; the fraction is bounded near 1 (plateau **0.92-0.95** CAL-4, **0.980-0.985** CAL-3). A per-bout instrument "must arrive with its own pre-registration, on its own corpus" | Know what one row of your log *is*. Event granularity silently defines the denominator | `docs/BENCHMARKS.md:1038`, `:1190-1195` |
| C7 | `resulted_in_gestation` as a conception count | Spotted in one cell: **1,857 flagged vs 2,852 actual births** | Undercounts ~**33-35%** (logging direction vs evaluation order). Count `kind:'mating'` events instead. Later nuance: `resulted_in_gestation == True` *is* the gate's exact eligible set, and blocked is a subset of it, never disjoint | A flag can be the right denominator for one question and a wrong count for another. Document both uses | `docs/EXECUTE-WAVE-C.md:1467-1472`, `docs/EXECUTE-WAVE-D.md:933-935`, `docs/BENCHMARKS.md:433` |

### 1.2 Bugs that manufactured results

| # | Claim/effect | How caught | True number / fix | Lesson | Cite |
|---|---|---|---|---|---|
| C8 | Population counts pre-Wave-A | Repairs that removed "manufactured free energy" | Forager leak = **2.8%** of intake (3456.40 credited vs 3362.77 removed); population fell alive 36 -> 19 -> 17 as subsidies were removed, "and that is CORRECT" | A falling number after a fix is often the honest number. Tell the reader in advance | `docs/WATCH.md:239-243`, `docs/BENCHMARKS.md:273` |
| C9 | Paternity | Data-quality block of `analyze.py` | Father slot recycled during gestation: **40** implausible fathers, **26** sex conflicts, **15/2337 = 0.64%** self-referential births | Identity must be a uid, never an array slot | `docs/BENCHMARKS.md:260-261` |
| C10 | Stale parent link | Investigation before Wave B | **22.2%** of father-link ticks pointed at a living stranger, **61%** of children affected | Same slot-vs-uid class; every consuming site must check | `docs/EXECUTE-WAVE-B.md:193-199` |
| C11 | Pooled lexicon `agreement` (flagship 0.508) | Code-reading verification session | Inflated two ways: `argmax` of an all-zero row is symbol 0 for everyone (an unlearned meaning scores as perfect agreement); self-pairs from sampling with replacement (~**7-11%** of pairs); and founders start at 1.0 so it measures decay of seeded consensus. Masked metric later: late `agree_masked` **0.207** vs pooled inflated **+0.072** | A metric's zero/default state must not be indistinguishable from success. Mask defaults and self-comparisons | `docs/VERIFICATION-SESSION-06.md:102-117`, `docs/BENCHMARKS.md:429` |
| C12 | Wave C `salt_here` per-meaning agreement **0.855** (strongest number) | Read beside default share | Default share **0.947**; same shape as the known artifact `care`. "A measurement of the DEFAULT, not of a learned symbol"; both corpora "CARRIED BY ARTIFACT" | The strongest number can be the weakest evidence; always print the default share beside it | `docs/BENCHMARKS.md:1058` |
| C13 | Population cap | Built a per-tick reconstruction from events | Cap silently destroyed **1316** births in 3 cells; no event, no counter; mating rate rose while births fell. Counter `births_blocked` added | A silent drop is worse than an error. Every truncation needs a counter that is shown firing in a test | `docs/DECISION-salt-findability.md:202-208`, `docs/EXECUTE-WAVE-C.md:702-706` |
| C14 | `wavegate.py`/`lexsize.py` meaning count | Reader audit at C5 | Hardcoded `M = 5`; after C5 (M=6) silently dropped `salt_here`. Now read M from data, exit 3 on mixed widths; regression contract = byte-identical output on old corpora (md5 `0a1a13de...`) | Hardcoded shape constants in analysis tools rot silently. Fix with a byte-identity regression check | `docs/BENCHMARKS.md:160-172`, `docs/tools/README.md:20-27` |
| C15 | `roster.py` on a renamed corpus | Found live | Scored the wrong directory, exit 0, and stamped the wrong `source_hash` into its own provenance | Provenance written by a tool can lie if path resolution is wrong. Verify from a non-repo cwd with absolute paths | `docs/BENCHMARKS.md:102-109`, `:320` |
| C16 | `dbattery.py` reported D5 "not shipped" on a D5+ corpus | Gate scoring | Probe list named census keys as season keys; corrected ("once the tool stopped lying about D5") | Feature-presence probes in tools need tests too | `docs/BENCHMARKS.md:1251` |
| C17 | `canary.py` VERDICT line / exit code | Amendments retired bars | Still applied the retired pair-tick bar and base+1 rule, printing FAIL on D2, D3, D5, D6. Gates were called from printed bars, never the VERDICT | A summary line that encodes a superseded rule is a standing trap. Retire the code with the rule | `docs/BENCHMARKS.md:1237`, `docs/EXECUTE-WAVE-D.md:1052-1054` |

### 1.3 Arithmetic, scoping and wording corrections

- **"Bit-identical" overreach (A23 -> A29).** `wave-c-base` was announced BIT-IDENTICAL to `wave-b-treat`; corrected to **field-identical** (four added keys and `archive` 58 -> 140 differ deliberately). The original journal title is kept because the log is append-only; the correction is a separate entry. `docs/EXECUTE-WAVE-C.md:118-128`, `:726-736`.
- **Factor-of-35 error (A33).** Runbook claimed one agent on a deposit for 700 ticks removes 40 units; capped uptake means at most **1.14** units. Corrected in place. `docs/EXECUTE-WAVE-C.md:932-941`.
- **Amendment 3's binomial arithmetic.** "Fails ~40% on noise" was the complement: **P(X>=3 | Bin(15,0.2)) = 0.6020**; "<=5 is the 95th percentile" was off by one (CDF(5) = **0.9389**); and the 20% premise was one world seed on a pre-Wave-A build, which the benchmark file forbids quoting. Correction note appended, original text left as written. `docs/EXECUTE-WAVE-D.md:1040-1057`, `docs/BENCHMARKS.md:1257`.
- **Walk fraction slice (A10/A37).** "0.53 -> 0.29 -> 0.17" was the mass-400 slice; corpus-wide is **0.394 / 0.178 / 0.125**. `docs/BENCHMARKS.md:686`, `docs/tools/README.md:83-89`.
- **12-season run length justification falsified.** Regime classifier found **32/35/30 of 75** cells still at global peak at s24; runbook text "falsified by measurement, not softened". `docs/EXECUTE-WAVE-C.md:1129-1143`.
- **12-season "free" result was an artifact.** Bound in 15/15 cells at zero hold cost at 12 seasons; at 24 seasons cost two worlds and 35% of median adults. `docs/DECISION-salt-findability.md:137-139`.
- **Lexicon sizing advice** ("~1 hour, no new runs") impossible: raw lexicons never persisted. `docs/VERIFICATION-SESSION-06.md:69-75`.
- **The 17/17 test-count slip** (actual count from execution was different); origin of "count from execution, never from memory". `docs/VERIFICATION-SESSION-06.md:45-49`, `docs/EXECUTE-WAVE-B.md:443-444`.
- **Null arms wrong.** `pref-redraw` redrew per mate-choice call (severing preference itself, not its inheritance) - "not the pre-registered comparison"; moved into `births()`. `shuffle-witness` had "the right mechanic against the wrong target". `docs/EXECUTE-WAVE-C.md:568-614`, `:1403-1404`.
- **Unreproducible sub-clause marked, not inherited.** CAL-3 B3 "strict monotone 10/15": three plausible readings give **15/15, 4/15, 6/15**, none 10/15; row marked "(scoring trail) - NOT reproduced" and not carried into CAL-4. `docs/BENCHMARKS.md:526-529`, `:676`.
- **Truncation, not rounding.** PLAN quoted peaks 40/72/90/110; true **40 / 72.5 / 90.5 / 110.5**. Cosmetic but recorded. `docs/BENCHMARKS.md:323`.
- **Research constants that did not reproduce.** Report 20's R~5 / spacing 22.0 did not reproduce under per-world measurement (19.65 spacing); that refusal blocked a pre-registered ladder step. `docs/BENCHMARKS.md:679-680`.

---

## 2. The verification machinery

### 2.1 "A number without its command is not a benchmark"
Every headline number is one row: value, one-line method, exact re-deriving command, status
(`RE-DERIVED <date>`, `(journal)`, or `(scoring trail) - NOT reproduced`). `docs/BENCHMARKS.md:3-20`.
How to add a row: get the value from a command you ran; write the method (population, rule,
denominator) in one line; paste the literal command and run it once more before writing.
Unreproducible numbers are still written, marked `(journal)`, with the command that *would* work and
the obstacle - "the difference between a number we have not checked and a number nobody can ever
check". `docs/BENCHMARKS.md:1262-1294`. Destroyed artifacts are named (row A-14, full-disk scan
returned **0 matches**). `docs/BENCHMARKS.md:264`. Spot-verification logs list every re-run command
and result. `docs/BENCHMARKS.md:471-574`. Independent channels: a tool-free `jq`/`awk` loop
re-derives the gate's hold count (`docs/BENCHMARKS.md:416`); birth events equal season-row
`births_total` exactly (`:433`); two readers agree on a first-binding series (`:682`).

### 2.2 Provenance pins
- **`source_hash`** = SHA-256 over five sim source files; corpora with different hashes are
  different simulators and are compared side by side, **never pooled** (rule a). `docs/BENCHMARKS.md:43-49`.
  Tag bases are re-derived by hashing each commit's sources, not taken from the journal. `:349-363`.
- **Tool hash pin**: SHA-256 of every analysis script; "if a script's hash has moved, the row was
  re-derived by a different instrument". Two moved tools forced re-runs. `docs/BENCHMARKS.md:131-217`.
- **`.FROZEN` marker** refused as output target by both `run.py` and `sweep.py`; 30 frozen corpora by
  Wave C close. `docs/EXECUTE-WAVE-C.md:545-555`, `docs/BENCHMARKS.md:890`.
- **New label every time**: `is_done()` is file-existence only, so a reused label silently returns the
  old corpus. `docs/BENCHMARKS.md:814-816`, `docs/EXECUTE-WAVE-D.md:925-926`.
- **Never pass default output paths**: `roster.py --out` / `analyze.py --json` defaults overwrite the
  artifacts they check (rule e). `docs/BENCHMARKS.md:76-81`.
- **Scripts that produced gate numbers are copied out of the session scratchpad** into `tools/` with
  hashes; numbers resting on scratch scripts are labelled "(scoring trail)" with an owed reader.
  `docs/EXECUTE-WAVE-C.md:1486-1491`, `docs/BENCHMARKS.md:768-785`, `:1160-1172`.
- **A provenance lie is refused at the flag level**: an accepted-but-inert `--prestige on` would mint a
  corpus claiming an arm the build cannot run, so it errors instead. `docs/EXECUTE-WAVE-D.md:1005-1009`.

### 2.3 Determinism and zero-draw proofs
- **L1: the rng stream is the experiment**; instrumentation must consume zero draws.
  `docs/EXECUTE.md:60-64`.
- Same seed -> byte-identical `.jsonl`, `.events`, `.trace` (`cmp`). `docs/BENCHMARKS.md:253`.
- Control arm is a strict no-op: season rows identical. `docs/BENCHMARKS.md:254`.
- **Field-diff gate**: replay a frozen cell under the new build, delete the named new keys, diff every
  other field (`fielddiff.sh`; `source_hash` must change, bodies must not). `docs/EXECUTE-WAVE-B.md:120-133`,
  `docs/tools/README.md:32`. Corpus-scale version: all 75 cells field-identical. `docs/EXECUTE-WAVE-C.md:726-736`.
- **Inertness by control flow**, not by a value happening to be an identity (`if thresh and ...`).
  `docs/EXECUTE-WAVE-C.md:958-963`.
- **A counter must be shown firing**: "a counter that is zero everywhere is indistinguishable from a
  counter that is broken". `docs/EXECUTE-WAVE-C.md:704-706`.
- **Mechanism-off replays** to exonerate or convict a package: stubbing a mechanism reproduced the
  previous canary byte-identically. `docs/BENCHMARKS.md:1256`.
- **First-divergence tick** between builds via per-tick full-state hash streams. `docs/BENCHMARKS.md:1258`.
- Ablation flag (`--salt-memory off`) proven byte-identical to the prior build in three fixtures, so it
  is "the exact ablation arm, not an approximation". `docs/BENCHMARKS.md:1055`.

### 2.4 Pre-registration, frozen bars, amendments
- Bars written **before** any cell ran, as "FROZEN TEXT" with a timestamp; amendments only pre-run,
  on the mechanism's own arithmetic, quoted in the row. `docs/EXECUTE-C7-SALT-CUE.md:109-145`,
  `docs/EXECUTE-C8-SALT-MEMORY.md:164-211`.
- **Frozen decision rule** with all branches written in advance, including the failure branch:
  "No ladder, no third bar, no walk." `docs/EXECUTE-C8-SALT-MEMORY.md:203-211`.
- "A bar whose measurement fails as defined is amended openly BEFORE scoring, never silently."
  `docs/EXECUTE-C7-SALT-CUE.md:144-145`.
- **Refusing a pre-registered escalation** because its stated premise measured false (decay 0.95 was
  justified as "ratio 0.32, the band's edge", but 0.90 already measured 0.305-0.509): "Executing a step
  whose stated justification has been measured false, to chase a bar, is parameter-walking."
  `docs/BENCHMARKS.md:582-588`, `:680`.
- **Amended gates as scope cuts, not passes**: struck items keep their numbers; "No bar was re-chosen,
  re-worded or re-scored after measurement"; "Nothing was re-scored and no red item was recoloured";
  annotated tags carry the caveat. `docs/BENCHMARKS.md:365-387`, `:837-856`, `:1255`.
- **Findings are not promoted to bars**: report-only legs that read green after the fact stay
  report-only; "Promoting any of these to a bar now, because they read green, is exactly the walk the
  method forbids." `docs/BENCHMARKS.md:1013-1022`, `:1035`.
- **Falsifiers that are predictions stay report-only** so a prediction is not converted into a target.
  `docs/EXECUTE-WAVE-C.md:1175-1185`, `docs/EXECUTE-WAVE-D.md:795-796`.
- **(proposed) vs (sourced)**: every unsourced number is labelled; a number found in no source and not
  marked is a hard stop. `docs/EXECUTE-WAVE-C.md:14-18`, `docs/EXECUTE-WAVE-B.md:11-14`.
- **Stops are the method working**: three waves stopped short of a tag rather than take one unearned.
  `docs/BENCHMARKS.md:830-831`, `docs/DECISION-salt-complements.md:16-22`.

### 2.5 Nulls and controls
- **Null arms live in the runner**, never hand-edited source: "a null implemented by hand-editing the
  source is a null nobody can reproduce". `docs/EXECUTE.md:389-395`.
- **Run the nulls in the same sweep as the treatment**, never as an afterthought. `docs/EXECUTE.md:494-497`.
- **ON / OFF / SHUFFLE arms**, matched seeds, one hash, paired by (world, pop). SHUFFLE came out the
  highest arm, killing the claim. `docs/BENCHMARKS.md:1239`, `docs/EXECUTE-WAVE-D.md:1088-1098`.
- **Severed inheritance (`pref-redraw`)**: never minted in Wave D, so no "inherited" claim allowed; the
  parent-offspring regression substitute (b_op 0.973-0.983) "is explicitly NOT that null".
  `docs/EXECUTE-WAVE-D.md:1104-1108`, `docs/BENCHMARKS.md:1253`.
- **Attribution chain**: control -> base (fix only) -> treat (genes); `treat - base` isolates genes,
  `base - control` isolates the fix. `docs/EXECUTE-WAVE-B.md:94-97`.
- **Measurement shadow**: replay control under a metric-only build so the new metric has a control on
  the identical stream. `docs/EXECUTE-WAVE-B.md:135-151`.
- **Pre-registered null measured before the experiment**: "a comparator recorded after the fact is not
  a comparator"; three of four predicted regimes already occur with no resource, so claims need a rate
  above null, not presence. `docs/EXECUTE-WAVE-C.md:1262-1290`.
- **Difference estimator**: β(mating) - β(survival) on the same covariates, because naive models
  reported 0.24-0.33 where the true pathway was 0.00. `docs/EXECUTE-WAVE-D.md:771-777`, `:955-958`.
- **Validity gate before statistics**: perceived-vs-true correlation must sit in (0.2, 0.98): 1.0 means
  the mediation did not land, ~0 means the channel is dead; "no bootstrap clears it".
  `docs/EXECUTE-WAVE-D.md:395-405`.

### 2.6 Seeds, sweeps, frames, CIs
- **A seed is a world, not a replicate**; single-seed deltas are "uninterpretable by construction".
  `docs/WATCH.md:245-249`. Split world/pop seeds. `docs/EXECUTE.md:417-420`.
- **Confirmation seeds disjoint from screening seeds**, or the gate is scored on the draws that
  selected the worlds. `docs/BENCHMARKS.md:330`.
- **Dual frame (pooled + best-4)**; a claim names its frame; disagreement between frames is itself a
  failure to sustain the claim. `docs/BENCHMARKS.md:119-121`, `docs/EXECUTE-WAVE-D.md:1114-1115`.
- Bootstrap B = 10,000 over surviving seeds; secondary per-seed significance; never a bare
  single-season β; BH q=0.05 for exploratory work. `docs/EXECUTE-WAVE-D.md:774-777`, `docs/EXECUTE.md:492-497`.
- **Two independent detectors** plus a robustness re-run at a rejected setting to answer the
  world-concentration objection (5 episodes were essentially one world). `docs/BENCHMARKS.md:422-423`.
- Exact binomial arithmetic for noise floors, no simulation. `docs/BENCHMARKS.md:1257`.
- Extinct runs are data; log what you dropped; timeouts re-run, never dropped.
  `docs/EXECUTE.md:464-467`, `docs/EXECUTE-C7-SALT-CUE.md:185-186`.

### 2.7 Read-only verification and watch discipline
A no-execution verification session classified every prior claim VERIFIED / ON TRUST / DISCREPANCY,
treating immutable commit messages as independent corroboration. `docs/VERIFICATION-SESSION-06.md:3-18`.
Preflight checks that do not match are a full stop: "Do not 'fix' preflight mismatches."
`docs/EXECUTE-WAVE-B.md:26-41`. Completion checklists are ticked "by running commands, never from
memory". `docs/EXECUTE-WAVE-B.md:463`. The watcher never writes, runs, or re-runs tests in the
watched tree. `docs/WATCH.md:154-173`. Never edit the repo during a sweep (subprocess picks up edits
mid-run). `docs/EXECUTE-WAVE-D.md:948-952`.

---

## 3. Known measurement traps (catalogue)

1. **Raw totals from arms that change population size** - rule (c). `docs/BENCHMARKS.md:60-64`.
2. **Cumulative counters summed over periods** - C2 above. `docs/BENCHMARKS.md:1051`.
3. **Default-state rows scoring as success** (argmax of an all-zero row = shared symbol 0) and
   **self-pairs**. `docs/VERIFICATION-SESSION-06.md:105-113`.
4. **High score at high default share** (`salt_here` 0.855 at default 0.947). `docs/BENCHMARKS.md:1058`.
5. **Glob/filter rescoping when outputs grow** (47.3% vs 94.7%); also shell-escaping that disables
   the filter and inflates denominators. `docs/BENCHMARKS.md:110-118`.
6. **Missing index file reads as zero** (`holds.py` prints `extinct=0` without INDEX; true 12/20).
   `docs/BENCHMARKS.md:95-98`.
7. **"ok" is not "holds"**: sweep log `ok=` (finished) vs held >=20 adults; gap 16/5/2, not constant.
   `docs/BENCHMARKS.md:1184-1188`.
8. **Median of per-cell ratios vs ratio of aggregates** differ (0.3340 vs 0.3444). `docs/BENCHMARKS.md:259`.
9. **Granularity unnamed** (per-world range 1.89-2.40 vs per-cell 1.39-2.62). `docs/BENCHMARKS.md:328`.
10. **Small canaries miss drift**: 15-cell, one-pop canaries could not see a demography fall
    (D4 read 13/15, same as base) that 75-cell mints showed (64.0% -> 54.7% -> 56.0% vs 89.3%).
    `docs/EXECUTE-WAVE-D.md:1119-1125`, `docs/BENCHMARKS.md:1242`.
11. **A canary's first cell is not the canary** (first cell alive=1, finished 13/15).
    `docs/EXECUTE-WAVE-C.md:762-764`.
12. **Slack gates**: a 60% bar passed at 94.7% "is a floor that catches catastrophe", not evidence of
    health. `docs/EXECUTE-WAVE-C.md:1425-1429`.
13. **Gates that bind for the wrong reason**: refusal counter firing on the founder-endowment timer
    (obs - pred = **0.0**) while the field sat 61-97% intact. Two mandatory checks: per-season series
    vs arithmetic prediction, and dose sensitivity. `docs/EXECUTE-WAVE-C.md:1456-1466`, `docs/BENCHMARKS.md:672`.
14. **Identity at zero**: "15/15 identical" when every value is zero is "true and worth nothing".
    `docs/BENCHMARKS.md:684`.
15. **VERDICT lines encoding retired bars** (`canary.py`). `docs/BENCHMARKS.md:1237`.
16. **Exit codes that mean "wrong corpus", not "failure"** (`approach.py` exits 1 by design off its
    frozen corpus). `docs/BENCHMARKS.md:1174-1179`.
17. **Cross-build language columns** (M=5 vs M=6) and decoded-vs-raw gene values after a range
    change. `docs/BENCHMARKS.md:51-58`, `:970-974`.
18. **Truncated trajectories** read as shapes; report the truncation rate beside every count.
    `docs/EXECUTE-WAVE-C.md:1140-1143`.
19. **Cross-corpus inferences** (measuring on one corpus, transferring to another) labelled every time.
    `docs/BENCHMARKS.md:434`.
20. **Inequality without population** (a Gini over 7 survivors). `docs/BENCHMARKS.md:1057`.
21. **Classifier thresholds one notch from flipping** ("no cycling under a two-oscillations rule",
    never "no oscillation exists"). `docs/BENCHMARKS.md:1141-1144`.
22. **Line-number references drift**; grep the quoted content and journal the drift.
    `docs/EXECUTE-WAVE-C.md:20-25`.

---

## 4. Proposed honesty protocol for the EBM lab (MY SYNTHESIS)

Derived from sections 1-3. The EBM lab has the same risk shape as Genesis: many small models, growth
over generations, stochastic training. "Sleep" retraining and action caching add new ways to fake a
result.

**A. Every number is a row.**
1. Keep `BENCHMARKS.md` from day one: value | one-line method (population, rule, denominator) |
   literal command | status (`RE-DERIVED date` / `(journal)` / `NOT reproduced`).
2. Re-run the command once more before writing the row. Never copy a number from a log, commit
   message, chat, or summary.
3. A caveat lives in the row or it does not travel.

**B. Provenance.**
4. Stamp every run's first line with: code hash (over the model/training sources), config, all seeds,
   the arm, and the instrument version.
5. Never pool runs across code hashes; compare named pairs only.
6. Hash-pin analysis scripts; a moved hash means re-run before quoting. Keep analysis tools in the
   repo (Genesis's unresolved recommendation).
7. Freeze evidence directories (`.FROZEN`, refused by every writer). New label for every run.
   No tool default may write over a stored artifact.
8. Move any script that produced a quoted number out of scratch before the session ends.

**C. Determinism and zero-interference.**
9. Same seed -> byte-identical outputs, tested. Separate rng streams for world, init, training noise,
   sleep replay sampling, and growth decisions so one change does not re-roll everything.
10. Instrumentation draws zero random numbers; prove it with a field-diff against a frozen run.
11. Every flag that turns a mechanism off is proven byte-identical to the build without it. That is the
    ablation arm.
12. Every counter (cache hits, connections pruned, retrain rejections, OOM drops, capped growth) has a
    test that shows it firing. Silent truncation is a bug.

**D. Pre-registration.**
13. Before any run: write the bars, the estimator, the denominator, the null, and a decision rule with
    every branch, including the failure branch. Timestamp it. No ladders added after.
14. Mark every unsourced threshold `(proposed)`.
15. Amend only before scoring, in the open. After scoring, a failed claim is retired as a finding with
    its number. It is never recoloured.
16. Report-only predictions stay report-only even when they come out green.

**E. Controls built into the runner.**
17. For each claimed mechanism, mint ON / OFF / SHUFFLE (and a severed-inheritance arm for anything
    "inherited across generations") on matched seeds in the same sweep. For EBM: sleep ON/OFF, cache
    ON/OFF, connections rewired at random, offspring weights from a shuffled parent.
18. Measure the null before the treatment exists. Claims need a rate above null, not mere presence.
19. Prefer difference estimators that cancel generic "good model" effects (gain from cache minus
    gain from an equal-size random cache).
20. Gate on validity first: e.g. energy actually discriminates (correlation with ground truth neither
    ~0 nor ~1) before any downstream statistic is read.

**F. Denominators and units (ask on every metric).**
21. What is one row? (step, episode, model-generation, connection-event.)
22. What does the denominator do when the treatment works? Growth, survival and caching all change
    the denominator. Report every raw total beside its per-unit rate.
23. Is the field cumulative or per-period?
24. Can a default/untrained state score as success (argmax over zeros, an untrained EBM's flat energy,
    an empty cache returning a default action)? Mask it and print the default share.
25. Name the granularity (per model / per lineage / per run) and the aggregation (median of ratios vs
    ratio of medians).
26. Correlate each instrument with its obvious confounder (activity rate, population size, model
    count). If r is near 1, it measures the confounder.

**G. Sample size and noise.**
27. A seed is one world. Use disjoint seeds for selecting configs and for confirming them.
28. Report two frames when a subset is privileged, and treat disagreement between them as failure.
29. Small canaries catch catastrophe only. Run full-size checks per package to catch drift.
30. Wait for the full canary. Report truncation (runs still improving at the end).
31. Use exact arithmetic for noise floors; bootstrap CIs over seeds.

**H. Tools and review.**
32. Every new output file, key, or event type triggers an audit of every reader, with a byte-identity
    check on old data.
33. No tool summary line (VERDICT/exit code) may encode a bar that has been retired.
34. Read-only verification passes classify every inherited claim VERIFIED / ON TRUST / DISCREPANCY.
    Preflight mismatches stop the session and are never "fixed".
35. Corrections are appended. The original text stays, and the correction names the true number and
    how it was caught.
36. When a fix lowers a number, say so before anyone reads it as a regression.
