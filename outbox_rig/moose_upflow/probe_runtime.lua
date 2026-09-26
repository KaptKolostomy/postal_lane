-- probe_runtime.lua — can MOOSE methods actually RUN (not just define)?
-- Run: lua54.exe probe_runtime.lua <path-to-Moose.lua>
dofile("stub_env.lua")
local moose = arg[1] or "Moose.lua"
local ok, err = pcall(dofile, moose)
if not ok then print("bundle load failed: " .. tostring(err)); os.exit(1) end

local results = {}
local function try(name, fn)
	local ok2, r = pcall(fn)
	results[#results + 1] = { name = name, ok = ok2, r = r }
end

-- Pure-math candidates: zone geometry needs no engine state.
-- NOTE: DCS Vec2 = {x, y} (y is the horizontal z-axis). ZONE_RADIUS:New does
-- NOT validate the shape — passing {x, z} fails later in IsVec2InZone. That
-- gotcha goes straight into the cookbook's "Common mistakes".
try("ZONE_RADIUS:New(name,vec2,r,noReg)", function()
	local z = ZONE_RADIUS:New("ProbeZone", { x = 0, y = 0 }, 1000, true) -- DoNotRegisterZone: no dispatcher
	return type(z)
end)
try("ZONE_RADIUS:GetRadius", function()
	local z = ZONE_RADIUS:New("ProbeZone", { x = 0, y = 0 }, 1000, true)
	return z:GetRadius()
end)
try("ZONE_RADIUS:IsVec2InZone (inside)", function()
	local z = ZONE_RADIUS:New("ProbeZone", { x = 0, y = 0 }, 1000, true)
	return tostring(z:IsVec2InZone({ x = 50, y = 50 }))
end)
try("ZONE_RADIUS:IsVec2InZone (outside)", function()
	local z = ZONE_RADIUS:New("ProbeZone", { x = 0, y = 0 }, 1000, true)
	return tostring(z:IsVec2InZone({ x = 5000, y = 0 }))
end)
-- Constructor-only candidates: object creation, no engine behavior expected.
-- SPAWN:New fails BY DESIGN without a mission (MOOSE's own fail-closed error:
-- "There is no group declared in the mission editor") — documented, not a bug.
try("SCHEDULER:New(obj,fn,args,t0)", function()
	local s = SCHEDULER:New({}, function() end, {}, 1, 2, 0, 10)
	return type(s)
end)
try("ZONE:New(name,vec2)", function()
	local z = ZONE:New("PZ", { x = 1, z = 1 })
	return type(z)
end)

local pass = 0
for _, r in ipairs(results) do
	local line
	if r.ok then
		pass = pass + 1
		line = string.format("RUN OK   %-34s -> %s", r.name, tostring(r.r))
	else
		line = string.format("RUN ERR  %-34s -> %s", r.name, tostring(r.r):sub(1, 90))
	end
	print(line)
end
print(string.format("\nruntime probe: %d/%d calls executed", pass, #results))
print("engine stubs touched in total: " .. #STUB_CALLS)
