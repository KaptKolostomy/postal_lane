-- api_testbox.lua — DCS/MOOSE scripting engine FEEDBACK BOX (Bible P2 companion)
-- Loads: stub DCS env -> ED sandbox contract -> pinned MOOSE -> target module.
-- Captures every failure WITH A CODE. The trap-and-repair box, offline.
--
-- Usage: lua54.exe api_testbox.lua <target.lua> [moose.lua]
-- Exit codes: 0 PASS · 1 TARGET LOAD FAIL · 2 TARGET RUNTIME FAIL · 3 MOOSE LOAD FAIL · 4 HARNESS FAIL
-- Output: machine lines  TESTBOX,STAGE,CODE,detail  + human summary.
--
-- Sandbox contract: read from ED's own MissionScripting.lua if present
-- (witnessed 09-25: require/loadlib/package stripped; os/io/lfs PRESENT).
-- Fallback = conservative list. Non-fatal sandbox violations are REPORTED
-- (code SBX) — the box itself still runs the target so errors surface.

local function P(s) io.write(s .. "\n") end
local W = io.write          -- harness self-defense: capture BEFORE sandbox emulation
local EXIT = os.exit        -- (commented-out sanitizeModule lines fooled parser v1)
local function T(stage, code, detail) W(string.format("TESTBOX,%s,%s,%s\n", stage, code, tostring(detail):gsub("[,\n]", " "))) end

local target = arg[1]
if not target then
  T("HARNESS", "E", "usage: api_testbox.lua <target.lua> [moose.lua]")
  os.exit(4)
end
-- normalize: git-bash virtual paths (/e/...) -> Windows (E:/...); backslashes -> forward
local function norm(p)
  p = p:gsub("\\", "/")
  local drive = p:match("^/([a-zA-Z])/")
  if drive then p = drive:upper() .. ":/" .. p:sub(4) end
  return p
end
target = norm(target)

-- ---------- 1. stub DCS environment ----------
local ok_stub, err_stub = pcall(dofile, (os.getenv("STUB_ENV") or "stub_env.lua"))
if not ok_stub then
  T("HARNESS", "E", "stub env failed: " .. tostring(err_stub))
  os.exit(4)
end

-- ---------- 2. ED sandbox contract ----------
local MS = "B:/GAMES/Eagle Dynamics/DCS World/Scripts/MissionScripting.lua"
local contract = { stripped = {}, present = {} }
local msf = io.open(MS, "r")
if msf then
  local body = msf:read("*a"); msf:close()
  -- strip COMMENT lines first: ED keeps '--sanitizeModule('os')' as a comment;
  -- only ACTIVE statements are the real contract (witnessed 09-25)
  body = body:gsub("[\r\n]%s*%-%-[^\r\n]*", "\n")
  for name in body:gmatch("sanitizeModule%('(%w+)'%)") do contract.stripped[#contract.stripped+1] = name end
  for name in body:gmatch("_G%['(%w+)'%]%s*=%s*nil") do contract.stripped[#contract.stripped+1] = name end
else
  -- conservative fallback (older builds)
  contract.stripped = { "require", "loadlib", "package" }
end
local seenS = {}
-- HARNESS SELF-DEFENSE: read the target + keep harness-side handles BEFORE the
-- sandbox emulation strips io/os out from under us (the box runs in the same
-- Lua state as the contract it emulates).
local tf = io.open(target, "r")
if not tf then T("TARGET", "E", "cannot open " .. target); os.exit(1) end
local src = tf:read("*a"); tf:close()
for _, n in ipairs(contract.stripped) do
  seenS[n] = true
  if _G[n] ~= nil then contract[n .. "_saved"] = _G[n]; _G[n] = nil end  -- emulate ED
end
T("SANDBOX", "OK", "stripped: " .. table.concat(contract.stripped, ";"))

-- ---------- 3. load pinned MOOSE ----------
local moose = norm(arg[2] or "E:/GAMES/Saved Games/DCS/Scripts/MOOSE/Moose.lua")
local chunk = loadfile(moose)
if not chunk then T("MOOSE", "E", "loadfile failed: " .. moose); os.exit(3) end
local ok_m, err_m = pcall(chunk)
if not ok_m then T("MOOSE", "E", tostring(err_m)); os.exit(3) end
T("MOOSE", "OK", "pinned build loaded")

-- ---------- 4. sandbox AUDIT of target (pre-load, static; src pre-read) ----------
for _, pat in ipairs({ "os%.", "io%.", "lfs%.", "require%s*%(", "package%.", "net%." }) do
  if src:match(pat) then
    local name = pat:match("%a+")
    if seenS[name] then
      T("SANDBOX", "SBX-STRIPPED", name .. " used but STRIPPED by ED contract -> runtime nil error") 
    else
      T("SANDBOX", "SBX-PRESENT", name .. " used; present in current build (E11 recalibrated)")
    end
  end
end

-- ---------- 5. load + run target under full env ----------
local tc, terr = loadfile(target)
if not tc then T("TARGET", "E-LOAD", tostring(terr)); os.exit(1) end
local ok_t, err_t = pcall(tc)
if not ok_t then T("TARGET", "E-RUNTIME", tostring(err_t)); os.exit(2) end
T("TARGET", "OK", "loaded + executed under stub+sandbox+MOOSE")
print("TESTBOX RESULT: PASS")
os.exit(0)
