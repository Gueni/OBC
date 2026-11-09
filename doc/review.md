# Review of the simulations (November 2026)

What was wrong in the PLECS and LTspice simulations, what was changed, and what is still open.

## PLECS

| Problem | Fix |
|---|---|
| `OBC.plecs` / `PFC.plecs` failed at start: `EMI FILTER` set to configuration 5 (the library now has 1–3); the old parameter file no longer matched the library blocks (switch, filter, load structs). | New `model/OBC.plecs` built from the library-based 1 kW PFC model (`0049_SP_BTP_PFC_1KW`), scaled to 7 kW, with every configuration a `ModelVars` field. `lib/vars.py` follows the current library structs. |
| `DUAL LLC` in **Pass** tied the DC-bus negative to PE: through the earthed grid and the totem-pole slow leg this shorts the grid (kA in the grid, ~1 % efficiency). The old OBC model ran with Pass. | PE branch removed from the Pass configuration. |
| `DUAL LLC` inner LLC blocks hardcoded to configuration 2; `DC FILTER`, `CDC`, `Load`, `PFC`, `PFC CTRL` configurations hardcoded. | All set from `LLC.Config`, `HV_Filter.Config`, `DCLink.Config`, `Load.Config`, `PFC.Config`. |
| The full OBC never simulated its LLC (`DUAL LLC` = Pass). The LLC controller had the 450 V target, the gains and a t = 0 enable hardcoded, so the `CTRL.Vset` sweep of the old script did nothing. | New `LLC CTRL` configurable subsystem (VF PI / fixed frequency) with all values in `CTRL`; LLC enabled after the PFC soft start. Full OBC regulates 300–450 V at 7 kW. |
| Old PFC controller: carrier 100 kHz but one sampler at 75 kHz; dead time 900 ns in one model, 300 ns in the other; DC-link reference 400 V in `OBC.plecs`, 450 V in `PFC.plecs`. | Replaced by the library `PFC CTRL` (average current mode, gains computed from L_boost and C_out in `Derived`). |
| Data export of the old OBC model commented out (mux widths did not match the probes); CSV without signal names. | Data export of the library model; names read by `SignalNames`. |
| `Trafo.plecs`: the `Tr1` transformer got an empty struct ("scalar cannot be indexed"); core loss Rc = 10 Ω (16 kW at 400 V), secondary Rs = 10 Ω. | Struct `Trafo` passed; Rc = 10 kΩ, Rs = 10 mΩ (also in `vars.LLC.Trafo`). |
| PFC choke 30 mH / 40 µH with Lm 1 mH (Lm > L2: not a physical coupled inductor). | L_boost = 98 µH (30 % ripple at 7 kW / 80 kHz). |
| Y capacitors 4.7 pF. | 4.7 nF. |
| Old scripts: absolute paths of another PC, `"Modeling and Simulation/..."` paths that no longer existed, Cx/Cy swapped in the DC filter sweep. | `main.py` / `analysis.py` + `lib/` with paths relative to the repo. |

## LTspice

| File | Problem | Fix |
|---|---|---|
| `LLCSoftSwitching.asc` | No `K L1 L2` statement: the transformer was not coupled. The primary tank node was labelled `Vo`, so it was shorted to the output. `.tran` of 10 s at 400 kHz. 30 V MOSFETs (Si7336ADP) on a 600 V bus. | `K L1 L2 1`; tank node `Vtank`; `.tran 0 3m 2.9m 5n`; IPB65R420CFD (700 V, CFD) with 12 V gate drive. Vo 28 V. |
| `LLCSoftSwitchingSynchRectifier.asc` | 30 V primary MOSFETs; 420 µs run (not settled). | IPB65R420CFD, 12 V gates, 3 ms. Vo 29.3 V. |
| `LLC_Simulation.asc` | Bridge return (E1 −) floating; `.meas` on `V(V_Bus)`, `I(V1)` (do not exist) and `I(R1)` (the VCO resistor, not the load); RMS of power instead of the average, measured at 3.5–5 ms of a 100 ms run (133 MB raw file). | E1 − grounded, `Vbus` label; `.meas` AVG of −V(Vbus)·I(E1) and V(Vout)·I(R16) over 25–30 ms of a 30 ms run. η = 91.5 %. |
| `Trafo.asc` | "Ideal" windings of 1 µH / 2 µH added to Lm (not ideal, ratio √2); Rc 10 Ω; C1 = 100 F (`100E`); 10 kHz drive with 1 s run at 1 ms max step; the DC operating point started the pulse source at −400 V across shorted inductors (MA). | 10 mH ideal windings, n parameter (1:1); Rc 10 kΩ; C1 100 pF, 1 MΩ reference; drive at f_r, 200 periods; `uic` + centred magnetizing current. |
| `Input_Filter.asc` | V3/V4 `AC 230` while the others are `AC 1`; leftover VCCS loop and `1Z` capacitor on the PE node; `1E` value. | `AC 1` everywhere; leftovers removed; R12 = 1 Ω. |

## Still open

- **LLC magnetics.** Lm = 4.5 µH (4 turns, 3 mm gap, 676 mm² core) and Z₀ = 1.1 Ω are far too small for 7 kW: 382 A p-p magnetizing current at f_r, Q = 0.06, and the output cannot go below ~305 V from a 400 V bus. A 7 kW / 400 V LLC typically needs L_r in the tens of µH and L_m of ~100–300 µH (more turns or a smaller gap).
- **SR timing** of `LLC SR` (see [llc.md](llc.md)).
- **EMI filter values** are those of the 1 kW reference filter (10 A chokes); scale them for 32 A in the real design.
- The `real` mode (physical switch models) is set up but was not run over a full 0.3 s (hours of run time).
