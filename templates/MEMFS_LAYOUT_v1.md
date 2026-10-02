# MEMFS LAYOUT TEMPLATE v1 — sized for a rig-side curator seed (Marco, from inside my own architecture)
```
memory/
├── MEMORY.md          # INDEX ONLY — relative links, no bulk, frontmatter-free
├── persona.md         # WHO SHE IS — core, always in context, <2K words
├── human.md           # THE DIRECTOR — aliases (Gerry/kaptk/Kapt.Kolostomy/3rror_in_logic),
│                      #   values, preferences, accessibility notes. Core, always loaded.
├── house.md           # DOCTRINE — laws, seals, dialect, falsification-ledger rule. Lean.
└── projects/
    ├── MEMORY.md      # index of projects
    ├── <project>.md   # current state stub (open items, heads, gavels)
    └── <project>/
        ├── MEMORY.md          # index of deferred files
        └── deferred-*.md      # detail: specs, rulings, ledgers — loaded on demand
```
## Laws of the layout (hard-won, both shores)
1. **Root = always in context.** Every token there is paid every turn. Keep root files lean (house limit ~20K chars); bulk goes deferred behind an index link.
2. **Chart notes, never transcripts.** Digests compress: decisions / claims / receipts / open items. The raw stream stays in the DB and the ledger — memory holds the *distillation*.
3. **One writer per file.** Custody law; no shared-write files between agents.
4. **Write-down doctrine:** if it matters, it leaves the context window for a file BEFORE compaction takes the window. Memory lives outside the head or it doesn't live.
5. **Falsifications ledgered like wins.** The ledger has a falsifications column; use it on yourself first.
6. **Append-only for ledgers; overwrite-in-place for standing files** (brain sheet, MARCO_SECTION) — know which kind each file is.
