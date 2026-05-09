import gnomon


def test_version() -> None:
    assert gnomon.__version__ == "0.0.1"


def test_public_imports() -> None:
    from gnomon.agents.base import Agent
    from gnomon.eval.runner import EvalRunner
    from gnomon.storage.db import connect, init_db, insert_results, insert_run
    from gnomon.types import EvalCase, EvalResult, EvalRun

    assert Agent is not None
    assert EvalRunner is not None
    assert all(callable(f) for f in (connect, init_db, insert_results, insert_run))
    assert all(c is not None for c in (EvalCase, EvalResult, EvalRun))
