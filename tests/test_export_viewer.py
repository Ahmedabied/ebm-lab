"""Export provenance: run.json carries the run's own input names, effective brain config and
per-night instruments; the CLI's defaults equal the dataclass defaults."""
import json
import numpy as np
import pytest

from creature.sim import Life, SimConfig
from creature.senses import Senses, SenseConfig
from creature import export as ex
from creature import run as runcli


def _life(tmp_path, label, sign=False, act_mode="softmax", learner="pg", days=3, day_len=60, seed=20):
    cfg = SimConfig(seed=seed, label=label, policy="ebm", days=days, day_len=day_len, day_learning=True,
                    learner=learner, runs_dir=str(tmp_path))
    cfg.sense.sign_features = sign
    cfg.brain.act_mode = act_mode
    Life(cfg).run()
    d = tmp_path / label / str(seed)
    ex.export(str(d))
    return json.loads((d / "run.json").read_text()), json.loads((d / "meta.json").read_text())


def test_export_sign_egreedy_q_life_has_15_inputs(tmp_path):
    run, meta = _life(tmp_path, "q15", sign=True, act_mode="egreedy", learner="q")
    names = run["input_names"]
    assert len(names) == 15 and names == meta["config"]["input_names"]
    assert names == Senses(SenseConfig(sign_features=True)).names()
    assert run["input_names_source"] == "meta"
    m = run["meta"]
    assert m["brain_dim"] == 15 and m["act_mode"] == "egreedy" and m["learner"] == "q"
    assert run["brain"], "the life must reach at least one night for this test to mean anything"
    for n in run["brain"]:
        u = np.asarray(n["u"])
        assert u.shape == (n["H"], 15)
        # q learner: td instruments from sleep_end, wake_entropy from sleep_start, all copied as-is
        for k in ("td_abs", "entropy", "w_norm", "wake_entropy", "surprise"):
            assert k in n
    ends = [e for e in run["events"] if e["kind"] == "sleep_end"]
    assert [n["td_abs"] for n in run["brain"]] == [e["td_abs"] for e in ends[:len(run["brain"])]]


def test_export_default_life_has_12_inputs(tmp_path):
    run, meta = _life(tmp_path, "pg12")
    assert len(run["input_names"]) == 12 and run["input_names"] == meta["config"]["input_names"]
    m = run["meta"]
    assert m["brain_dim"] == 12 and m["act_mode"] == "softmax" and m["learner"] == "pg"
    assert run["brain"]
    for n in run["brain"]:
        assert np.asarray(n["u"]).shape == (n["H"], 12)
        assert "td_abs" not in n                       # pg logs no TD instrument
        assert "clip_frac" in n


def test_export_fallback_only_when_meta_lacks_names():
    names, src = ex.input_names({"config": {}}, None)
    assert names == ex.INPUT_NAMES and src == "fallback-legacy-12"
    names, src = ex.input_names({"config": {}}, [{"u": [[0.0] * 15]}])
    assert names is None and src == "absent"           # never mislabel a 15-wide brain with 12 names
    names, src = ex.input_names({"config": {"input_names": ["a", "b"]}}, None)
    assert names == ["a", "b"] and src == "meta"


def test_cli_defaults_equal_dataclass_defaults():
    assert runcli.build_config([]) == SimConfig()
    c = runcli.build_config([])
    assert (c.brain.T, c.brain.lr, c.day_len) == (0.3, 1.0, 300)   # EXP-01's configuration


def test_cli_overrides_only_given_flags():
    c = runcli.build_config(["--learner", "q", "--alpha-q", "0.05", "--alpha-v", "0.2", "--gamma", "0.8",
                             "--sign-features", "--act-mode", "egreedy", "--T", "0.5", "--seed", "7"])
    ref = SimConfig()
    assert (c.learner, c.alpha_q, c.alpha_v, c.gamma, c.seed) == ("q", 0.05, 0.2, 0.8, 7)
    assert c.sense.sign_features is True and c.brain.act_mode == "egreedy" and c.brain.T == 0.5
    assert c.brain.lr == ref.brain.lr and c.day_len == ref.day_len and c.day_learning == ref.day_learning
