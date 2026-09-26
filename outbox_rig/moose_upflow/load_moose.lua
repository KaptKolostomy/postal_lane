-- load_moose.lua — experiment runner: can MOOSE *define itself* outside DCS?
-- Run: lua54.exe load_moose.lua <path-to-Moose.lua>
-- Success = framework fully defines under stubs (then we probe it).
-- Failure = the first engine dependency at definition time, reported exactly.

local moose_path = arg[1]
if not moose_path then
	print("usage: load_moose.lua <Moose.lua>")
	os.exit(1)
end

dofile(os.getenv("STUB_ENV") or "stub_env.lua") -- install auto-stub DCS globals FIRST

local t0 = os.clock()
local chunk, err = loadfile(moose_path)
if not chunk then
	print("LOAD FAILED (syntax): " .. tostring(err))
	os.exit(1)
end

local ok, run_err = pcall(chunk)
if not ok then
	print("LOAD FAILED (runtime): " .. tostring(run_err))
	print("This is the first engine dependency hit at definition time.")
	os.exit(1)
end

local dt = os.clock() - t0
print(string.format("MOOSE FULLY DEFINED in %.2fs under stub environment.", dt))

-- Probe: how much of the surface exists and is introspectable?
local probe = { "SPAWN", "SCHEDULER", "ZONE", "ZONE_RADIUS", "ZONE_POLYGON",
	"GROUP", "UNIT", "OPSGROUP", "AUFTRAG", "AIRBOSS", "WAREHOUSE", "UTILS",
	"COORDINATE", "MENU", "MESSAGE" }
local found, missing = 0, {}
for _, name in ipairs(probe) do
	if type(_G[name]) ~= "nil" then found = found + 1 else missing[#missing + 1] = name end
end
print(string.format("probe: %d/%d headline classes present", found, #probe))
if #missing > 0 then print("missing: " .. table.concat(missing, ", ")) end

-- Report what the framework touched during definition.
print("engine stubs touched at load time: " .. #STUB_CALLS)
local seen, uniq = {}, {}
for _, c in ipairs(STUB_CALLS) do
	if not seen[c] then seen[c] = true; uniq[#uniq + 1] = c end
end
table.sort(uniq)
for _, c in ipairs(uniq) do print("  touched: " .. c) end
print("EXPERIMENT: PASS")
