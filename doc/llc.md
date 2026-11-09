# LLC stage and LLC controller

![LLC](../asset/llc.png)

## Power stage (`DUAL LLC`)

`DUAL LLC` is a configurable subsystem of the model, set by `LLC.Stage`:

| Configuration | Content |
|---|---|
| 1 Dual LLC | two `Power/LLC` blocks, inputs and outputs in parallel, same gate signals |
| 2 Single LLC | one `Power/LLC` |
| 3 Pass | DC link wired straight to the DC filter (PFC-only runs) |

Each `Power/LLC` block (configuration `LLC.Config`) contains:

- a full-bridge primary: `HS1`/`LS1`, `HS2`/`LS2`, with the switch struct `LLC.HS1`;
- the series resonant inductor `L_r`, the resonant capacitor `C_r` and the parallel inductor `L_k`;
- the transformer `Tr` (`LLC.Trafo`; 1 Ideal uses only the turns ratio, 2 Real uses the core and gap model);
- a full-bridge rectifier: synchronous switches `SRHS1 …` in `LLC SR` (config 1), or diodes in `LLC AR` (config 2, the default);
- the output filter `L` and `C_o`.

The gate input is an 8-element vector `[HS1 LS1 HS2 LS2 SRHS1 SRLS1 SRHS2 SRLS2]`.

### Tank

| | Value |
|---|---|
| f_r = 1/(2π√(L_r C_r)) | 116 kHz |
| Z_0 = √(L_r/C_r) | 1.14 Ω |
| L_n = L_k / L_r | 3.2 |
| Turns ratio | 1:1 (4:4) |
| Q at 7 kW / 400 V (R_ac = 8/π² · R_load = 18.5 Ω) | 0.06 |

Q is very low, so the gain curve is flat. Above resonance the gain only falls towards L_n/(L_n+1) = 0.76, which puts the lowest reachable output at about 0.76 × 400 V ≈ 305 V. The 300 V setpoint therefore ends at `f_max` (303 V). The gain peak (start of the capacitive region) is near f_r/√(1+L_n) ≈ 57 kHz, so `f_min` = 70 kHz.

## Controller (`LLC CTRL`)

`LLC CTRL` is a configurable subsystem (`CTRL.LLC_Config`). Both configurations contain the same C-Script gate generator. It runs on a variable sample time with one hit per gate edge, so the edges are exact at any frequency:

- The two bridge diagonals alternate: HS1 + LS2 (+ SRHS1 + SRLS2), then LS1 + HS2 (+ SRLS1 + SRHS2).
- Each half period is 1/(2f) − `T_dt_llc`, followed by `T_dt_llc` of dead time.
- Gates stay off until `CTRL.t_llc_en`.
- Output 2 is the switching frequency (`Goto f_LLC`).

| Config | Frequency |
|---|---|
| 1 VF PI (output voltage) | Once per switching period: f = f_max − (Kp·e + ∫Ki·e), with e = v_ref − v_out, clamped to [`f_min`, `f_max`] with anti-windup. v_ref ramps from the measured output to `Vset` at `slew_llc` (soft start from `f_max`). v_out is the `Vo` voltmeter, sampled once per period. |
| 2 Fixed frequency | f = `CTRL.f_llc` (default f_r), open loop |

Tuning: near f_r the plant is about ΔV_out/Δf ≈ V_in · 0.62 / f_r ≈ 2 mV/Hz, with the output RC pole at about 14 Hz. `Kp_llc` = 2000 Hz/V gives a crossover of about 50 Hz, and the PI zero (`Ki_llc` = Kp·2π·14) cancels the output pole.

### Limitations

- **`LLC SR` with ideal switches fails** with "state discontinuity". The rectifier gates are switched in phase with the primary diagonals, without current sensing. Use `LLC AR` (diodes), or add SR timing with a conduction check, before you use config 1.
- Both LLCs of `Dual LLC` get the same gates (no interleaving, no current sharing control).
- The start at `f_max` still charges `C_o` to ~0.76 × V_DC almost at once; there is no burst or pre-charge mode.
