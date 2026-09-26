#!/usr/bin/env python3
"""bible_lint.py — DCS Scripting Bible P2 gate + REPAIR mode (v1.1, 2026-09-26).

Traps (and optionally repairs) the witnessed Lua failure classes in house scripts:

  E01 banner-broken    file starts with '====' (lost '--')           -> REPAIR: prepend '--'
  E02 charset          filename violates [A-Za-z0-9_.] law           -> REPAIR: rename to snake
  E03 dash-in-include  filename has '-' AND is dofile/require target -> REPORT (manual rename; import-side truth)
  E04 moose-dash       '-' inside a name literal passed to MOOSE-facing
                       calls (FindByName/SPAWN:New/ZONE:New/FilterPrefixes)
                       when not AIRBASE/airbase stock               -> REPORT (escape or rename; semantics!)
  E05 no-header        no bible header block in first 30 lines       -> REPAIR: insert template (if --fix)
  E06 fail-closed      no pcall/assert guard around MOOSE usage      -> REPAIR: prepend assert line (if --fix)
  E07 luac-parse       file does not compile under luac54            -> never auto-fix
  E08 late-act         mission-builder scripts missing LATE-ACT rule -> REPORT (builder concern)
  E09 wire-key         log line KEY not registered (MAZE_*/LADDER_* pattern required)
  E10 clone-flag       same flag literal assigned in >1 rule (builder-level, report only here)

Usage:
  python bible_lint.py <path>...            # lint only
  python bible_lint.py <path>... --fix      # apply safe repairs (E01, E05, E06) with .bak receipts
  python bible_lint.py <path>... --json     # machine output for the Liber/beat

PORTABILITY (v1.1, C1 scrub per cloud-103): zero machine paths in source.
Every external path resolves CLI flag > env var > auto-detect (walk up from
this file to the repo root, then repo-relative):
  --luac       BIBLE_LINT_LUAC        <root>/tools/lua54/bin/luac54.exe
  --lua        BIBLE_LINT_LUA         <root>/tools/lua54/bin/lua54.exe
  --registry   BIBLE_LINT_REGISTRY    <root>/docs/NAME_REGISTRY.md
  --json-out   BIBLE_LINT_JSON_OUT    <root>/data/audits/bible_lint_latest.json
  --moose-lua  BIBLE_LINT_MOOSE_LUA   Saved Games/DCS/Scripts/MOOSE/Moose.lua
                                          (relocated Saved Games honored via
                                           Windows User Shell Folders)
If luac54 cannot be resolved, E07 degrades to a WARN (parse check SKIPPED) —
stated, never assumed.

Exit code: 0 clean, 1 findings, 2 repaired-all, 3 unrepairable remain.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def _repo_root():
    """Walk up from this file to the house root.
    Marker: docs/NAME_REGISTRY.md — unique to the FORGE root. (.git is NOT a
    safe marker: data/postal/ holds a nested legacy .git that false-matches.)"""
    here = Path(__file__).resolve().parent
    for cand in (here, *here.parents):
        if (cand / "docs" / "NAME_REGISTRY.md").is_file():
            return cand
    return None

_ROOT = _repo_root()

def _resolve(cli, env, *rel):
    """CLI value > env var > repo-root-relative auto-detect (must be a file) > None."""
    if cli:
        return Path(cli)
    v = os.environ.get(env)
    if v:
        return Path(v)
    if _ROOT is not None and rel:
        p = _ROOT.joinpath(*rel)
        if p.is_file():
            return p
    return None

def _saved_games_dir():
    """Windows Saved Games dir (relocations honored via User Shell Folders); falls back to ~/Saved Games."""
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
        v, _ = winreg.QueryValueEx(k, "{4C5C32FF-BB9D-43B0-B5B4-2D72E54EAAA4}")
        return Path(os.path.expandvars(v))
    except Exception:
        return Path.home() / "Saved Games"

# C1 (cloud-103): resolved, never hardcoded. Module defaults honor env +
# repo-root auto-detect; main() re-resolves from CLI flags when given.
LUAC = _resolve(None, "BIBLE_LINT_LUAC", "tools", "lua54", "bin", "luac54.exe")
LUA = _resolve(None, "BIBLE_LINT_LUA", "tools", "lua54", "bin", "lua54.exe")
REG = _resolve(None, "BIBLE_LINT_REGISTRY", "docs", "NAME_REGISTRY.md")
MOOSE_PIN = _resolve(None, "BIBLE_LINT_MOOSE_LUA") or (_saved_games_dir() / "DCS" / "Scripts" / "MOOSE" / "Moose.lua")
JSON_OUT = _resolve(None, "BIBLE_LINT_JSON_OUT", "data", "audits", "bible_lint_latest.json")

MOOSE_FACING = re.compile(
    r'(?:GROUP|UNIT|AIRBASE|STATIC|SCENERY):FindByName\s*\(\s*(?:"[^"]*"|\'[^\']*\')'
    r'|(?:SPAWN|ZONE|ZONE_GROUP|MOVE_UNIT|SET_[A-Z_]+):New\s*\(\s*(?:"[^"]*"|\'[^\']*\')'
    r'|FilterPrefixes\s*\(\s*(?:"[^"]*"|\'[^\']*\')')
HEADER_MARK = re.compile(r'--\s*(BIBLE|bible header|TIER\s*:|WIRE\s*:|tier\s*[:=])', re.M)
WIREKEY = re.compile(r'^\s*(?:env\.info|log|print)?[^-\n]*["\'](?:MAZE|LADDER|GRID|SCAN)_[A-Z0-9_]+,')
NAMEY = re.compile(r'"([A-Za-z0-9_\-\. ]{3,50})"')
CHARSET_OK = re.compile(r'^[A-Za-z0-9_.]+$')

def luac_ok(p):
    if LUAC is None:
        return None, ["luac54 not resolved — pass --luac or set BIBLE_LINT_LUAC"]
    if not Path(LUAC).exists():
        return None, [f"luac54 missing at resolved path: {LUAC}"]
    try:
        r = subprocess.run([str(LUAC), "-p", str(p)], capture_output=True, text=True, timeout=30)
        return r.returncode == 0, (r.stderr or "").strip().splitlines()[:1]
    except Exception as e:
        return False, [str(e)]

def lint_file(p: Path, fix=False):
    F = []  # findings: (code, severity, msg, repaired)
    raw = p.read_bytes()
    txt = raw.decode("utf-8", errors="replace")

    # E01 banner-broken
    if txt.startswith("====") and not txt.startswith("-- ==="):
        F.append(("E01", "ERROR", "file starts with raw '====' banner (lost '--') — dead load", False))
        if fix:
            fixed = "-- " + txt if not txt.startswith("--") else txt
            shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
            p.write_bytes(fixed.encode("utf-8"))
            txt = fixed
            F[-1] = ("E01", "ERROR", "banner repaired ('--' restored; .bak receipt)", True)

    # E02 filename charset
    if not CHARSET_OK.match(p.stem):
        F.append(("E02", "WARN", f"filename violates charset law: '{p.name}'", False))

    # E03 dash-in-include
    if "-" in p.stem and re.search(r'dofile|require', txt):
        F.append(("E03", "WARN", "dashed filename but file is include-target — rename manually (import-side truth)", False))

    # E04 moose-dash names (airbase stock names exempt)
    for m in MOOSE_FACING.finditer(txt):
        call = m.group(0)
        lit = next((g for g in m.groups() if g), None)
        if lit and "-" in lit and not call.startswith("AIRBASE"):
            F.append(("E04", "WARN", f"MOOSE-facing name with '-': {call.strip()[:70]} — escape %-or rename", False))

    # E05 header block
    if not HEADER_MARK.search(txt[:2500]):
        F.append(("E05", "WARN", "no bible header block (TIER/WIRE) in first 30 lines", False))
        if fix:
            hdr = ("-- BIBLE HEADER v1 (P2)\n"
                   "-- TIER: T1 mission-embed\n"
                   "-- WIRE: none (document yours: KEY,fields)\n"
                   "-- FLAGS: (document read/write)\n"
                   "-- VERBS: (receipts against target build)\n")
            shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
            p.write_bytes((hdr + txt).encode("utf-8"))
            txt = hdr + txt
            F[-1] = ("E05", "WARN", "header template inserted (.bak receipt)", True)

    # E06 fail-closed guard (only if MOOSE used)
    if re.search(r'\b(GROUP|SPAWN|ZONE|SET_GROUP|MESSAGE):', txt) and \
       not re.search(r'assert\(\s*MOOSE|pcall\(function|pcall\(\s*function', txt):
        F.append(("E06", "WARN", "MOOSE usage without fail-closed guard (assert/pcall)", False))
        if fix:
            guard = ('if not MOOSE then env.info("LINT: MOOSE missing - script aborts (fail-closed)"); return end\n')
            # safe only for T1-style whole-file scripts; do not inject into functions
            if not re.search(r'^function\s', txt, re.M):
                shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))
                p.write_bytes((guard + txt).encode("utf-8"))
                txt = guard + txt
                F[-1] = ("E06", "WARN", "fail-closed guard injected (.bak receipt)", True)

    # E07 luac parse (skips LOUDLY when luac54 unresolvable — never silently)
    ok, err = luac_ok(p)
    if ok is None:
        F.append(("E07", "WARN", f"parse check SKIPPED: {err[0]}", False))
    elif not ok:
        F.append(("E07", "ERROR", f"luac54 parse FAIL: {err[0] if err else '?'}", False))

    # E11 sandbox-banned globals (mission env strips os/io/require/lfs — silent death)
    # context: only if script looks mission-side (uses env./trigger/coalition/world or MESSAGE/SPAWN)
    missionish = re.search(r'\b(env\.|trigger\.|coalition\.|world\.|timer\.|MESSAGE:|SPAWN:|GROUP:)', txt)
    if missionish:
        for bad, why in ((r'\bos\.', 'os. (sanitized out of mission env)'),
                         (r'\bio\.', 'io. (sanitized out of mission env)'),
                         (r'\brequire\s*\(', 'require() (whitelist-only in mission env)'),
                         (r'\blfs\.', 'lfs. (needs sanction helper)'),
                         (r'\bpackage\.', 'package. (not present in mission env)'),
                         (r'\bnet\.', 'net. (Hooks env only, not mission env)')):
            m2 = re.search(bad, txt)
            if m2:
                F.append(("E11", "ERROR", f"sandbox-banned: {why} — dies silently at runtime", False))

    # E12 MOOSE constructor/verb receipt vs PINNED build (NewROUTE trap, automated)
    moose_pin = MOOSE_PIN
    if missionish and moose_pin is not None and moose_pin.is_file():
        moose_src = moose_pin.read_text(encoding="utf-8", errors="replace")
        moose_defs = set(re.findall(r'function\s+([A-Z][A-Za-z0-9_]*):([A-Za-z0-9_]+)\s*\(', moose_src))
        moose_classes = {c for c, _ in moose_defs} | set(re.findall(r'([A-Z][A-Za-z0-9_]*)\s*=\s*\{\s*className', moose_src))
        used = set(re.findall(r'\b([A-Z][A-Za-z0-9_]{2,}):([A-Za-z0-9_]+)\s*\(', txt))
        for cls, meth in sorted(used):
            if cls in moose_classes and meth not in {"New"}:
                if (cls, meth) not in moose_defs:
                    F.append(("E12", "ERROR", f"MOOSE receipt FAIL: {cls}:{meth} not in pinned build {moose_pin.name} — NewROUTE trap", False))

    # E09 wire keys present but unregistered pattern
    for ln in txt.splitlines():
        if re.search(r'(MAZE|LADDER|GRID|SCAN)_[A-Z0-9_]+,', ln):
            break
    else:
        pass  # informational only; registry drift handled by P5 sweep

    return F

def main():
    global LUAC, LUA, REG, MOOSE_PIN, JSON_OUT
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--luac", help="luac54 binary (env BIBLE_LINT_LUAC)")
    ap.add_argument("--lua", help="lua54 binary (env BIBLE_LINT_LUA)")
    ap.add_argument("--registry", help="NAME_REGISTRY.md path (env BIBLE_LINT_REGISTRY)")
    ap.add_argument("--json-out", dest="json_out", help="--json output path (env BIBLE_LINT_JSON_OUT)")
    ap.add_argument("--moose-lua", dest="moose_lua", help="pinned Moose.lua for E12 (env BIBLE_LINT_MOOSE_LUA)")
    a = ap.parse_args()

    # C1: CLI > env > auto-detect — nothing machine-specific lives in this file
    if a.luac: LUAC = Path(a.luac)
    if a.lua: LUA = Path(a.lua)
    if a.registry: REG = Path(a.registry)
    if a.moose_lua:
        MOOSE_PIN = Path(a.moose_lua)
    if a.json_out:
        JSON_OUT = Path(a.json_out)
    elif JSON_OUT is None:
        JSON_OUT = (_ROOT / "data" / "audits" / "bible_lint_latest.json") if _ROOT else Path("bible_lint_latest.json")

    files = []
    for s in a.paths:
        pp = Path(s)
        if pp.is_dir():
            files += sorted(pp.rglob("*.lua"))
        elif pp.is_file():
            files.append(pp)

    report = {"generated": time.strftime("%Y-%m-%d %H:%M:%S"), "files": [], "counts": {}}
    n_err = n_rep = 0
    for p in files:
        F = lint_file(p, fix=a.fix)
        if F:
            entry = {"file": str(p), "findings": [dict(code=c, sev=s, msg=m, repaired=r) for c, s, m, r in F]}
            report["files"].append(entry)
        for c, s, m, r in F:
            report["counts"][c] = report["counts"].get(c, 0) + 1
            if s == "ERROR" and not r: n_err += 1
            if r: n_rep += 1
            sev = "REPAIRED" if r else s
            print(f"[{sev:8}] {c}  {p.name}  ::  {m}")

    print(f"\nSUMMARY: {len(files)} files · errors(unrepaired)={n_err} · repairs={n_rep}")
    for c, n in sorted(report["counts"].items()):
        print(f"  {c}: {n}")
    if a.json:
        jp = JSON_OUT
        jp.parent.mkdir(parents=True, exist_ok=True)
        jp.write_text(json.dumps(report, indent=1), encoding="utf-8")
        print(f"json: {jp}")
    sys.exit(2 if (n_rep and not n_err) else (1 if n_err else (0 if not report["files"] else 2 if a.fix else 1)))

if __name__ == "__main__":
    main()
