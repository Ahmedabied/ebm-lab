# HANDOFF — read this first next session

## Where it stands (one paragraph)
EXP-02 gave the lab its first positive within-life learning result: the EBM trained as a value
function (`ebm-td`) forages by smell and reaches tabular Q's level (`findings/02`). The decomposition
says no single borrowed ingredient does it; the value-learning paradigm does. Policy gradient at the
old step size collapses on night 0 (`research/07`). Two referee-found bugs were fixed before the run
(A14 critic scale, A16 Q centring; plus the unclipped behaviour ratio); one baseline defect was found
and kept as the pre-registered target with a textbook variant added (A17).

## Goal pivot first
Read `decisions/0002_goal_pivot.md`. The first deliverable next session is the written list of
brain-cell properties the EBM must mimic, each with a source and a falsifiable test; EXP-03 is chosen
from that list, not from the lever list below.

## Decisions that are Ahmed's (nothing below is started)
1. **Which next experiment (EXP-03), one only.** `findings/02` §"What it points to" lists five;
   the orchestrator's recommendation, if asked: **(4) sleep on a learner that actually learns** (the
   EXP-01 matched sleep arms on `ebm-td`: replay vs today vs noise vs none) because it is the first
   meaningful test of H1 and needs no new machinery; second choice (3) make the xor world bite and test
   whether hidden units earn their keep (the first real test of "small EBMs that make connections").
2. **World design:** raise toxicity or make poison drain energy directly, so the conjunction is required
   (`research/07` §1.3). Not changed inside EXP-02.
3. **Step-size policy:** adopt a per-sample normalised step (α/|∂Q/∂θ|²) so arms with different input
   widths are comparable (`findings/02` Limits 1), or keep fixed α and pilot per arm.
4. **Policy gradient:** re-ask it at a sane step with an entropy bonus (lr/T² one knob) or retire it in
   favour of the value learner for v0.
5. **RNG streams:** split world / body-noise / agent streams from EXP-03 on (true pairing), accepting
   that EXP-01/02 numbers are then not bit-reproducible under the new scheme.
6. The open questions from R1–R4 (`research/03`–`06` foots) still stand: seasons, growth within life
   or across generations, unit cost physics or gene, dreams now or later.

## Protocol reminders
- Pre-register (file + commit) before any run; pilots only on declared pilot seeds; the burned list is
  in `STATE.md` and enforced by the harness. Fresh main seeds next: 400–419.
- Every interesting conclusion gets two hostile referees before it is written as a finding.
- Corrections are appended, never erased (see `findings/01`, `research/07`).
- No screen popups; write to disk and give paths. No cloud spend without asking.

## Housekeeping
- Raw run logs live under `/tmp/ebm-runs/` (not committed; regenerate with the commands in each
  finding). Referee scratch scripts are under the session scratchpad and are not part of the record.
- The ES search (`research/07` M1b) finished after the close: held-out 5250 on 20/20 in xor; recorded.
