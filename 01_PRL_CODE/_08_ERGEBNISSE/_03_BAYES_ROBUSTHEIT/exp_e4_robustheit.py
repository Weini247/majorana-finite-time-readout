"""EXP-E4: Robustheit der Arbeitspunktwahl gegen Parameterabweichungen (Gauß-Benchmark, Etappe 3, Q-3B).

Spezifikation: 02_FORSCHUNGSDOKUMENTATION/_03_EXPERIMENTE/EXP-E4_Robustheit_Gauss.md (vorab registriert).
Kalibrierung (I0, θ, Filtergewichte, Schwelle) am Nominalmodell; Messdaten aus dem abweichenden „wahren" Modell.
Aufruf aus 01_PRL_CODE:  python -B -u -m _08_ERGEBNISSE._03_BAYES_ROBUSTHEIT.exp_e4_robustheit
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, replace

import numpy as np
from scipy.special import erfc

from _02_AUSFUEHRUNG.homodyn_trajektorien import messkanal_rwa, mittelwert_record
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT, neue_lauf_id, schreibe_manifest
from _08_ERGEBNISSE._02_ENDLICHE_MESSZEIT.exp_e1_endliche_messzeit import CUTOFF, ETA, _modell

E2 = "EXP-E2_20261109T205736Z"
BUDGETS = (0.3, 0.01)
T_WERTE = (2500.0, 5000.0, 10000.0)
DT_MW = 0.5


def abweichungen(m):
    k = m.kappa_in + m.kappa_out
    aus = {"nominal": m}
    for dphi in (-0.2, -0.1, 0.1, 0.2):
        aus[f"phi{dphi:+.1f}"] = replace(m, phi=m.phi + dphi)
    for f in (0.95, 1.05):
        aus[f"t1x{f}"] = replace(m, t1=m.t1 * f)
    for f in (0.8, 1.2):
        aus[f"kappax{f}"] = replace(m, kappa_in=m.kappa_in * f, kappa_out=m.kappa_out * f)
    assert abs(k - (m.kappa_in + m.kappa_out)) < 1e-15
    return aus


def _phi(x):
    return 0.5 * erfc(-x / math.sqrt(2.0))


def fehlerraten(mu_nom, mu_wahr, idx):
    """Linearer Filter mit Nominalgewichten und -schwelle, Daten aus dem wahren Modell (weißes Rauschen, Varianz dt)."""
    w = 0.5 * ((mu_nom[1] - mu_nom[-1])[1:] + (mu_nom[1] - mu_nom[-1])[:-1])
    mitte = 0.25 * ((mu_nom[1] + mu_nom[-1])[1:] + (mu_nom[1] + mu_nom[-1])[:-1])
    mp = 0.5 * (mu_wahr[1][1:] + mu_wahr[1][:-1]); mm = 0.5 * (mu_wahr[-1][1:] + mu_wahr[-1][:-1])
    cw2, cwp, cwm, cwt = (np.cumsum(a) * DT_MW for a in (w * w, w * mp, w * mm, w * mitte))
    dw = (mp - mm) ** 2
    cdw = np.cumsum(dw) * DT_MW
    out = {}
    for T, i in idx.items():
        s = math.sqrt(cw2[i - 1]) if cw2[i - 1] > 0 else 1e-300
        p_fest = 0.5 * (_phi((cwt[i - 1] - cwp[i - 1]) / s) + _phi((cwm[i - 1] - cwt[i - 1]) / s))
        p_orakel = 0.5 * erfc(math.sqrt(cdw[i - 1]) / (2 * math.sqrt(2)))     # neu kalibriert am wahren Modell
        out[T] = (p_fest, p_orakel)
    return out


def main() -> int:
    lauf_id = neue_lauf_id("EXP-E4")
    roh, aus = PROJEKT_ROOT / "10_Raw_Outputs" / lauf_id, PROJEKT_ROOT / "11_Processed_Outputs" / lauf_id
    roh.mkdir(parents=True, exist_ok=True); aus.mkdir(parents=True, exist_ok=True)
    m0 = _modell(); modelle = abweichungen(m0)
    schreibe_manifest(roh, {"lauf_id": lauf_id, "experiment": "EXP-E4", "quelle_e2": E2, "budgets": BUDGETS,
                            "T_werte": T_WERTE, "eta": ETA, "abweichungen": {k: asdict(v) for k, v in modelle.items()}})
    zeiten = np.arange(0.0, max(T_WERTE) + 1e-9, DT_MW)
    idx = {T: int(round(T / DT_MW)) for T in T_WERTE}
    zusammenfassung = {}
    for budget in BUDGETS:
        nc = CUTOFF[budget]
        with (PROJEKT_ROOT / "11_Processed_Outputs" / E2 / f"gauss_scan_n{budget}.csv").open(encoding="utf-8") as h:
            scan = [{k: float(v) for k, v in z.items()} for z in csv.DictReader(h)]
        zeilen = []
        for ap in scan:
            mu = {}
            for name, mod in modelle.items():
                mu[name] = {z: mittelwert_record(messkanal_rwa(buendel(mod, ap["omega"], ap["I0"], nc, paritaet=z),
                                                               eta=ETA, theta=ap["theta"])[0], zeiten) for z in (1, -1)}
            for name in modelle:
                for T, (pf, po) in fehlerraten(mu["nominal"], mu[name], idx).items():
                    zeilen.append({"budget": budget, "omega": ap["omega"], "abweichung": name, "T": T,
                                   "P_fest": pf, "P_orakel": po})
            with (aus / f"exp_e4_n{budget}.csv").open("w", newline="", encoding="utf-8") as h:
                wtr = csv.DictWriter(h, fieldnames=list(zeilen[0].keys())); wtr.writeheader(); wtr.writerows(zeilen)
            print(f"n={budget} omega={ap['omega']:.2f} fertig", flush=True)
        # Auswertung: Mittel und Worst-Case über die Abweichungen (feste Nominalkalibrierung)
        res = {}
        oms = sorted({z["omega"] for z in zeilen})
        for T in T_WERTE:
            wc = {o: max(z["P_fest"] for z in zeilen if z["omega"] == o and z["T"] == T) for o in oms}
            mi = {o: float(np.mean([z["P_fest"] for z in zeilen if z["omega"] == o and z["T"] == T])) for o in oms}
            nom = {o: [z["P_fest"] for z in zeilen if z["omega"] == o and z["T"] == T and z["abweichung"] == "nominal"][0] for o in oms}
            o_nom = min(oms, key=nom.get); o_wc = min(oms, key=wc.get); o_mi = min(oms, key=mi.get)
            res[str(int(T))] = {"omega_nominal": o_nom, "omega_worstcase": o_wc, "omega_mittel": o_mi,
                                "P_wc_bei_omega_nominal": wc[o_nom], "P_wc_opt": wc[o_wc],
                                "regret_worstcase": wc[o_nom] - wc[o_wc],
                                "P_mittel_bei_omega_nominal": mi[o_nom], "P_mittel_opt": mi[o_mi],
                                "regret_mittel": mi[o_nom] - mi[o_mi]}
        zusammenfassung[str(budget)] = res
        print(json.dumps(res, indent=1), flush=True)
        (aus / "ergebnis.json").write_text(json.dumps(zusammenfassung, indent=2), encoding="utf-8")
    print("Ausgabe:", aus)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
