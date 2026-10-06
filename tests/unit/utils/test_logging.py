"""Phase 02 tests for `janus/utils/logging.py`.

Spec required tests: format and levels. CPU only, no tensors required.
"""

from __future__ import annotations

import json
import logging as stdlib_logging
from pathlib import Path

import pytest
import torch

from janus.utils.logging import (
    LEVELS,
    RESERVED_KEYS,
    JsonlLogger,
    LogError,
    read_records,
)


def _read_raw_lines(path: Path) -> list[str]:
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line]


# ---------------------------------------------------------------------------
# format
# ---------------------------------------------------------------------------
def test_writes_one_valid_json_object_per_line(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path, run_id="run-1") as log:
        log.info("start", lr=1e-3)
        log.error("boom", code=5)

    lines = _read_raw_lines(path)
    assert len(lines) == 2
    for line in lines:
        record = json.loads(line)  # must be strict JSON (no NaN literal)
        assert isinstance(record, dict)

    records = read_records(path)
    assert records[0]["event"] == "start"
    assert records[0]["level"] == "INFO"
    assert records[0]["run_id"] == "run-1"
    assert records[0]["lr"] == pytest.approx(1e-3)
    assert records[0]["ts"].endswith("Z")
    assert records[1]["event"] == "boom"
    assert records[1]["level"] == "ERROR"
    assert records[1]["code"] == 5


def test_record_envelope_keys_present(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path) as log:
        log.info("x")
    record = read_records(path)[0]
    for key in ("ts", "level", "event"):
        assert key in record


def test_context_fields_merged_into_every_record(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path, context={"experiment_id": "e1"}) as log:
        log.set_context(seed=7)
        log.info("a")
        log.warning("b")
    records = read_records(path)
    assert [r["experiment_id"] for r in records] == ["e1", "e1"]
    assert [r["seed"] for r in records] == [7, 7]


def test_context_rejects_reserved_keys(tmp_path: Path) -> None:
    with JsonlLogger(tmp_path / "run.jsonl") as log:
        with pytest.raises(LogError, match="reserved"):
            log.set_context(level="INFO")


def test_append_mode(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path) as log:
        log.info("first")
    with JsonlLogger(path) as log:
        log.info("second")
    assert [r["event"] for r in read_records(path)] == ["first", "second"]


def test_creates_parent_directories(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "dirs" / "run.jsonl"
    with JsonlLogger(path) as log:
        log.info("x")
    assert path.is_file()


def test_tensor_fields_are_converted(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path) as log:
        log.info("tensors", scalar=torch.tensor(1.5), matrix=torch.zeros(2, 3))
    record = read_records(path)[0]
    assert record["scalar"] == pytest.approx(1.5)
    assert record["matrix"] == {"shape": [2, 3], "dtype": "torch.float32"}
    json.dumps(record)  # still serialisable


def test_non_finite_floats_become_strings(tmp_path: Path) -> None:
    """Strict JSON: the invalid `NaN` literal must never be written."""
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path) as log:
        log.info("bad", loss=float("nan"), grad=float("inf"), neg=-float("inf"))
    line = _read_raw_lines(path)[0]
    assert "NaN" in line and "Infinity" in line
    record = json.loads(line)
    assert record["loss"] == "NaN"
    assert record["grad"] == "Infinity"
    assert record["neg"] == "-Infinity"


def test_nested_structures_sanitised(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    payload = {"a": {"b": [1, 2.5, None, True]}, "path": Path("x/y")}
    with JsonlLogger(path) as log:
        log.info("nested", **payload)
    record = read_records(path)[0]
    assert record["a"]["b"] == [1, 2.5, None, True]
    assert record["path"] == str(Path("x/y"))  # Path -> str (OS-specific separators)


def test_cycle_guard_does_not_crash(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    cyclic: dict = {"name": "loop"}
    cyclic["self"] = cyclic
    with JsonlLogger(path) as log:
        log.info("cyclic", payload=cyclic)
    assert read_records(path)[0]["payload"]["self"] == "<cycle>"


# ---------------------------------------------------------------------------
# levels
# ---------------------------------------------------------------------------
def test_level_filtering(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path, level="WARNING") as log:
        assert log.debug("d") is False
        assert log.info("i") is False
        assert log.warning("w") is True
        assert log.error("e") is True
        assert log.critical("c") is True
    assert [r["event"] for r in read_records(path)] == ["w", "e", "c"]


def test_all_levels_pass_at_debug(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path, level="DEBUG") as log:
        for name in LEVELS:
            assert log.log(name, name.lower()) is True
    assert len(read_records(path)) == len(LEVELS)


def test_level_names_written_uppercase(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    with JsonlLogger(path, level="debug") as log:
        assert log.log("info", "lowercase_level") is True
    assert read_records(path)[0]["level"] == "INFO"


def test_unknown_level_rejected(tmp_path: Path) -> None:
    with pytest.raises(LogError, match="unknown level"):
        JsonlLogger(tmp_path / "never_created.jsonl", level="LOUD")
    assert not (tmp_path / "never_created.jsonl").exists()
    with pytest.raises(LogError, match="unknown level"):
        with JsonlLogger(tmp_path / "run.jsonl") as log:
            log.log("LOUD", "x")


def test_reserved_field_key_rejected(tmp_path: Path) -> None:
    with JsonlLogger(tmp_path / "run.jsonl") as log:
        # keys that are not method parameters can be passed as fields
        for key in ("ts", "run_id"):
            with pytest.raises(LogError, match="reserved"):
                log.info("x", **{key: "v"})
        # every reserved key is rejected as a persistent context field
        for key in sorted(RESERVED_KEYS):
            with pytest.raises(LogError, match="reserved"):
                log.set_context(**{key: "v"})
        # convenience methods surface LogError, not a TypeError from forwarding
        with pytest.raises(LogError, match="reserved"):
            log.info("x", level="INFO")


def test_empty_event_rejected(tmp_path: Path) -> None:
    with JsonlLogger(tmp_path / "run.jsonl") as log:
        with pytest.raises(LogError, match="event"):
            log.info("")


def test_closed_logger_rejects_writes(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    log = JsonlLogger(path)
    log.info("x")
    log.close()
    assert log.closed is True
    with pytest.raises(LogError, match="closed"):
        log.info("y")
    log.close()  # idempotent


def test_log_exception_captures_traceback(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    log = JsonlLogger(path)
    try:
        raise ValueError("kaboom")
    except ValueError:
        log.log_exception("failure", phase="unit")
    log.close()
    record = read_records(path)[0]
    assert record["event"] == "failure"
    assert record["level"] == "ERROR"
    assert "ValueError: kaboom" in record["traceback"]


def test_console_mirroring_does_not_break_file(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    logger = stdlib_logging.getLogger("janus.jsonl")
    old_level = logger.level
    logger.setLevel(stdlib_logging.CRITICAL)  # silence stderr noise in the test
    try:
        with JsonlLogger(path, console=True) as log:
            log.info("mirrored", v=1)
    finally:
        logger.setLevel(old_level)
    assert read_records(path)[0]["event"] == "mirrored"


# ---------------------------------------------------------------------------
# read-back
# ---------------------------------------------------------------------------
def test_read_records_rejects_malformed_line(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text('{"ok": 1}\nnot json\n', encoding="utf-8")
    with pytest.raises(LogError, match="malformed JSONL line"):
        read_records(path)


def test_read_records_rejects_non_object_line(tmp_path: Path) -> None:
    path = tmp_path / "bad.jsonl"
    path.write_text('"just a string"\n', encoding="utf-8")
    with pytest.raises(LogError, match="is not an object"):
        read_records(path)


def test_read_records_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "run.jsonl"
    path.write_text('{"a": 1}\n\n{"a": 2}\n', encoding="utf-8")
    assert len(read_records(path)) == 2
