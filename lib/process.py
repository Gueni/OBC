#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?              ____  _________  ________  __________
#?             / __ \/ ___/ __ \/ ___/ _ \/ ___/ ___/
#?            / /_/ / /  / /_/ / /__/  __(__  |__  )
#?           / .___/_/   \____/\___/\___/____/____/
#?          /_/
#?
#?
#? Name:        process.py
#? Purpose:     Results: HTML report and result matrices (PPlots), sweep log (PLog).
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     10/18/2026
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import  os
import  math
import  re
import  webbrowser
import  io
import  base64
import  screeninfo

import  numpy                       as      np
import  pandas                      as      pd
import  plotly.graph_objects        as      go
import  plotly.colors               as      pc

from    pathlib                     import  Path
from    plotly.subplots             import  make_subplots
from    PIL                         import  Image
from    .calc                       import  PMath
from    .plecs                      import  OUTPUT_KEY, OUTPUT_FIELDS, Sweep
from    .signals                    import  SignalNames
#?----------------------------------------------------------------------------------------------------------------------------------------
class PPlots:
    """HTML reports of simulation results."""

    PLOT_BUCKETS        = 2500                                                         # time-domain min/max bins per trace
    N_HARMONICS         = 50                                                           # harmonic orders shown in the harmonic bar plots
    ANALYSIS_CYCLES     = 5                                                            # last whole fundamental cycles used for the metrics and harmonics (None = all)

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Helpers
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def units_from_names(waveforms):
        """Unit of each waveform guessed from a keyword of its name (SignalNames.UNIT_KEYWORDS, '[ / ]' if none matches)."""
        return SignalNames.units_from_names(waveforms)

    @staticmethod
    def png_to_hex_base64(img_path):
        """Image resized to the screen and encoded as base64 PNG ('' if unavailable)."""
        if not img_path or not Path(img_path).is_file():
            print(f"Model image not found: {img_path}")
            return ''
        screen              = screeninfo.get_monitors()[0]
        size                = (int(screen.width * 0.5), int(screen.height * 0.4))
        try:
            with Image.open(img_path) as img:
                buffer      = io.BytesIO()
                img.resize(size, resample=Image.LANCZOS).save(buffer, format="PNG")
        except OSError:
            print("Unable to resize image")
            return ''
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    @staticmethod
    def flatten_dict(d):
        """Flatten a nested dict into {'a.b.c': value}."""
        return {'.'.join(map(str, p)): Sweep.get_nested(d, p) for p in Sweep.leaf_paths(d)}

    @staticmethod
    def extract_comments(filename):
        """Unit and comment of each parameter of a parameters file, keyed by its dotted path ('Grid.Vin', 'PFC.Choke.L1').
        The path follows the dict nesting of the file: a top-level 'Grid = {' is 'Grid', an entry "'Choke' : {" inside it
        is 'PFC.Choke' (so top-level dict names must be the ModelVars keys). The trailing '#?' comment of an entry is split
        into its 8-char unit field and the rest. Returns {path: (unit, comment)}."""
        found               = {}
        stack               = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                code, sep, comment = line.partition('#?')
                code        = code.split('#')[0].strip()
                top         = re.match(r"^(\w+)\s*=\s*\{", code)
                entry       = re.match(r"^'([^']+)'\s*:\s*(.*)$", code)
                if top:
                    stack   = [top.group(1)]
                elif entry and stack:
                    if entry.group(2).startswith('{'):
                        stack.append(entry.group(1))
                    elif sep:
                        found['.'.join(stack + [entry.group(1)])] = (comment[:8].strip(), comment[8:].strip())
                if code.startswith('}') and stack:
                    stack.pop()
        return found

    @staticmethod
    def find_note(notes, name):
        """(unit, comment) of a parameter: exact path first, else the documented path sharing the longest ending
        (a struct copied from another dict, e.g. PFC.SW.Rgon <- Switches.GS66508.Rgon). ('', '') if none."""
        if name in notes:
            return notes[name]
        parts               = name.split('.')
        for k in range(1, len(parts)):
            tail            = '.' + '.'.join(parts[k:])
            match           = next((v for key, v in notes.items() if key.endswith(tail)), None)
            if match:
                return match
        return ('', '')

    @staticmethod
    def _params_table(columns):
        """Plotly table with one header per key of columns and its values as cells."""
        return go.Figure(data=[go.Table(
            header          = dict(values=list(columns), fill_color='paleturquoise', align='left'),
            cells           = dict(values=list(columns.values()), fill_color='lavender', align='left'),
        )])

    @staticmethod
    def write_html(html_file, title, figures, img_b64='', OPEN=False):
        """Write figures (first one loads plotly.js) to an HTML page, with an optional base64 PNG on top."""
        img                 = (f'<div class="center"><img src="data:image/png;base64,{img_b64}" alt="{title}"></div>'
                               if img_b64 else '')
        plots               = ''.join(fig.to_html(full_html=False, include_plotlyjs='cdn' if i == 0 else False)
                                      for i, fig in enumerate(figures))
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>.center {{display: flex; justify-content: center;}}</style>
</head>
<body>
{img}
{plots}
</body>
</html>
""")
        if OPEN:
            webbrowser.open(html_file)

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Sweep report
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def format_hz(f):
        """50 -> '50 Hz', 80000 -> '80 kHz'."""
        for scale, prefix in ((1e9, 'G'), (1e6, 'M'), (1e3, 'k')):
            if abs(f) >= scale:
                return f"{f / scale:g} {prefix}Hz"
        return f"{f:g} Hz"

    @staticmethod
    def waveform_f0_paths(waveforms, f0_path=None, f0_overrides=None):
        """Key path of the fundamental of each waveform: the first f0_overrides keyword found in its name, else f0_path."""
        overrides           = f0_overrides or {}
        return [next((p for kw, p in overrides.items() if kw.lower() in w.lower()), f0_path) for w in waveforms]

    @staticmethod
    def _load_run(resFile, n, f0s=None):
        """Load one time-series CSV once and compute everything the reports need (None if the file is missing):
        't', 'Y': time-domain min/max envelopes; 'metrics': PMath.calc_metrics per waveform; 'harmonics': (orders, H);
        'window': analysis window [s]. The window is the last ANALYSIS_CYCLES whole cycles of the lowest fundamental
        (whole file without fundamental), shared by the metrics and the harmonics of the run."""
        if not os.path.isfile(resFile):
            print(f"WARNING: result CSV not found, skipped in the HTML report: {resFile}. "
                  f"The model has no 'To File' block writing to {OUTPUT_KEY}.ToFile_path.")
            return None
        try:
            with open(resFile, encoding='utf-8', errors='ignore') as f:
                named       = f.readline().lstrip()[:1] == '"'                      # To File header with the signal names
            data            = pd.read_csv(resFile, header=None, skiprows=1 if named else 0, usecols=range(n + 1), dtype=float).to_numpy()
        except (pd.errors.EmptyDataError, ValueError) as err:
            print(f"WARNING: result CSV empty or unreadable, skipped in the reports: {resFile} ({err})")
            return None
        if len(data) < 2:
            print(f"WARNING: result CSV has less than 2 samples, skipped in the reports: {resFile}")
            return None
        t, Y                = data[:, 0], data[:, 1:]
        f0s                 = f0s or [None] * n
        f_base              = min((f for f in f0s if f), default=None)
        window              = PMath.analysis_window(t, f_base, PPlots.ANALYSIS_CYCLES)
        if f_base and window is None:
            print(f"WARNING: less than one {PPlots.format_hz(f_base)} cycle saved in {resFile}: metrics over the whole file, no harmonics.")
        t_env, Y_env        = PMath.envelope(t, Y, PPlots.PLOT_BUCKETS)
        return {'t'         : t_env,
                'Y'         : Y_env,
                'metrics'   : PMath.calc_metrics(t, Y, window),
                'harmonics' : PMath.harmonics(t, Y, f0s, PPlots.N_HARMONICS, window),
                'window'    : window if window else t[-1] - t[0]}

    @staticmethod
    def _run_name(label, mv, varied):
        """Legend name of a sweep point: '#idx k1=v1, k2=v2' over the varied sweep parameters."""
        fmt                 = lambda v: f"{v:g}" if isinstance(v, (int, float)) else str(v)
        return f"#{mv[OUTPUT_KEY]['sim_idx']} " + ", ".join(f"{k}={fmt(label[k])}" for k in varied)

    @staticmethod
    def _style(fig, height=450):
        fig.update_layout(plot_bgcolor='#e9f5f9', height=height, showlegend=True)
        return fig

    @staticmethod
    def _write_metric(kind, runs, waveforms, units, labels, out):
        """mat/<kind>_<run>.csv: one row per sweep point (sim_idx + swept values), one column per waveform."""
        values              = np.array([r['metrics'][kind] for r in runs])                     # [point][waveform]
        sweep_cols          = {k: [lab[k] for lab in labels] for k in labels[0]}
        table               = pd.DataFrame({'sim_idx': [r['sim_idx'] for r in runs], **sweep_cols,
                                            **{f"{w} {u}": values[:, k] for k, (w, u) in enumerate(zip(waveforms, units))}})
        csv_file            = Path(out['Mat']) / f"{kind}_{out['utc_numeric']}.csv"
        table.to_csv(csv_file, index=False, encoding='utf-8-sig')
        return csv_file

    @staticmethod
    def _write_fft(runs, waveforms, units, labels, f0s, out):
        """mat/FFT_<run>.csv: one row per sweep point and waveform (with a fundamental): f0_Hz, H1..HN."""
        rows                = []
        for r, lab in zip(runs, labels):
            orders, H       = r['harmonics']
            for k, wave in enumerate(waveforms):
                f0          = f0s[r['index']][k]
                if f0:
                    rows.append({'sim_idx': r['sim_idx'], **lab, 'waveform': wave, 'unit': units[k], 'f0_Hz': f0,
                                 **{f"H{o}": H[k, j] for j, o in enumerate(orders)}})
        csv_file            = Path(out['Mat']) / f"FFT_{out['utc_numeric']}.csv"
        pd.DataFrame(rows).to_csv(csv_file, index=False, encoding='utf-8-sig')
        return csv_file

    @staticmethod
    def _harmonics_fig(k, wave, unit, runs, f0s, f0_paths, window_text):
        """Harmonic bar plot of waveform k, every sweep point side by side (None if the waveform has no fundamental)."""
        fig                 = go.Figure()
        for r in runs:
            orders, H       = r['harmonics']
            if not np.isnan(H[k]).all():
                fig.add_trace(go.Bar(x=orders, y=H[k], name=r['name'], marker_color=r['color']))
        if not fig.data:
            return None
        f0_text             = " / ".join(PPlots.format_hz(f) for f in sorted({run_f0s[k] for run_f0s in f0s if run_f0s[k]}))
        fig.update_layout(title=f"{wave} - Harmonics (f0: {'.'.join(map(str, f0_paths[k]))} = {f0_text}, {window_text})",
                          xaxis_title="Harmonic order", yaxis_title=f"Amplitude {unit}", barmode='group', bargap=0.15)
        fig.update_xaxes(tickmode='linear', tick0=1, dtick=1)
        return PPlots._style(fig)

    @staticmethod
    def _metrics_table(runs, waveforms, units, window_text):
        """Table of the calculated results: one row per waveform and sweep point, one column per type of PMath.METRICS."""
        fmt                 = lambda v: f"{v:.6g}"
        rows                = [(wave, unit, r['name'], [fmt(r['metrics'][kind][k]) for kind in PMath.METRICS])
                               for k, (wave, unit) in enumerate(zip(waveforms, units)) for r in runs]
        columns             = {"WAVEFORM": [w for w, _, _, _ in rows], "UNIT": [u for _, u, _, _ in rows],
                               "SWEEP POINT": [p for _, _, p, _ in rows]}
        columns.update({kind.upper(): [v[j] for _, _, _, v in rows] for j, kind in enumerate(PMath.METRICS)})
        fig                 = PPlots._params_table(columns)
        fig.update_layout(title=f"Calculated results ({window_text})", height=min(1200, 26 * len(rows) + 160))
        return fig

    @staticmethod
    def gen_sweep_plots(points, waveforms, units=None, f0_path=None, f0_overrides=None, model_name='', img_path=None, params_file=None, OPEN=False):
        """Reports of a whole sweep. Every time-series CSV is loaded once, then:
            - html/Html_<run>.html : for each waveform its time-domain figure then its harmonic bar plot (every sweep
                                     point overlaid, x axis = harmonic order, f0 in the title), then the table of the
                                     calculated results (RMS, Average, PeakToPeak, Max, Min, Peak per waveform and point)
                                     and the parameter table;
            - mat/<type>_<run>.csv : one matrix per scalar metric of PMath.METRICS (rows: sweep points, columns: waveforms);
            - mat/FFT_<run>.csv    : harmonic amplitudes per sweep point and waveform.
        Metrics and harmonics use the last ANALYSIS_CYCLES whole cycles of the lowest fundamental of the run.

        *Args:
            points      : list of (label, ModelVars) as built by plecs.Sweep.build_points.
            waveforms   : the result CSV columns after time, in order: {name: unit}, or a list of names.
            units       : unit of each waveform; None = the units of the waveforms dict, or guessed from the names (units_from_names).
            f0_path     : key path of the fundamental frequency in ModelVars, e.g. ('Grid', 'f'); None = no harmonics,
                          metrics over the whole saved window.
            f0_overrides: {waveform name keyword: key path} for waveforms with their own fundamental, e.g. {'HS1': ('CTRL', 'fsw')}.
            model_name  : used in the page title.
            img_path    : image shown on top of the report (optional).
            params_file : file whose '#?' comments give the unit/comment columns of the parameter table (optional).
        Returns the list of calculated CSV files.
        """
        if isinstance(waveforms, dict):                                                    # {name: unit}
            units           = units or list(waveforms.values())
            waveforms       = list(waveforms)
        n                   = len(waveforms)
        units               = units or PPlots.units_from_names(waveforms)
        labels_all          = [label for label, _ in points]
        varied              = [k for k in labels_all[0] if len({str(l[k]) for l in labels_all}) > 1] or list(labels_all[0])
        colors              = pc.qualitative.Dark24
        f0_paths            = PPlots.waveform_f0_paths(waveforms, f0_path, f0_overrides)
        f0s                 = [[Sweep.get_nested(mv, p) if p else None for p in f0_paths] for _, mv in points]   # [point][waveform]
        runs, labels        = [], []
        for i, ((label, mv), run_f0s) in enumerate(zip(points, f0s)):
            res             = PPlots._load_run(mv[OUTPUT_KEY]['ToFile_path'], n, run_f0s)
            if res is not None:
                res.update(name=PPlots._run_name(label, mv, varied), color=colors[i % len(colors)],
                           sim_idx=mv[OUTPUT_KEY]['sim_idx'], index=i)
                runs.append(res)
                labels.append(label)
        if not runs:
            print("WARNING: no result CSV found, HTML report not written.")
            return []
        out                 = points[0][1][OUTPUT_KEY]
        f_base              = min((f for row in f0s for f in row if f), default=None)
        window              = runs[0]['window']
        window_text         = (f"last {window:.4g} s = {window * f_base:.0f} cycles of {PPlots.format_hz(f_base)}"
                               if f_base else f"whole saved window, {window:.4g} s")
        #? figures: time domain then harmonics, waveform after waveform
        figures             = []
        for k, (wave, unit) in enumerate(zip(waveforms, units)):
            fig             = go.Figure()
            for r in runs:
                fig.add_trace(go.Scatter(x=r['t'], y=r['Y'][:, k], mode='lines', name=r['name'], line=dict(color=r['color'], width=1)))
            fig.update_layout(title=wave, xaxis_title="Time [s]", yaxis_title=unit)
            figures.append(PPlots._style(fig))
            fig_h           = PPlots._harmonics_fig(k, wave, unit, runs, f0s, f0_paths, window_text)
            if fig_h is not None:
                figures.append(fig_h)
        #? calculated results table
        figures.append(PPlots._metrics_table(runs, waveforms, units, window_text))
        #? parameter table
        shown               = lambda mv: {k: (v if k != OUTPUT_KEY else {kk: vv for kk, vv in v.items() if kk not in OUTPUT_FIELDS})
                                          for k, v in mv.items()}
        params              = [PPlots.flatten_dict(shown(mv)) for _, mv in points]
        names               = list(params[0].keys())
        fmt                 = lambda v: f"{v:g}" if isinstance(v, float) else str(v)
        values              = [" / ".join(dict.fromkeys(fmt(p[name]) for p in params)) for name in names]   # swept: 'a / b / c'
        columns             = {"PARAMETERS": names}
        if params_file:
            notes           = PPlots.extract_comments(params_file)
            found           = [PPlots.find_note(notes, name) for name in names]
            columns.update({"UNITS": [u for u, _ in found], "COMMENTS": [c for _, c in found]})
        columns["VALUE"]    = values
        table_fig           = PPlots._params_table(columns)
        table_fig.update_layout(height=900)
        title               = f"{model_name}_{out['utc_numeric']}_SWEEP_MOHAMED_GUENI"
        PPlots.write_html(out['output_html'], title, figures + [table_fig], PPlots.png_to_hex_base64(img_path), OPEN)
        #? calculated results: one matrix CSV per type
        csv_files           = [PPlots._write_metric(kind, runs, waveforms, units, labels, out) for kind in PMath.METRICS]
        if f0_path or f0_overrides:
            csv_files.append(PPlots._write_fft(runs, waveforms, units, labels, f0s, out))
        return csv_files

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? AC analysis report
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def plot_ac_analysis_sweep(results_list, html_file, analysis_opts, title='AC Sweep Analysis', OPEN=False):
        """Plot magnitude (Gr) and phase (Gi) of each AC sweep result in results_list on log-frequency axes,
        with the analysis options as a table."""
        fig                 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.20,
                                            subplot_titles=('Magnitude (Gr)', 'Phase (Gi)'))
        for idx, data in enumerate(results_list, start=1):
            fig.add_trace(go.Scatter(x=data['F'], y=data['Gr'][0], mode='lines', name=f'Magnitude (Gr) Iteration {idx}'), row=1, col=1)
            fig.add_trace(go.Scatter(x=data['F'], y=data['Gi'][0], mode='lines', name=f'Phase (Gi) Iteration {idx}'), row=2, col=1)
        fig.update_layout(
            autosize        = True,
            title_text      = title,
            yaxis_title     = 'Magnitude (dB)',
            yaxis2_title    = 'Phase (deg)',
            margin          = dict(l=50, r=50, t=100, b=50),
            height          = 600,
        )
        fig.update_xaxes(type='log', title_text='Frequency (Hz)')
        params              = PPlots.flatten_dict(analysis_opts)
        table_fig           = PPlots._params_table({"PARAMETERS": list(params.keys()), "VALUES": list(params.values())})
        PPlots.write_html(html_file, f"{title}_MOHAMED_GUENI", [fig, table_fig], OPEN=OPEN)
#?----------------------------------------------------------------------------------------------------------------------------------------
class PLog:
    """Parameter logs. ModelVars are nested dicts; a parameter is written as [key][subkey]... = value."""

    WIDTH               = 99                                                           # length of the section separators

    @staticmethod
    def flat(d):
        """Yield (key path tuple, value) for every leaf of a nested dict."""
        return ((p, Sweep.get_nested(d, p)) for p in Sweep.leaf_paths(d))

    @staticmethod
    def _differs(a, b):
        """a != b, with a relative tolerance on numbers so rounding noise of derived parameters is not a change."""
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return not math.isclose(a, b, rel_tol=1e-9)
        return a != b

    @staticmethod
    def _key(keys):
        return "[" + "][".join(str(k) for k in keys) + "]"

    @staticmethod
    def _fmt(value):
        return f"{value:g}" if isinstance(value, (int, float)) and not isinstance(value, bool) else str(value)

    @staticmethod
    def params_lines(params):
        """All parameters of a nested dict (output files excluded), one '[a][b] = value' line each."""
        return ["{:<40}= {}".format(PLog._key(k), v) for k, v in PLog.flat(params) if k[0] != OUTPUT_KEY]

    @staticmethod
    def write_sweep_log(points, base, run_id):
        """One log file per sweep: the base parameters once, then one section per iteration with only the parameters
        that differ from the base (swept values and the derived parameters they change).
        points: list of (label, ModelVars) as built by plecs.Sweep.build_points; the file is ModelVars[OUTPUT_KEY]['logfile']."""
        log_file            = points[0][1][OUTPUT_KEY]['logfile']
        base_flat           = dict(PLog.flat(base))
        lines               = [f"Sweep {run_id}: {len(points)} iterations", "=" * PLog.WIDTH, "BASE PARAMETERS", "-" * PLog.WIDTH]
        lines              += PLog.params_lines(base)
        for label, mv in points:
            swept           = ", ".join(f"{k}={PLog._fmt(v)}" for k, v in label.items())
            lines          += ["=" * PLog.WIDTH, f"ITERATION {mv[OUTPUT_KEY]['sim_idx']}/{len(points)} : {swept}",
                               f"results : {mv[OUTPUT_KEY]['ToFile_path']}", "-" * PLog.WIDTH]
            lines          += ["{:<40}= {:<24} (base: {})".format(PLog._key(k), str(v), base_flat.get(k))
                               for k, v in PLog.flat(mv) if k[0] != OUTPUT_KEY and PLog._differs(v, base_flat.get(k))]
        with open(log_file, 'w') as f:
            f.write("\n".join(lines) + "\n")
        return log_file
#?----------------------------------------------------------------------------------------------------------------------------------------
