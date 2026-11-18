"""Kanonischer Testlauf: aktive Tests (_06_TESTS) und wissenschaftliche Prüfungen (VAL*).

Aufruf aus 01_PRL_CODE:  python -B -m _05_INFRASTRUKTUR.run_checks --scope all
Die gesammelte Testanzahl muss EXPECTED_COUNTS entsprechen; Abweichungen sind Fehler.
"""
from __future__ import annotations

import argparse
import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THREAD_VARIABLES = ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS")
LOCAL_PACKAGES = ("_01_GRUNDLAGEN_FORMELN", "_02_AUSFUEHRUNG", "_03_WISSENSCHAFTLICHE_PRUEFUNGEN",
                  "_04_AUSWERTUNG_DIAGNOSTIK", "_05_INFRASTRUKTUR")
EXPECTED_COUNTS = {"active": 37, "scientific": 21, "all": 58}


def configure_process(temp: Path) -> None:
    sys.dont_write_bytecode = True
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["MPLBACKEND"] = "Agg"
    os.environ["MPLCONFIGDIR"] = str(temp / "matplotlib")
    for v in THREAD_VARIABLES:
        os.environ[v] = "1"
    os.chdir(ROOT)
    if str(ROOT) in sys.path:
        sys.path.remove(str(ROOT))
    sys.path.insert(0, str(ROOT))


def verify_local_imports() -> None:
    for name in LOCAL_PACKAGES:
        origin = Path(importlib.import_module(name).__file__).resolve()
        if not origin.is_relative_to(ROOT):
            raise RuntimeError(f"{name} wurde außerhalb des Projektroots importiert: {origin}")


def build_suite(scope: str) -> unittest.TestSuite:
    loader = unittest.defaultTestLoader
    active = lambda: loader.discover(str(ROOT / "_06_TESTS"), pattern="test*.py", top_level_dir=str(ROOT))
    scientific = lambda: loader.discover(str(ROOT / "_03_WISSENSCHAFTLICHE_PRUEFUNGEN"), pattern="val*.py",
                                         top_level_dir=str(ROOT))
    if scope == "active":
        return active()
    if scope == "scientific":
        return scientific()
    if scope == "all":
        return unittest.TestSuite([active(), scientific()])
    raise ValueError(f"Unbekannter scope {scope}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Kanonischer Test von ParityReadoutLab")
    parser.add_argument("--scope", choices=tuple(EXPECTED_COUNTS), default="active")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="prl_checks_") as temp:
        configure_process(Path(temp))
        verify_local_imports()
        suite = build_suite(args.scope)
        anzahl = suite.countTestCases()
        if anzahl != EXPECTED_COUNTS[args.scope]:
            print(f"FEHLER: {anzahl} Tests gesammelt, erwartet {EXPECTED_COUNTS[args.scope]}")
            return 2
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        if result.skipped:
            print(f"FEHLER: {len(result.skipped)} übersprungene Tests")
            return 3
        return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
