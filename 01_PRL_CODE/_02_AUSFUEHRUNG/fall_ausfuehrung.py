"""Ein vollständiger stationärer Rechenfall: Modell bauen, lösen, auswerten."""
from __future__ import annotations

from dataclasses import dataclass

from _01_GRUNDLAGEN_FORMELN.abgeleitete_groessen import AbgeleiteteGroessen
from _01_GRUNDLAGEN_FORMELN.operatoren_rwa import baue_rwa_modell
from _01_GRUNDLAGEN_FORMELN import semiklassik
from _02_AUSFUEHRUNG.stationaer_loeser import StationaerErgebnis, loese_stationaer
from _04_AUSWERTUNG_DIAGNOSTIK import fehlermasse as fm
from _05_INFRASTRUKTUR.konfiguration.config import ParameterBuendel


@dataclass(frozen=True)
class FallErgebnis:
    groessen: AbgeleiteteGroessen
    loesung: StationaerErgebnis
    exakt: fm.ExakteErwartungswerte
    A_ref: complex
    A_semikl: complex
    a_semikl: complex
    tau_z_semikl: float
    eps_a_tau_z: float
    eps_a_tau_z_gegen_semikl: float
    eps_A: float
    eps_phi: float


def rechne_fall(b: ParameterBuendel) -> FallErgebnis:
    m, d = b.modell, b.antrieb
    ops = baue_rwa_modell(b)
    g = ops.groessen
    loesung = loese_stationaer(ops, b.numerik.loeser, kappa=m.kappa,
                               gamma_min=max(m.gamma, m.gamma_phi, 1e-12),
                               max_fock=b.numerik.max_oberste_fock_population)
    w = fm.erwartungswerte(ops, loesung.rho)
    A_ref = fm.amplitude_exakt(w, m.kappa_out, d.I0)
    A_sc = semiklassik.amplitude_semiklassisch_stark(m, g)
    a_sc = semiklassik.a_semiklassisch_stark(m, d, g)
    tz_sc = semiklassik.tau_z_thermisch(g, m.temperatur)
    return FallErgebnis(
        groessen=g, loesung=loesung, exakt=w, A_ref=A_ref, A_semikl=A_sc, a_semikl=a_sc, tau_z_semikl=tz_sc,
        eps_a_tau_z=fm.fehler_faktorisierung(w),
        eps_a_tau_z_gegen_semikl=fm.fehler_faktorisierung_gegen_semiklassik(w, a_sc, tz_sc),
        eps_A=fm.fehler_amplitude(A_sc, A_ref), eps_phi=fm.fehler_phase(A_sc, A_ref),
    )
