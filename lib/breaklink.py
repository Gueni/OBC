#!/usr/bin/env python
# coding=utf-8
#? -------------------------------------------------------------------------------
#?
#?           __                    __   ___       __
#?          / /_  ________  ____ _/ /__/ (_)___  / /__
#?         / __ \/ ___/ _ \/ __ `/ //_/ / / __ \/ //_/
#?        / /_/ / /  /  __/ /_/ / ,< / / / / / / ,<
#?       /_.___/_/   \___/\__,_/_/|_/_/_/_/ /_/_/|_|
#?
#?
#? Name:        breaklink.py
#? Purpose:     break the library links of a PLECS model and save it: each Reference block becomes a copy of its
#?              library block, with the mask values of the reference (user libraries and the PLECS built-in library).
#?              Standalone (standard library only): copy the file to any project.
#?                  path = break_links('model.plecs', 'lib_dir')                  # -> model_nolink.plecs
#?
#? Author:      Mohamed Gueni ( mohamedgueni@outlook.com)
#?
#? Created:     11/04/2026
#? Licence:     Refer to the LICENSE file
#? -------------------------------------------------------------------------------
#? -------------------------------------------------------------------------------
import copy
import glob
import os
import re
from   pathlib              import  Path

NL                                  = chr(10)
#?----------------------------------------------------------------------------------------------------------------------------------------
def break_links(model_path, lib_dir=None, out=None, builtins=True):
    """Break every library link of model_path and save the model; returns the saved path.

    model_path  .plecs model (text format)
    lib_dir     folder, or list of folders, of the user libraries (the model folder is always searched)
    out         output file (default <model>_nolink.plecs next to the model; pass model_path to overwrite the model)
    builtins    True: also break the links to the PLECS built-in library (Components/...)
    """
    return LinkBreaker(model_path, lib_dir, builtins).save(out)
#?----------------------------------------------------------------------------------------------------------------------------------------
class PlecsBlock:
    """'Tag {' block of a .plecs file, kept as text: items are ['prop', key, raw lines] or ['block', PlecsBlock], in file order."""

    def __init__(self, tag):
        self.tag                    = tag
        self.items                  = []

    def props(self, key):
        return [it for it in self.items if it[0] == 'prop' and it[1] == key]

    def raw(self, key):
        """Raw value of key (string pieces joined, outer quotes kept), None if missing."""
        p                           = self.props(key)
        if not p:
            return None
        lines                       = p[0][2]
        value                       = lines[0].strip().partition(' ')[2].strip()
        for l in lines[1:]:
            value                   = value[:-1] + l.strip()[1:]
        return value

    def value(self, key):
        """String value of key without its quotes (escapes kept as written: \\n, \\\\, \\")."""
        v                           = self.raw(key)
        return v[1:-1] if v and len(v) >= 2 and v[0] == v[-1] == '"' else v

    def set(self, key, item_lines, after=None):
        """Replace key by raw lines ('Key  "value"' + continuation pieces); insert it (after the item 'after', or
        before the first child block) when missing."""
        new                         = ['prop', key, list(item_lines)]
        for k, it in enumerate(self.items):
            if it[0] == 'prop' and it[1] == key:
                self.items[k]       = new; return
        idx                         = next((k + 1 for k, it in enumerate(self.items) if after and it[0] == 'prop' and it[1] == after), None)
        if idx is None:
            idx                     = next((k for k, it in enumerate(self.items) if it[0] == 'block'), len(self.items))
        self.items.insert(idx, new)

    def drop(self, key):
        self.items                  = [it for it in self.items if not (it[0] == 'prop' and it[1] == key)]

    def kids(self, tag=None):
        return [it[1] for it in self.items if it[0] == 'block' and (tag is None or it[1].tag == tag)]

    def text(self, depth=0):
        """Lines of the block; the root block (tag None) gives its items without a frame."""
        if self.tag is None:
            return sum(([it[2][0].strip()] + it[2][1:] if it[0] == 'prop' else it[1].text(depth) for it in self.items), [])
        pad                         = '  ' * depth
        out                         = [f"{pad}{self.tag} {{"]
        for it in self.items:
            if it[0] == 'prop':
                out                += [pad + '  ' + it[2][0].strip()] + it[2][1:]       # continuation pieces stay at column 0
            else:
                out                += it[1].text(depth + 1)
        return out + [f"{pad}}}"]

    @staticmethod
    def load(path):
        """Root block of a .plecs file, and its line ending."""
        data                        = Path(path).read_bytes()
        if data[:2] == b'PK' or b'\x00' in data[:4096]:
            raise ValueError(f"{path}: binary or zipped file, not a PLECS text model (save it as a plain .plecs model)")
        text                        = data.decode('utf-8-sig', errors='replace')
        root                        = PlecsBlock(None)
        stack, last                 = [root], None
        for line in text.splitlines():
            s                       = line.strip()
            if not s:
                continue
            if line.startswith('"') and last is not None:                         # piece of a string split over lines
                last[2].append(line); continue
            last                    = None
            if re.match(r'^[A-Za-z_]\w*\s*\{$', s):
                b                   = PlecsBlock(s[:-1].strip())
                stack[-1].items.append(['block', b]); stack.append(b)
            elif s == '}':
                if len(stack) > 1:
                    stack.pop()
            else:
                last                = ['prop', s.split()[0], [s]]
                stack[-1].items.append(last)
        if not root.kids('Plecs'):
            raise ValueError(f"{path}: does not start like a PLECS model ('Plecs {{')")
        return root, '\r\n' if '\r\n' in text else '\n'

    def save(self, path, newline='\n'):
        Path(path).write_text(NL.join(self.text()) + NL, encoding='utf-8', newline=newline)
        return Path(path)
#?----------------------------------------------------------------------------------------------------------------------------------------
class LinkBreaker:
    """Library links of a PLECS model: find the library block behind each Reference and put a copy of it in its place."""

    SUFFIX                          = '_nolink'
    LIBRARY_ONLY                    = ('LibraryKeywords',)                       # keys that only mean something in a library
    PLECS_DIRS                      = ['$PLECS_DIR', '~/Documents/Plexim/PLECS*', '~/AppData/Local/Plexim/PLECS*', '~/AppData/Roaming/Plexim/PLECS*',
                                       'C:/Program Files/Plexim/PLECS*', 'C:/Program Files (x86)/Plexim/PLECS*', 'C:/ProgramData/Plexim/PLECS*',
                                       'C:/Plexim/PLECS*', '/Applications/PLECS*', '~/Plexim/PLECS*', '/opt/plexim/plecs*']   # PLECS installations
    MAX_DEPTH                       = 40                                         # library blocks inside library blocks

    def __init__(self, model_path, lib_dir=None, builtins=True):
        self.model                  = Path(model_path)
        dirs                        = [lib_dir] if isinstance(lib_dir, (str, Path)) else list(lib_dir or [])
        self.lib_files              = {}
        for d in [self.model.parent] + [Path(x) for x in dirs]:
            for f in sorted(Path(d).glob('*.plecs')):
                self.lib_files.setdefault(f.stem.lower(), f)
        self.builtins               = builtins
        self.trees                  = {}
        self.missing                = set()
        self.root, self.newline     = PlecsBlock.load(self.model)
        self.plecs                  = self.root.kids('Plecs')[0]
        self.broken                 = self.unlink(self.plecs)

    def save(self, out=None, tag='breaklink'):
        """Save the model without links (model name = file name); returns the path."""
        out                         = Path(out) if out else self.model.with_name(self.model.stem + self.SUFFIX + self.model.suffix)
        self.plecs.set('Name', [f'Name          "{out.stem}"'])
        self.root.save(out, self.newline)
        print(f"{tag}: {out}  ({self.broken} library links broken)")
        if self.missing:
            print(f"{tag}: library block not found, kept as a link: {', '.join(sorted(self.missing))}")
        return out

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Libraries
    #?------------------------------------------------------------------------------------------------------------------------------------
    def _library_file(self, name):
        f                           = self.lib_files.get(name.lower())
        if f is None and name == 'Components' and 'components' not in self.lib_files:   # PLECS built-in library, newest installation
            hits                    = []
            for d in self.PLECS_DIRS:
                d                   = os.path.expandvars(os.path.expanduser(d))
                for depth in ('', '*', '*/*', '*/*/*'):
                    hits           += glob.glob(os.path.join(d, depth, 'components.plecs'))
            f                       = self.lib_files['components'] = Path(max(hits, key=os.path.getmtime)) if hits else None
        return f

    @staticmethod
    def _component(sch, name):
        return next((c for c in sch.kids('Component') if c.value('Name') == name), None) if sch else None

    @classmethod
    def _find(cls, block, name):
        for c in block.kids():
            if c.tag == 'Component' and c.value('Name') == name:
                return c
            hit                     = cls._find(c, name)
            if hit:
                return hit
        return None

    def library_block(self, src):
        """Library block behind SrcComponent src ('Power/EVSE\\\\/GRID', 'Components/Control/Filters/RMS Value'), or None."""
        src                         = src.replace('\\\\', '\\')                 # one level of string escape: names compare as written
        parts                       = [p.replace('\\/', '/') for p in re.split(r'(?<!\\)/', src)]
        if len(parts) < 2 or (parts[0] == 'Components' and not self.builtins):
            return None
        f                           = self._library_file(parts[0])
        if f is None:
            return None
        if f not in self.trees:
            self.trees[f]           = PlecsBlock.load(f)[0]
        plecs                       = (self.trees[f].kids('Plecs') or [self.trees[f]])[0]
        sch, blk                    = (plecs.kids('Schematic') or [plecs])[0], None
        for k, part in enumerate(parts[1:]):                                    # library folders, then the block
            blk                     = self._component(sch, part)
            if blk is None or k == len(parts) - 2:
                break
            sch                     = (blk.kids('Schematic') or [None])[0]
        return blk or self._find(plecs, parts[-1])

    #?------------------------------------------------------------------------------------------------------------------------------------
    #? Break the links
    #?------------------------------------------------------------------------------------------------------------------------------------
    def _broken(self, ref, depth):
        """Copy of the library block of the Reference ref, with the name, place and mask values of ref."""
        src                         = ref.value('SrcComponent') or ''
        lib                         = self.library_block(src) if depth < self.MAX_DEPTH else None
        if lib is None:
            if not src.startswith('Components/') or self.builtins:
                self.missing.add(src)
            return None
        blk                         = copy.deepcopy(lib)
        for key in self.LIBRARY_ONLY:
            blk.drop(key)
        prev                        = 'Type'
        for it in ref.items:                                                    # name, position, orientation ... of the reference
            if it[0] == 'prop' and it[1] not in ('Type', 'SrcComponent'):
                blk.set(it[1], it[2], after=prev); prev = it[1]
        params                      = {p.value('Variable'): p for p in blk.kids('Parameter')}
        for p in ref.kids('Parameter'):                                         # mask values (and the selected configuration)
            target                  = params.get(p.value('Variable'))
            if target is None:
                blk.items.append(['block', copy.deepcopy(p)])
            elif p.props('Value'):
                target.set('Value', p.props('Value')[0][2])
        return blk

    def unlink(self, block, depth=0):
        """Replace every Reference below block by its library block (recursively); number of links broken."""
        n                           = 0
        for k, it in enumerate(block.items):
            if it[0] != 'block':
                continue
            child                   = it[1]
            if child.tag == 'Component' and child.value('Type') == 'Reference':
                new                 = self._broken(child, depth)
                if new is not None:
                    block.items[k]  = ['block', new]; child = new; n += 1
            n                      += self.unlink(child, depth + 1)
        return n
#?----------------------------------------------------------------------------------------------------------------------------------------
#? Run this file (VS Code: Run Python File, the play button) to break the links of a model. Set the paths here;
#? command-line arguments, when given, replace them:  python breaklink.py model.plecs [lib_dir ...] [--out f.plecs] [--keep-builtins]
#?----------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    MODEL                           = r'D:\WORKSPACE\0049_SP_BTP_PFC_1KW\model\PFC.plecs'      # model to break the links of
    LIB_DIRS                        = [r'D:\WORKSPACE\0000_libraries\Plecs']                   # folders of your libraries ([] = none)
    OUT                             = None                                                   # None = <model>_nolink.plecs next to the model
    BUILTINS                        = True                                                   # also break the links to the PLECS built-in library

    import sys
    argv                            = sys.argv[1:]
    if argv:
        BUILTINS                    = '--keep-builtins' not in argv
        if '--out' in argv:
            k                       = argv.index('--out')
            OUT                     = argv[k + 1]
            del argv[k:k + 2]
        args                        = [a for a in argv if not a.startswith('--')]
        MODEL, LIB_DIRS             = args[0], args[1:]
    break_links(MODEL, LIB_DIRS, OUT, BUILTINS)
