#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?              __      __
#?         ____/ /_____/ /
#?        / __/ __/ __  /
#?       (__  ) /_/ /_/ /
#?      /____/\__/\__,_/
#?
#?
#? Name:        standalone.py
#? Purpose:     standalone copy of a PLECS model (<model>_std.plecs) that runs from PLECS alone:
#?              - every library link broken (breaklink.py);
#?              - every parameter set: the ModelVars written as actual values into the initialization commands.
#?              Standard library only; needs breaklink.py next to it (copy both files to another project).
#?                  path = Standalone.write('model.plecs', ModelVars, ['lib_dir'])
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     11/04/2026
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import math
from   pathlib              import  Path

try:
    from   .breaklink       import  LinkBreaker                              # inside a package (from lib.standalone import ...)
except ImportError:
    from   breaklink        import  LinkBreaker                              # run as a script, breaklink.py next to it

NL                                  = chr(10)
#?----------------------------------------------------------------------------------------------------------------------------------------
class Standalone:
    """Standalone copy of a PLECS model: library links broken, ModelVars written into the initialization commands.

        path = Standalone.write(model_path, modelvars=None, lib_dir=None, out=None, builtins=True)

    model_path  .plecs model (text format)
    modelvars   {name: value} as given to plecs.simulate (nested dicts = structs; lists = vectors / matrices; str)
    lib_dir     folder(s) of the user libraries (the model folder is always searched)
    out         output file (default <model>_std.plecs next to the model, so relative paths such as thermal files still work)
    builtins    True: also break the links to the PLECS built-in library (Components/...)
    """

    SUFFIX                          = '_std'

    @classmethod
    def write(cls, model_path, modelvars=None, lib_dir=None, out=None, builtins=True):
        lb                          = LinkBreaker(model_path, lib_dir, builtins)
        out                         = Path(out) if out else lb.model.with_name(lb.model.stem + cls.SUFFIX + lb.model.suffix)
        if modelvars:
            init                    = (lb.plecs.value('InitializationCommands') or '').replace('\\n', NL).strip()
            code                    = NL.join(['% ---- parameters written by standalone.py (ModelVars as actual values) ----',
                                               *cls.matlab(modelvars), ''])
            lb.plecs.set('InitializationCommands', cls.encode('InitializationCommands', (init + NL + NL if init else '') + code))
            print(f"standalone: {len(modelvars)} ModelVars structs set as values")
        return lb.save(out, tag='standalone')

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? ModelVars -> MATLAB / PLECS initialization commands
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def encode(key, text):
        """Raw lines of 'key "text"': escaped, one string piece per line of text (long lines cut in pieces of 70)."""
        esc                         = text.replace('\\', '\\\\').replace('"', '\\"').replace('\t', '\\t').split(NL)
        pieces                      = []
        for k, line in enumerate(esc):
            line                   += '\\n' if k < len(esc) - 1 else ''
            while len(line) > 70:
                cut                 = 70
                while line[cut - 1] == '\\' and (len(line[:cut]) - len(line[:cut].rstrip('\\'))) % 2:   # do not split an escape
                    cut            -= 1
                pieces.append(line[:cut]); line = line[cut:]
            if line or not pieces:
                pieces.append(line)
        return [f'{key} "{pieces[0]}"'] + [f'"{p}"' for p in pieces[1:]]

    @classmethod
    def value(cls, v):
        if isinstance(v, bool):
            return 'true' if v else 'false'
        if isinstance(v, (int, float)):
            if isinstance(v, float) and math.isnan(v):
                return 'NaN'
            if isinstance(v, float) and math.isinf(v):
                return 'Inf' if v > 0 else '-Inf'
            return repr(v)
        if v is None:
            return '[]'
        if isinstance(v, str):
            return "'" + v.replace("'", "''") + "'"
        if hasattr(v, 'tolist'):                                                # numpy arrays / scalars
            return cls.value(v.tolist())
        if isinstance(v, (list, tuple)):
            if not v:
                return '[]'
            if all(isinstance(x, (list, tuple)) for x in v):                   # matrix: one row per inner list
                return '[' + '; '.join(' '.join(cls.value(x) for x in row) for row in v) + ']'
            if all(isinstance(x, str) for x in v):
                return '{' + ', '.join(cls.value(x) for x in v) + '}'
            return '[' + ' '.join(cls.value(x) for x in v) + ']'
        raise TypeError(f"no MATLAB form for {type(v).__name__}: {v!r}"[:120])

    @classmethod
    def matlab(cls, d, prefix=''):
        """'Grid.f = 50;' lines of the nested dict d (lists of dicts: struct arrays S(k).x)."""
        lines                       = []
        for key, v in d.items():
            name                    = f"{prefix}{key}"
            if isinstance(v, dict):
                lines              += cls.matlab(v, name + '.') if v else [f"{name} = struct();"]
            elif isinstance(v, (list, tuple)) and v and all(isinstance(x, dict) for x in v):
                for k, x in enumerate(v, 1):
                    lines          += cls.matlab(x, f"{name}({k}).")
            else:
                lines.append(f"{name} = {cls.value(v)};")
        return lines
#?----------------------------------------------------------------------------------------------------------------------------------------
#? Run this file (VS Code: Run Python File, the play button) to write the standalone copy. Set the paths here.
#?----------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    MODEL                           = r'D:\WORKSPACE\0049_SP_BTP_PFC_1KW\model\PFC.plecs'      # model to copy
    LIB_DIRS                        = [r'D:\WORKSPACE\0000_libraries\Plecs']                   # folders of your libraries ([] = none)
    VARS                            = None                                                   # ModelVars: dict, path of a JSON file, or None (values kept as in the model)
    OUT                             = None                                                   # None = <model>_std.plecs next to the model
    BUILTINS                        = True                                                   # also break the links to the PLECS built-in library

    import json
    if isinstance(VARS, str):
        with open(VARS, encoding='utf-8') as f:
            VARS                    = json.load(f)
        VARS                        = VARS.get('ModelVars', VARS) if isinstance(VARS, dict) else {}
    Standalone.write(MODEL, VARS, LIB_DIRS, OUT, BUILTINS)
