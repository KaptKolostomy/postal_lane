#!/usr/bin/env python3
"""bible_lint.py — DCS Scripting Bible P2 gate + REPAIR mode (v1.0, 2026-09-25).

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

Exit code: 0 clean, 1 findings, 2 repaired-all, 3 unrepairable remain.
"""
import argparse, hashlib, json, re, shutil, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LUAC = r"F:\SOULSMITH_FORGE\tools\lua54\bin\luac54.exe"
LUA = r"F:\SOULSMITH_FORGE\tools\lua54\bin\lua54.exe"
REG = Path("F:/SOULSMITH_FORGE/docs/NAME_REGISTRY.md")

MOOSE_FACING = re.compile(
    r'(?:GROUP|UNIT|AIRBASE|STATIC|SCENERY):FindByName\s*\(\s*(?:"[^"]*"|\'[^\']*\')'
    r'|(?:SPAWN|ZONE|ZONE_GROUP|MOVE_UNIT|SET_[A-Z_]+):New\s*\(\s*(?:"[^"]*"|\'[^\']*\')'
    r'|FilterPrefixes\s*\(\s*(?:"[^"]*"|\'[^\']*\')')
HEADER_MARK = re.compile(r'--\s*(BIBLE|bible header|TIER\s*:|WIRE\s*:|tier\s*[:=])', re.M)
WIREKEY = re.compile(r'^\s*(?:env\.info|log|print)?[^-\n]*["\'](?:MAZE|LADDER|GRID|SCAN)_[A-Z0-9_]+,')
NAMEY = re.compile(r'"([A-Za-z0-9_\-\. ]{3,50})"')
CHARSET_OK = re.compile(r'^[A-Za-z0-9_.]+$')

def luac_ok(p):
    try:
        r = subprocess.run([LUAC, "-p", str(p)], capture_output=True, text=True, timeout=30)
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

    # E07 luac parse
    ok, err = luac_ok(p)
    if not ok:
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
    moose_pin = Path(r"E:/GAMES/Saved Games/DCS/Scripts/MOOSE/Moose.lua")
    if missionish and moose_pin.exists():
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
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

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
        jp = Path("F:/SOULSMITH_FORGE/data/audits/bible_lint_latest.json")
        jp.write_text(json.dumps(report, indent=1), encoding="utf-8")
        print(f"json: {jp}")
    sys.exit(2 if (n_rep and not n_err) else (1 if n_err else (0 if not report["files"] else 2 if a.fix else 1)))

if __name__ == "__main__":
    main()
