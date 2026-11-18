"""Referenzdaten Benjadi & Egger (2026), Zenodo 10.5281/zenodo.20623730 (CC-BY-4.0).

Die Dateien werden unverändert abgelegt. Die md5-Werte stammen aus der Zenodo-API
(abgerufen 2026-11-09) und sind Teil des Provenienzvertrags: Eine abweichende Datei
wird nie still verwendet.

Aufruf (aus 01_PRL_CODE):  python -B -m _05_INFRASTRUKTUR.referenzdaten.zenodo_benjadi_egger --laden
"""
from __future__ import annotations

import argparse
import hashlib
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import numpy as np

PROJEKT_ROOT = Path(__file__).resolve().parents[3]
DATEN_ORDNER = PROJEKT_ROOT / "03_Quellen" / "Referenzdaten_Zenodo_20623730"
ZENODO_RECORD = "20623730"
ZENODO_DOI = "10.5281/zenodo.20623730"
LIZENZ = "CC-BY-4.0"
ZITATION = ("S. M. Benjadi, R. Egger, Parity readout in Majorana box qubits from the dispersive "
            "to the resonant regime [Data set], Zenodo (2026), doi:10.5281/zenodo.20623730")

ERWARTETE_MD5: dict[str, str] = {
    "fig2a.dat": "7501484ecee0b76a97e10b14be375e1f",
    "fig2b.dat": "6a4e53c65fd900611ff10ab29a2b8eae",
    "fig3a.dat": "3e54e58cf919a7aa9e1e1a8c7e257618",
    "fig3b.dat": "9f52df8e24bc47559b73f323fe33197a",
    "fig3c.dat": "c8d8d3df89c151eb5aa9069c9774bfc6",
    "fig3d.dat": "ed2d25c373a80335e34a75d096e431a1",
    "fig3e.dat": "dc7ecaaa771166fc1515f1a58408a133",
    "fig3f.dat": "f34621c18c2e501cb29d2b8a874cf972",
    "fig3g.dat": "969e52a731eea2ab6bca3382b307879f",
    "fig3h.dat": "c220fe4fc0d30db0002de39f0f96f87a",
    "fig4.dat": "20293820c8c66c0e9b5bae256f6eebd4",
    "fig5a.dat": "e577a1bc899a222dea69aeede76f6b3a",
    "fig5b.dat": "738ef3f59a6be8f9a774be3015cb90a8",
}


class ReferenzdatenFehler(RuntimeError):
    """Referenzdatei fehlt oder weicht vom Provenienzvertrag ab."""


@dataclass(frozen=True)
class Referenzdatei:
    name: str
    pfad: Path
    md5: str
    sha256: str
    daten: np.ndarray


def _hash(pfad: Path, algorithmus: str) -> str:
    h = hashlib.new(algorithmus)
    with pfad.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def lade_referenzdatei(name: str) -> Referenzdatei:
    if name not in ERWARTETE_MD5:
        raise ReferenzdatenFehler(f"Unbekannte Referenzdatei {name}")
    pfad = DATEN_ORDNER / name
    if not pfad.is_file():
        raise ReferenzdatenFehler(f"{pfad} fehlt; zuerst mit --laden herunterladen")
    md5 = _hash(pfad, "md5")
    if md5 != ERWARTETE_MD5[name]:
        raise ReferenzdatenFehler(f"{name}: md5 {md5} != erwartet {ERWARTETE_MD5[name]}")
    daten = np.loadtxt(pfad, dtype=np.float64, ndmin=2)
    return Referenzdatei(name=name, pfad=pfad, md5=md5, sha256=_hash(pfad, "sha256"), daten=daten)


def herunterladen(ueberschreiben: bool = False) -> list[str]:
    DATEN_ORDNER.mkdir(parents=True, exist_ok=True)
    protokoll: list[str] = []
    for name, md5_soll in ERWARTETE_MD5.items():
        ziel = DATEN_ORDNER / name
        if ziel.exists() and not ueberschreiben:
            if _hash(ziel, "md5") != md5_soll:
                raise ReferenzdatenFehler(f"Vorhandene Datei {name} weicht ab; nicht überschrieben")
            protokoll.append(f"{name}: vorhanden, md5 ok")
            continue
        url = f"https://zenodo.org/records/{ZENODO_RECORD}/files/{name}?download=1"
        temp = ziel.with_suffix(".part")
        with urllib.request.urlopen(url, timeout=60) as antwort, temp.open("wb") as handle:
            handle.write(antwort.read())
        md5_ist = _hash(temp, "md5")
        if md5_ist != md5_soll:
            temp.unlink()
            raise ReferenzdatenFehler(f"{name}: Download-md5 {md5_ist} != {md5_soll}")
        temp.replace(ziel)
        protokoll.append(f"{name}: geladen, md5 ok")
    sha_zeilen = [f"{_hash(DATEN_ORDNER / n, 'sha256')}  {n}" for n in ERWARTETE_MD5]
    (DATEN_ORDNER / "SHA256SUMS.txt").write_text("\n".join(sha_zeilen) + "\n", encoding="utf-8", newline="\n")
    return protokoll


def main() -> int:
    parser = argparse.ArgumentParser(description="Zenodo-Referenzdaten Benjadi & Egger laden/prüfen")
    parser.add_argument("--laden", action="store_true")
    args = parser.parse_args()
    if args.laden:
        for zeile in herunterladen():
            print(zeile)
    for name in ERWARTETE_MD5:
        datei = lade_referenzdatei(name)
        print(f"{name}: shape={datei.daten.shape}, x=[{datei.daten[:,0].min():.4g}, {datei.daten[:,0].max():.4g}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
