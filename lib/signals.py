#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?                _                   __
#?          _____(_)___ _____  ____ _/ /____
#?         / ___/ / __ `/ __ \/ __ `/ / ___/
#?        (__  ) / /_/ / / / / /_/ / (__  )
#?       /____/_/\__, /_/ /_/\__,_/_/____/
#?              /____/
#?
#?
#? Name:        signals.py
#? Purpose:     names (and units) of the signals a PLECS To File writes, read from the model file and its libraries.
#?              Standalone (standard library only): copy the file to any project.
#?                  names = SignalNames.from_model('model.plecs')                 # from the model alone
#?                  names = SignalNames.read('result.csv', 'model.plecs')        # columns of a result CSV
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     10/29/2026
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import ast
import base64
import glob
import math
import os
import re
import warnings
from   pathlib              import  Path

NL                                  = chr(10)
MARK                                = ('\0', '', '', '')                        # trace reached the input port of the block being evaluated
#?----------------------------------------------------------------------------------------------------------------------------------------
class _Env:
    """Variables of one block level: mask parameters (name -> expression, evaluated in the level above) and values set
    by initialization code (model InitializationCommands, block MaskInit). At the top: ModelVars, then the model's
    initialization commands. Expressions use the MATLAB-like syntax of PLECS parameters ('[nV nI]', 'S.n', 'a(2)')."""

    OPS                             = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b, ast.Mult: lambda a, b: a * b,
                                       ast.Div: lambda a, b: a / b, ast.Pow: lambda a, b: a ** b}
    CMP                             = {ast.Eq: lambda a, b: a == b, ast.NotEq: lambda a, b: a != b, ast.Lt: lambda a, b: a < b,
                                       ast.LtE: lambda a, b: a <= b, ast.Gt: lambda a, b: a > b, ast.GtE: lambda a, b: a >= b}
    FUNCS                           = {'length': lambda v: len(v) if isinstance(v, (list, tuple, str)) else 1,
                                       'numel': lambda v: len(v) if isinstance(v, (list, tuple)) else 1,
                                       'sum': lambda v: sum(v) if isinstance(v, (list, tuple)) else v,
                                       'max': lambda *v: max(v[0]) if len(v) == 1 and isinstance(v[0], (list, tuple)) else max(v),
                                       'min': lambda *v: min(v[0]) if len(v) == 1 and isinstance(v[0], (list, tuple)) else min(v),
                                       'double': float, 'int32': int, 'round': round, 'floor': math.floor, 'ceil': math.ceil,
                                       'abs': abs, 'isfield': lambda s, f: isinstance(s, dict) and f in s}

    def __init__(self, variables, parent=None, modelvars=None):
        self.vars, self.parent      = variables, parent
        self.values                 = {}                                        # set by initialization code of this level
        self.modelvars              = modelvars if parent is None else parent.modelvars

    def lookup(self, name):
        if self.parent is None:                                                 # top: ModelVars override the init commands
            return self.modelvars[name] if name in self.modelvars else self.values.get(name)
        if name in self.values:
            return self.values[name]
        if name in self.vars:
            return self.parent.eval(self.vars[name])
        return self.parent.lookup(name)

    @staticmethod
    def matlab(expr):
        """MATLAB-like expression -> Python syntax: [a b; c] -> [a, b, c], ~= -> !=, && / || / ~, ^ -> **."""
        s                           = str(expr).strip()
        s                           = s.replace('~=', '!=').replace('&&', ' and ').replace('||', ' or ').replace('^', '**')
        s                           = re.sub(r'~(?!=)', ' not ', s)
        out, depth                  = [], 0
        for k, ch in enumerate(s):                                              # inside [ ]: spaces / ';' separate elements
            depth                  += ch == '['
            depth                  -= ch == ']'
            if depth and ch == ';':
                ch                  = ','
            elif depth and ch in ' \t' and out and re.match(r"[\w)\]'.]", out[-1]) and \
                    re.match(r"[\w(\['.]|-\S", s[k + 1:k + 3].lstrip()) and not re.match(r'\s*[-+*/,]\s', s[k:k + 3]):
                ch                  = ','
            out.append(ch)
        return re.sub(r',\s*,+', ',', ''.join(out))

    def eval(self, expr):
        """Value of a parameter expression ('1', 'PFC.SW.Config', '[nV nI]', 'n+1'); None if it cannot be evaluated."""
        if expr is None or str(expr).strip() == '':
            return None
        try:
            return self._node(ast.parse(self.matlab(expr), mode='eval').body)
        except Exception:
            return None

    def _node(self, n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.Name):
            return {'true': True, 'false': False, 'pi': math.pi}.get(n.id, None) if n.id in ('true', 'false', 'pi') else self.lookup(n.id)
        if isinstance(n, ast.Attribute):
            v                       = self._node(n.value)
            return v.get(n.attr) if isinstance(v, dict) else getattr(v, n.attr)
        if isinstance(n, (ast.List, ast.Tuple)):
            out                     = []
            for e in n.elts:                                                    # MATLAB [a b] concatenates vectors
                v                   = self._node(e)
                out                += list(v) if isinstance(v, (list, tuple)) else [v]
            return out
        if isinstance(n, ast.Call):
            args                    = [self._node(a) for a in n.args]
            if isinstance(n.func, ast.Name) and n.func.id in self.FUNCS and self.lookup(n.func.id) is None:
                return self.FUNCS[n.func.id](*args)
            v                       = self._node(n.func)                        # a(2), S.n(2): 1-based indexing
            return v[int(args[0]) - 1] if isinstance(v, (list, tuple)) else v
        if isinstance(n, ast.BinOp) and type(n.op) in self.OPS:
            return self.OPS[type(n.op)](self._node(n.left), self._node(n.right))
        if isinstance(n, ast.UnaryOp):
            v                       = self._node(n.operand)
            return -v if isinstance(n.op, ast.USub) else (not v) if isinstance(n.op, ast.Not) else v
        if isinstance(n, ast.Compare) and len(n.ops) == 1 and type(n.ops[0]) in self.CMP:
            return self.CMP[type(n.ops[0])](self._node(n.left), self._node(n.comparators[0]))
        if isinstance(n, ast.BoolOp):
            vals                    = [self._node(v) for v in n.values]
            return all(vals) if isinstance(n.op, ast.And) else any(vals)
        if isinstance(n, ast.IfExp):
            return self._node(n.body) if self._node(n.test) else self._node(n.orelse)
        raise ValueError(n)

    def run(self, code):
        """Assignments of initialization code into self.values ('x = 2;', 'S.n = [1 2];', if/elseif/else/end blocks).
        Statements it cannot evaluate are skipped; if-blocks with an unknown condition are skipped."""
        if not code:
            return self
        lines                       = []
        for raw in str(code).replace('\\n', '\n').splitlines():
            line                    = re.sub(r"%.*$", '', raw).strip()            # MATLAB comment
            lines                  += [p.strip() for p in re.split(r';(?![^\[]*\])', line) if p.strip()]
        stack                       = []                                        # if-blocks: [taken?, any branch taken?, parent active?]
        for st in lines:
            active                  = all(s[0] for s in stack)
            m                       = re.match(r'^(if|elseif)\s+(.+)$', st)
            if m and m.group(1) == 'if':
                cond                = bool(self.eval(m.group(2))) if active else False
                stack.append([cond, cond])
            elif m:                                                             # elseif
                if stack:
                    parent_active   = all(s[0] for s in stack[:-1])
                    cond            = parent_active and not stack[-1][1] and bool(self.eval(m.group(2)))
                    stack[-1]       = [cond, stack[-1][1] or cond]
            elif st == 'else':
                if stack:
                    parent_active   = all(s[0] for s in stack[:-1])
                    stack[-1]       = [parent_active and not stack[-1][1], True]
            elif st == 'end':
                stack and stack.pop()
            elif active:
                a                   = re.match(r'^([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*=(?!=)\s*(.+)$', st)
                value               = self.eval(a.group(2)) if a else None
                if value is not None:
                    keys            = a.group(1).split('.')
                    d               = self.values
                    for k in keys[:-1]:
                        d           = d.setdefault(k, {}) if isinstance(d.get(k, {}), dict) else d
                    d[keys[-1]]     = value
        return self
#?----------------------------------------------------------------------------------------------------------------------------------------
class _Scope:
    """One schematic level while walking the model: the schematic, the block that owns it, its parameters, the level above."""

    def __init__(self, sch, owner=None, env=None, parent=None, root=False):
        self.sch, self.owner, self.env, self.parent, self.root = sch, owner, env, parent, root

    def path(self):
        names, s                    = [], self
        while s and s.owner is not None:
            names.append(SignalNames.prop(s.owner, 'Name')); s = s.parent
        return '/'.join(reversed(names)) or '(top level)'
#?----------------------------------------------------------------------------------------------------------------------------------------
class SignalNames:
    """Names of the signals a To File block writes, from the model file and the libraries it references.

    The To File input is traced back to its sources: through Mux (element order), subsystem and library-block ports
    at any depth, configurable subsystems (active configuration from ModelVars through the mask parameters),
    Goto/From and hold blocks, to the probes. A probe gives 'component signal' per probed signal; a probed library
    block with a mask probe names each element of the vector (e.g. 'PFC SW Voltages HS1'). A block with one input
    (RMS, gain, filter, a subsystem computed from its input) keeps the names of its input, with its name in front;
    other blocks give their own name. Libraries are searched in lib_dir(s), the model's folder and the PLECS
    installation (components.plecs). With a result CSV, the header PLECS writes is used where it holds real names.
    Units are guessed from the probe and signal names (UNIT_KEYWORDS: keyword -> unit, first match wins)."""

    UNIT_KEYWORDS                   = {
                                        'gate'          : '[ / ]',
                                        'temperature'   : '[ °C ]',
                                        'temp'          : '[ °C ]',
                                        'voltage'       : '[ V ]',
                                        'current'       : '[ A ]',
                                        'loss'          : '[ W ]',
                                        'power'         : '[ W ]',
                                      }
    GENERIC                         = re.compile(r'^(<undefined>|ToFile[ _]?In[ _]?\d+|In[ _]?\d*|Signal[ _]?\d*|)$', re.I)   # names PLECS gives unnamed signals
    PASS_THROUGH                    = {'ZeroOrderHold', 'Memory', 'Delay', 'DataTypeConversion', 'SignalSwitch'}   # input 1 -> output, same names
    PLECS_DIRS                      = ['$PLECS_DIR', '~/Documents/Plexim/PLECS*', '~/AppData/Local/Plexim/PLECS*', '~/AppData/Roaming/Plexim/PLECS*',
                                       'C:/Program Files/Plexim/PLECS*', 'C:/Program Files (x86)/Plexim/PLECS*', 'C:/ProgramData/Plexim/PLECS*',
                                       'C:/Plexim/PLECS*', '/Applications/PLECS*', '~/Plexim/PLECS*', '/opt/plexim/plecs*']   # PLECS installations

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? One-line entry points
    #?------------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def from_model(cls, model_path, lib_dir=None, modelvars=None, labels=None, units=False, tofile=None, unit_keywords=None):
        """Names of the signals written by the model's To File block (named tofile when there are several), in order;
        (names, units) with units=True.
        lib_dir  : folder (or list of folders) of the libraries the model references (the model's folder is always searched)
        modelvars: ModelVars dict, to pick the active configurations ('PFC.Config'); without it every configuration is tried
        labels   : {'component:probe signal': [element names]} for vectors that cannot be resolved"""
        sn                          = cls(model_path, lib_dir, modelvars, labels)
        entries                     = sn.traced(tofile=tofile) or []
        return sn._out([sn._name(c, s, l) for c, s, l, _ in entries], [f"{s} {h}".lower() for _, s, _, h in entries], units, unit_keywords)

    @classmethod
    def read(cls, csv_file, model_path, lib_dir=None, modelvars=None, labels=None, units=False, tofile=None, unit_keywords=None):
        """Names of the columns of csv_file after the time column, in order; (names, units) with units=True.
        Arguments as from_model()."""
        sn                          = cls(model_path, lib_dir, modelvars, labels)
        names, hints                = sn.columns(csv_file, tofile)
        return sn._out(names, hints, units, unit_keywords)

    @classmethod
    def units_from_names(cls, names, unit_keywords=None):
        """Unit of each name guessed from its keywords ('[ / ]' if none matches)."""
        keywords                    = unit_keywords or cls.UNIT_KEYWORDS
        return [next((u for kw, u in keywords.items() if kw in n.lower()), '[ / ]') for n in names]

    def _out(self, names, hints, units, unit_keywords):
        if not units:
            return names
        keywords                    = unit_keywords or self.UNIT_KEYWORDS
        return names, [next((u for kw, u in keywords.items() if kw in h), '[ / ]') for h in hints]

    def __init__(self, model_path, lib_dir=None, modelvars=None, labels=None):
        self.root                   = self.parse(model_path)
        self.modelvars              = modelvars or {}
        self.labels                 = labels or {}
        dirs                        = [lib_dir] if isinstance(lib_dir, (str, Path)) else list(lib_dir or [])
        self.lib_files              = {}                                        # library name (lower case) -> file
        for d in [Path(model_path).parent] + [Path(d) for d in dirs]:
            for f in sorted(d.glob('*.plecs')) if d.is_dir() else []:
                self.lib_files.setdefault(f.stem.lower(), f)
        self._trees, self._blocks   = {}, {}
        self.steps                  = []                                        # trace log (report)
        top                         = next((c for c in self.root['children'] if c['tag'] == 'Plecs'), self.root)
        env                         = _Env({}, None, self.modelvars).run(self.prop(top, 'InitializationCommands'))
        self.top                    = _Scope(next(iter(self.kids(top, 'Schematic')), top), env=env, root=True)

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? .plecs files: tree of 'Tag { key value ... }' blocks
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parse(path):
        """{'tag', 'props' [(key, value) in order], 'children'} of a .plecs file (text format of PLECS 4.x and later).
        Strings split over several lines are joined, the outer quotes removed (inner \\" kept as ")."""
        data                        = Path(path).read_bytes()
        head                        = data[:200].lstrip(b'\xef\xbb\xbf \t\r\n')
        if head.startswith(b'PK') or b'\x00' in data[:4096]:
            raise ValueError(f"{path}: binary or zipped file, not a PLECS text model (save it as a plain .plecs model)")
        if head.startswith(b'<'):
            raise ValueError(f"{path}: XML file, not a PLECS text model")
        try:
            text                    = data.decode('utf-8-sig')
        except UnicodeDecodeError:
            text                    = data.decode('latin-1')
        if not re.match(r'\s*\w+\s*\{', text):
            raise ValueError(f"{path}: does not start like a PLECS model ('Plecs {{'): {text[:60]!r}")
        root                        = {'tag': None, 'props': [], 'children': []}
        stack, pending, raw         = [root], None, None                       # pending: 'Tag' line waiting for its '{'
        def unquote(v):
            m                       = re.match(r'^base64\s+"(.*)"$', v, re.S)   # non-ASCII text: base64 "Q3VzdG9t..."
            if m:
                try:
                    return base64.b64decode(m.group(1)).decode('utf-8', errors='replace')
                except (ValueError, TypeError):
                    return v
            return v[1:-1].replace('\\"', '"') if len(v) >= 2 and v[0] == '"' and v[-1] == '"' else v
        def close_prop():
            nonlocal raw
            if raw:
                node, key, value    = raw
                node['props'].append((key, unquote(value)))
            raw                     = None
        def open_block(tag):
            node                    = {'tag': tag, 'props': [], 'children': []}
            stack[-1]['children'].append(node)
            stack.append(node)
        for line in text.splitlines():
            s                       = line.strip()
            if not s:
                continue
            if raw and s.startswith('"'):                                       # continuation of a string split over lines
                node, key, value    = raw
                raw                 = (node, key, value[:-1] + s[1:] if value.endswith('"') else value + s)
                continue
            close_prop()
            if pending is not None:
                if s == '{':
                    open_block(pending); pending = None; continue
                stack[-1]['props'].append((pending, '')); pending = None
            m                       = re.match(r'^([A-Za-z_]\w*)\s*\{$', s)
            if m:
                open_block(m.group(1))
            elif s.startswith('}'):
                if len(stack) > 1:
                    stack.pop()
            elif re.match(r'^[A-Za-z_]\w*$', s):
                pending             = s                                         # 'Tag' with its '{' on the next line, or a bare key
            else:
                key, _, value       = s.replace('\t', ' ').partition(' ')       # key, any spaces / tabs, value
                raw                 = (stack[-1], key, value.strip())
        close_prop()
        return root

    @staticmethod
    def _strings(value):
        """Strings of a list value: '{"VL1", "IL1"}' -> ['VL1', 'IL1']."""
        return [x.replace('\\"', '"') for x in re.findall(r'"((?:[^"\\]|\\.)*)"', value or '')]

    @staticmethod
    def prop(node, key):
        return next((v for k, v in node['props'] if k == key), None) if node else None

    @staticmethod
    def kids(node, tag):
        return [c for c in node['children'] if c['tag'] == tag] if node else []

    @staticmethod
    def param(comp, variable):
        return next((SignalNames.prop(p, 'Value') for p in SignalNames.kids(comp, 'Parameter')
                     if SignalNames.prop(p, 'Variable') == variable), None)

    @staticmethod
    def component(schematic, name):
        return next((c for c in SignalNames.kids(schematic, 'Component') if SignalNames.prop(c, 'Name') == name), None)

    @staticmethod
    def find(node, name):
        """First Component named name anywhere below node."""
        for child in node['children']:
            if child['tag'] == 'Component' and SignalNames.prop(child, 'Name') == name:
                return child
            found                   = SignalNames.find(child, name)
            if found:
                return found
        return None

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Libraries: the block behind a Reference ('Power/EVSE\/GRID', 'Components/Control/Filters/RMS Value')
    #?------------------------------------------------------------------------------------------------------------------------------------
    def _library_file(self, name):
        f                           = self.lib_files.get(name.lower())
        if f is None and name == 'Components' and 'components' not in self.lib_files:   # PLECS built-in library, newest installation
            hits                    = []
            for d in self.PLECS_DIRS:
                d                   = os.path.expandvars(os.path.expanduser(d))
                for depth in ('', '*', '*/*', '*/*/*'):                         # components.plecs may sit in a subfolder
                    hits           += glob.glob(os.path.join(d, depth, 'components.plecs'))
            f                       = self.lib_files['components'] = Path(max(hits, key=os.path.getmtime)) if hits else None
        return f

    def _ref_block(self, comp):
        src                         = self.prop(comp, 'SrcComponent')
        if src not in self._blocks:
            parts                   = [p.replace('\\/', '/') for p in re.split(r'(?<!\\)/', (src or '').replace('\\\\', '\\'))]
            f                       = self._library_file(parts[0]) if len(parts) > 1 else None
            blk                     = None
            if f is not None:
                if f not in self._trees:
                    self._trees[f]  = self.parse(f)
                tree                = self._trees[f]
                node                = next((c for c in tree['children'] if c['tag'] == 'Plecs'), tree)
                sch                 = next(iter(self.kids(node, 'Schematic')), node)
                for k, part in enumerate(parts[1:]):                           # walk the library folders
                    blk             = self.component(sch, part)
                    if blk is None or k == len(parts) - 2:
                        break
                    sch             = next(iter(self.kids(blk, 'Schematic')), None)
                    if sch is None:
                        blk         = None; break
                blk                 = blk or self.find(tree, parts[-1])
            self._blocks[src]       = blk
        return self._blocks[src]

    def content(self, comp):
        """Component holding the content of comp: the library block of a Reference, else comp itself."""
        return self._ref_block(comp) if self.prop(comp, 'Type') == 'Reference' else comp

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Levels: schematics of a block (active configuration first) and the scope inside it
    #?------------------------------------------------------------------------------------------------------------------------------------
    def _configs(self, comp, env):
        """(configuration names, schematics, active index or None) of comp."""
        blk                         = self.content(comp)
        configs                     = next(iter(self.kids(blk, 'Configurations')), None)
        if configs is None:
            return [None], self.kids(blk, 'Schematic')[:1], 0 if self.kids(blk, 'Schematic') else None
        names                       = [v for k, v in configs['props'] if k == 'Name']
        value                       = env.eval(self.param(comp, 'Configuration'))
        if isinstance(value, str):                                              # configuration given by its name ('On')
            low                     = [str(n).lower() for n in names]
            idx                     = low.index(value.lower()) if value.lower() in low else None
        else:
            try:
                idx                 = int(value) - 1 if 1 <= int(value) <= len(names) else None
            except (TypeError, ValueError):
                idx                 = None
        return names, self.kids(configs, 'Schematic'), idx

    def schematics(self, comp, scope, config_name=None):
        """[(configuration name, child scope)] of comp in scope: the named configuration, or the active one
        (every configuration when the active one is unknown)."""
        names, schs, idx            = self._configs(comp, scope.env)
        pairs                       = list(zip(names, schs))
        if config_name is not None:
            pairs                   = [p for p in pairs if p[0] == config_name]
        elif idx is not None:
            pairs                   = [pairs[idx]]
        blk                         = self.content(comp)
        variables                   = {self.prop(p, 'Variable'): self.prop(p, 'Value') for p in self.kids(blk, 'Parameter')}
        variables.update({self.prop(p, 'Variable'): self.prop(p, 'Value') for p in self.kids(comp, 'Parameter')})
        env                         = _Env(variables, scope.env).run(self.prop(blk, 'MaskInit'))
        is_root                     = self.prop(comp, 'Type') == 'Reference' or bool(self.kids(blk, 'MaskProbe'))
        return [(n, _Scope(s, comp, env, scope, root=is_root)) for n, s in pairs]

    def walk(self, scope=None):
        """(scope, component) for every component of the model, inside subsystems and library blocks."""
        scope                       = scope or self.top
        for c in self.kids(scope.sch, 'Component'):
            yield scope, c
            for _, inner in self.schematics(c, scope):
                yield from self.walk(inner)

    def _by_path(self, scope, path, name):
        """(scope, component) of the probe target `name` at Path 'A/Config/B', relative to the enclosing library block
        or masked subsystem (innermost first) or to the top level."""
        parts                       = [p for p in re.split(r'(?<!\\)/', path or '') if p]
        bases                       = []
        s                           = scope
        while s:
            if s.root:
                bases.append(s)
            s                       = s.parent
        for base in bases:
            for skip in (0, 1):                                                 # a path may start with the base's configuration
                cur, ok, i          = base, True, skip
                while i < len(parts):
                    comp            = self.component(cur.sch, parts[i])
                    inner           = self.schematics(comp, cur, parts[i + 1]) if comp and i + 1 < len(parts) else []
                    if inner:
                        i          += 1                                         # next part was a configuration name
                    inner           = inner or (self.schematics(comp, cur) if comp else [])
                    if not inner:
                        ok          = False; break
                    cur             = inner[0][1]
                    i              += 1
                target              = self.component(cur.sch, name) if ok else None
                if target is not None:
                    return cur, target
        for s, c in self.walk():                                                # unexpected path: first match anywhere
            if self.prop(c, 'Name') == name:
                return s, c
        return scope, None

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Mask probes: element names of a probed vector signal
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _width(schematic, name):
        """Signal width of a placeholder Constant (zeros(a,b) -> a*b); 1 otherwise."""
        c                           = SignalNames.find(schematic, name) if schematic else None
        value                       = SignalNames.param(c, 'Value') if c and SignalNames.prop(c, 'Type') == 'Constant' else None
        dims                        = [int(x) for x in re.findall(r'\d+', value)] if value and value.startswith(('zeros', 'ones')) else []
        return math.prod(dims) if dims else 1

    def _mask_entries(self, comp, scope, probe):
        """[(element label, underlying signal)] of the mask probe `probe` of comp (active configuration); None if unknown."""
        blk                         = self.content(comp) if comp else None
        mp                          = next((c for c in self.kids(blk, 'MaskProbe') if self.prop(c, 'Name') == probe), None)
        if mp is None:
            return None
        names, schs, idx            = self._configs(comp, scope.env)
        if names != [None] and idx is None:
            return None                                                         # configuration unknown: elements unknown
        active, schematic           = (names[idx], schs[idx]) if names != [None] else (None, blk)
        out                         = []
        for p in self.kids(mp, 'Probe'):
            if active is not None and self.prop(p, 'Path') not in (None, '', active):
                continue
            entry                   = self.prop(p, 'Component')
            signals                 = self._strings(self.prop(p, 'Signals'))
            w                       = self._width(schematic, entry)
            for s in signals:
                label               = entry if len(signals) == 1 else s if entry.lower() in probe.lower() else f"{entry} {s}"
                out                += [(label if w == 1 else f"{label} {k}", s) for k in range(1, w + 1)]
        return out

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Tracing a signal back to its sources: entries (component, probe signal, element label, hint), one per scalar
    #?------------------------------------------------------------------------------------------------------------------------------------
    def _source(self, schematic, name, terminal):
        """(component, terminal) driving input `terminal` of component `name` in schematic."""
        def hit(node):
            if self.prop(node, 'DstComponent') == name and self.prop(node, 'DstTerminal') == str(terminal):
                return True
            return any(hit(b) for b in self.kids(node, 'Branch'))
        for c in self.kids(schematic, 'Connection'):
            if hit(c):
                return self.prop(c, 'SrcComponent'), int(self.prop(c, 'SrcTerminal') or 1)
        return None

    def _inputs(self, schematic, name):
        """Input terminals of component name that a signal connection drives."""
        def dst(node):
            own                     = [self.prop(node, 'DstTerminal')] if self.prop(node, 'DstComponent') == name else []
            return own + [t for b in self.kids(node, 'Branch') for t in dst(b)]
        return {t for c in self.kids(schematic, 'Connection') if self.prop(c, 'Type') == 'Signal' for t in dst(c)}

    def _terminals(self, comp):
        """Terminal entries of comp (instance first, else its library block), numbered in their listed order."""
        return self.kids(comp, 'Terminal') or self.kids(self.content(comp), 'Terminal')

    def _port_index(self, comp, number):
        """(type, index) of terminal `number` of comp."""
        terms                       = self._terminals(comp)
        if not 0 < number <= len(terms):
            return None, None
        t                           = terms[number - 1]
        kind                        = self.prop(t, 'Type')
        index                       = self.prop(t, 'Index') or str(sum(self.prop(x, 'Type') == kind for x in terms[:number]))
        return kind, index

    def _terminal_number(self, comp, kind, index):
        terms                       = self._terminals(comp)
        for k, t in enumerate(terms):
            if self.prop(t, 'Type') == kind and (self.prop(t, 'Index') or str(sum(self.prop(x, 'Type') == kind for x in terms[:k + 1]))) == index:
                return k + 1
        return None

    def _log(self, depth, text):
        self.steps.append(('  ' * min(depth, 30)) + text)

    def _trace_input(self, scope, name, terminal, stops, depth):
        src                         = self._source(scope.sch, name, terminal)
        if not src:
            self._log(depth, f"STOP: nothing connected to input {terminal} of '{name}' in {scope.path()}")
            return None
        return self._trace(scope, src[0], src[1], stops, depth + 1)

    def _trace(self, scope, name, terminal, stops=frozenset(), depth=0):
        """Entries of output `terminal` of component `name` in scope. stops: scopes whose input ports end the trace (MARK)."""
        comp                        = self.component(scope.sch, name)
        if comp is None or depth > 300:
            self._log(depth, f"STOP: no component '{name}' in {scope.path()}" if comp is None else 'STOP: too deep (loop?)')
            return None
        typ                         = self.prop(comp, 'Type')
        self._log(depth, f"{scope.path()}: '{name}' ({typ}) output {terminal}")
        if typ == 'PlecsProbe' or self.kids(comp, 'Probe'):                     # probe: any block with Probe entries
            out                     = []
            for p in self.kids(comp, 'Probe'):
                target              = self.prop(p, 'Component')
                tscope, tcomp       = self._by_path(scope, self.prop(p, 'Path'), target)
                order               = [self.prop(m, 'Name') for m in self.kids(self.content(tcomp), 'MaskProbe')] if tcomp else []
                signals             = self._strings(self.prop(p, 'Signals'))
                for s in sorted(signals, key=lambda s: order.index(s) if s in order else len(order)):   # PLECS: mask probe order
                    entries         = self.labels.get(f"{target}:{s}")
                    entries         = [(l, '') for l in entries] if entries else self._mask_entries(tcomp, tscope, s)
                    if entries and len(entries) == 1:
                        entries     = [('', entries[0][1])]                     # scalar: no element label
                    out            += [(target, s, l, h) for l, h in entries] if entries else [(target, s, '', '')]
            return out
        if typ in ('SignalMux', 'Mux'):
            widths                  = self._mux_widths(scope, comp)
            self._log(depth, f"  Mux '{name}' Width '{self.param(comp, 'Width')}' -> {widths} (-1: taken from the traced input)")
            out                     = []
            for k, w in enumerate(widths):
                sub                 = self._trace_input(scope, name, k + 2, stops, depth) or []
                if w > 0 and len(sub) != w and MARK not in sub:                # declared width differs from the traced signals
                    if len(sub) > 1:
                        self._log(depth, f"  WARNING: Mux '{name}' input {k + 1}: width {w}, {len(sub)} signals traced (names kept, cut / padded)")
                    if len(sub) == 1:                                           # one vector source: number its elements
                        sub         = [(sub[0][0], sub[0][1], f"{sub[0][2]} {j}".strip(), sub[0][3]) for j in range(1, w + 1)]
                    else:
                        sub         = sub[:w] + [(name, f"In{k + 1}", str(j), '') for j in range(len(sub) + 1, w + 1)]
                out                += sub
            return out
        if typ == 'Input':                                                      # port: continue outside the block
            if scope.owner is None:
                self._log(depth, 'STOP: input port at the top level of the model')
                return None
            if id(scope) in stops:
                return [MARK]
            index                   = self.param(comp, 'Index')
            if index is None:                                                   # no Index: the only input port, or its order
                ports               = [c for c in self.kids(scope.sch, 'Component') if self.prop(c, 'Type') == 'Input']
                index               = str(ports.index(comp) + 1)
            n                       = self._terminal_number(scope.owner, 'Input', index)
            if not n:
                terms               = [(self.prop(t, 'Type'), self.prop(t, 'Index')) for t in self._terminals(scope.owner)]
                self._log(depth, f"STOP: input port '{name}' (Index {index}) has no matching terminal on '{self.prop(scope.owner, 'Name')}': {terms}")
                return None
            return self._trace_input(scope.parent, self.prop(scope.owner, 'Name'), n, stops, depth)
        if typ == 'From':
            tag                     = self.param(comp, 'Tag')
            gotos                   = [(s, c) for s, c in self.walk(scope) if self.prop(c, 'Type') == 'Goto' and self.param(c, 'Tag') == tag] + \
                                      [(s, c) for s, c in self.walk() if self.prop(c, 'Type') == 'Goto' and self.param(c, 'Tag') == tag]
            for s, g in gotos:
                res                 = self._trace_input(s, self.prop(g, 'Name'), 1, stops, depth)
                if res:
                    return res
            self._log(depth, f"STOP: no Goto with tag '{tag}' gives a signal ({len(gotos)} found)")
            return None
        if typ in self.PASS_THROUGH:
            return self._trace_input(scope, name, 1, stops, depth)
        kind, index                 = self._port_index(comp, terminal)
        if kind == 'Output':                                                    # subsystem / library block: its Output port
            for _, inner in self.schematics(comp, scope):
                port                = next((c for c in self.kids(inner.sch, 'Component') if self.prop(c, 'Type') == 'Output'
                                            and self.param(c, 'Index') == index), None)
                res                 = self._trace_input(inner, self.prop(port, 'Name'), 1, stops | {id(inner)}, depth) if port else None
                if res and MARK not in res:
                    return res                                                  # sources inside the block (probes)
                if res:
                    break                                                       # computed from its inputs: name it from outside
        return self._elementwise(scope, comp, stops, depth)

    METERS                          = {'Voltmeter': 'Measured voltage', 'Ammeter': 'Measured current', 'Wattmeter': 'Measured power',
                                       'Thermometer': 'Measured temperature', 'HeatFlowMeter': 'Measured heat flow'}

    def _mux_widths(self, scope, comp):
        """Width of each Mux input: the Width parameter evaluated (numbers, or names set in ModelVars / init code);
        -1 where the width is not given (then the traced input decides)."""
        expr                        = self.param(comp, 'Width') or '1'
        value                       = scope.env.eval(expr)
        n_in                        = max([int(t) - 1 for t in self._inputs(scope.sch, self.prop(comp, 'Name')) if t and t.isdigit()] or [0])
        if isinstance(value, (list, tuple)):
            widths                  = [int(v) if isinstance(v, (int, float)) else -1 for v in value]
        elif isinstance(value, (int, float)):
            widths                  = [-1] * int(value)                         # scalar: number of inputs
        elif expr.strip().startswith('['):                                      # names that cannot be evaluated: count them
            widths                  = [-1] * len([x for x in re.split(r'[\s,;]+', expr.strip()[1:-1]) if x])
        else:
            widths                  = [-1] * n_in
        return widths + [-1] * (n_in - len(widths))

    def _elementwise(self, scope, comp, stops, depth):
        """A block computed from its input: one input -> the input names with the block name in front; else its own name.
        Meters (voltmeter, ammeter...) give their name and measured quantity."""
        name                        = self.prop(comp, 'Name')
        typ                         = self.prop(comp, 'Type')
        if typ in self.METERS:
            return [(name, '', '', self.METERS[typ])]
        if self._inputs(scope.sch, name) == {'1'}:
            res                     = self._trace_input(scope, name, 1, stops, depth)
            if res == [MARK] or (res and MARK in res):
                return [MARK]
            if res:
                return [(f"{name} {c}", s, l, h) for c, s, l, h in res]
        return [(name, '', '', '')]

    def tofiles(self):
        """(scope, To File component) of every To File block of the model."""
        return [(s, c) for s, c in self.walk() if self.prop(c, 'Type') == 'ToFile'
                or (self.param(c, 'WriteSignalNames') is not None and self.param(c, 'Filename') is not None)]

    def traced(self, n_columns=None, tofile=None):
        """Entries of the input of the To File block named tofile (else the one whose width is n_columns, else the first)."""
        best                        = None
        for s, c in self.tofiles():
            if tofile and self.prop(c, 'Name') != tofile:
                continue
            res                     = [e for e in (self._trace_input(s, self.prop(c, 'Name'), 1, frozenset(), 0) or []) if e != MARK]
            if res and (n_columns is None or len(res) == n_columns):
                return res
            best                    = best or res
        return best

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Result CSV columns
    #?------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def header(csv_file):
        """Signal names of the To File header, without the time column."""
        with open(csv_file, encoding='utf-8-sig', errors='ignore') as f:
            line                    = f.readline().strip()
        sep                         = max((',', ';', '\t'), key=line.count)    # ',' (PLECS), ';' or tab (re-saved by other tools)
        return [h.strip().strip('"') for h in line.split(sep)][1:]

    @staticmethod
    def _name(comp, probe, label):
        title                       = probe if probe and probe.lower().startswith(comp.lower()) else f"{comp} {probe}".strip()
        return f"{title} {label}".strip()                                       # 'Load:Load Voltage' -> 'Load Voltage'

    def _scoped(self, name):
        return next(((s, c) for s, c in self.walk() if self.prop(c, 'Name') == name), (self.top, None))

    def columns(self, csv_file, tofile=None):
        """(names, unit hints) of the columns of csv_file: the header where PLECS wrote real names, the model elsewhere."""
        header                      = self.header(csv_file)
        split                       = lambda h: (h.rpartition(':')[0], h.rpartition(':')[2]) if h.rpartition(':')[2].isdigit() else (h, '')
        groups                      = {}
        for h in header:
            groups[split(h)[0]]     = groups.get(split(h)[0], 0) + 1
        unnamed                     = lambda h: self.GENERIC.match(h) or not split(h)[0].partition(':')[2]   # 'ToFile_In_1', 'RMS Value:3'
        traced                      = self.traced(len(header), tofile)
        if traced and len(traced) != len(header):
            if all(unnamed(h) for h in header):                                 # header carries no names at all: keep the model's
                warnings.warn(f"{len(header)} columns in the CSV header, {len(traced)} signals traced in the model: "
                              f"names assigned in order, check the result (python signals.py <csv> <model> --debug)")
                traced              = (traced + [(h, '', '', '') for h in header])[:len(header)]
            else:
                traced              = None
        cache, names, hints         = {}, [], []
        for i, h in enumerate(header):
            key, idx                = split(h)
            comp, _, probe          = key.partition(':')
            if traced and unnamed(h):                                           # PLECS could not name it: the model's name
                c, s, label, hint   = traced[i]
                names.append(self._name(c, s, label)); hints.append(f"{s} {hint}".lower())
                continue
            if key not in cache:
                entries             = [(l, '') for l in self.labels[key]] if key in self.labels else \
                                      self._mask_entries(*reversed(self._scoped(comp)), probe) if self._scoped(comp)[1] else None
                cache[key]          = entries if entries and (not idx or len(entries) == groups[key]) else None
            entries                 = cache[key]
            if idx and not entries and traced:                                  # vector the mask probe does not name
                c, s, label, hint   = traced[i]
                entries_i           = (label or idx, hint)
            else:
                entries_i           = entries[int(idx) - 1] if idx and entries else (idx, entries[0][1] if entries else '')
            names.append(self._name(comp, probe, entries_i[0]))
            hints.append(f"{probe} {entries_i[1]}".lower())
        return names, hints

    def report(self, csv_file=None):
        """Text: libraries found, every To File block (where, fed by what) and the signals traced into it; the CSV header."""
        out                         = [f"libraries: {', '.join(sorted(self.lib_files)) or 'none'} "
                                       f"(PLECS components.plecs: {self._library_file('Components') or 'not found'})"]
        missing                     = sorted({self.prop(c, 'SrcComponent') for _, c in self.walk()
                                              if self.prop(c, 'Type') == 'Reference' and self.content(c) is None})
        builtin                     = [m for m in missing if m.startswith('Components/')]
        missing                     = [m for m in missing if not m.startswith('Components/')]
        if builtin:
            out                    += [f"PLECS built-in blocks used as black boxes (named from their input, no library file needed): "
                                       f"{len(builtin)}, e.g. {[b.rsplit('/', 1)[-1] for b in builtin[:6]]}"]
        if missing:
            out                    += [f"blocks from YOUR libraries not found (pass their folder as lib_dir): {missing}"]
        if csv_file:
            header                  = self.header(csv_file)
            out                    += [f"CSV header: {len(header)} columns after time: {header[:12]}{' ...' if len(header) > 12 else ''}"]
        tofiles                     = self.tofiles()
        for s, c in tofiles:
            self.steps              = []
            res                     = [e for e in (self._trace_input(s, self.prop(c, 'Name'), 1, frozenset(), 0) or []) if e != MARK]
            out                    += [f"To File '{self.prop(c, 'Name')}' in {s.path()}: input from {self._source(s.sch, self.prop(c, 'Name'), 1)}, "
                                       f"{len(res)} signals"]
            out                    += [f"    {k + 1:3d}  {self._name(a, b, l)}" for k, (a, b, l, _) in enumerate(res)]
            if not res or any(st.lstrip().startswith('STOP') for st in self.steps):
                out                += ['  trace (where it stops):'] + [f"    {st}" for st in self.steps[:80]] +                                       ([f"    ... {len(self.steps) - 80} more steps"] if len(self.steps) > 80 else [])
        if not tofiles:
            out                    += ['no To File block found in the model']
        return NL.join(out)
#?----------------------------------------------------------------------------------------------------------------------------------------
#? Run this file (VS Code: Run Python File, the play button) to list the signals of a model. Set the paths here;
#? command-line arguments, when given, replace them.
#?----------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    MODEL                           = r'D:\WORKSPACE\0049_SP_BTP_PFC_1KW\model\testmodel.plecs'   # model to read
    LIB_DIRS                        = [r'D:\WORKSPACE\0000_libraries\Plecs']                   # folders of your libraries ([] = none)
    CSV                             = None                                                   # result CSV to name its columns (None = names from the model)
    VARS                            = None                                                   # ModelVars: dict, or path of a JSON file (None = values saved in the model)
    DEBUG                           = True                                                   # also print libraries, To File blocks and the trace

    import json
    import sys
    argv                            = sys.argv[1:]
    if argv:                                                                    # python signals.py [result.csv] model.plecs [lib_dir ...] [--vars f.json] [--debug]
        DEBUG                       = '--debug' in argv
        if '--vars' in argv:
            k                       = argv.index('--vars')
            VARS                    = argv[k + 1]
            del argv[k:k + 2]
        args                        = [a for a in argv if not a.startswith('--')]
        CSV, MODEL, LIB_DIRS        = (None, args[0], args[1:]) if args[0].endswith('.plecs') else (args[0], args[1], args[2:])
    if isinstance(VARS, str):
        with open(VARS, encoding='utf-8') as f:
            VARS                    = json.load(f)
        VARS                        = VARS.get('ModelVars', VARS) if isinstance(VARS, dict) else {}
    if DEBUG:
        print(SignalNames(MODEL, LIB_DIRS, VARS).report(CSV)); print()
    names, units                    = SignalNames.read(CSV, MODEL, LIB_DIRS, VARS, units=True) if CSV else \
                                      SignalNames.from_model(MODEL, LIB_DIRS, VARS, units=True)
    for n, u in zip(names, units):
        print(f"{u:8s} {n}")
