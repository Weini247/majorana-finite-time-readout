"""Provenienz eines Laufs (QuTiP, Seeds und Eingabehashes)."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

CODE_ROOT = Path(__file__).resolve().parents[2]
PROJEKT_ROOT = CODE_ROOT.parent
LOCKFILE = CODE_ROOT / "_05_INFRASTRUKTUR" / "requirements-lock.txt"
PAKETE = ("numpy", "scipy", "qutip", "matplotlib")


def sha256_datei(pfad: str | Path) -> str:
    h = hashlib.sha256()
    with Path(pfad).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _git(*argumente: str) -> str | None:
    try:
        r = subprocess.run(("git", "--no-optional-locks", *argumente), cwd=PROJEKT_ROOT,
                           capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def umgebung() -> dict[str, Any]:
    head = _git("rev-parse", "HEAD") or "unbekannt"
    status = _git("status", "--porcelain")
    return {
        "git_head": head,
        "git_dirty": True if status is None else bool(status),
        "lockfile_sha256": sha256_datei(LOCKFILE) if LOCKFILE.is_file() else "fehlt",
        "python": platform.python_version(),
        "plattform": platform.platform(),
        **{p: metadata.version(p) for p in PAKETE},
        "float": "float64/complex128",
    }


def neue_lauf_id(praefix: str) -> str:
    return f"{praefix}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def schreibe_manifest(ordner: Path, inhalt: dict[str, Any]) -> Path:
    ordner.mkdir(parents=True, exist_ok=True)
    daten = {"erstellt_utc": datetime.now(timezone.utc).isoformat(), "umgebung": umgebung(), **inhalt}
    ziel = ordner / "manifest.json"
    ziel.write_text(json.dumps(daten, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    return ziel
