-- stub_env.lua — auto-stub DCS scripting environment for load-time testing.
-- Doctrine: NOT a simulator. A tripwire. Every missing DCS global becomes a
-- self-documenting stub object that is indexable AND callable, and every call
-- is recorded so we can report exactly what the framework touched.
-- Findings are the product: LOAD FAILED <error> = first engine dependency at
-- definition time; full load = MOOSE definitions are engine-free.

STUB_CALLS = {}
STUB_DEPTH = 0

-- Globals the DCS mission environment provides as STRINGS before the bundle
-- loads (include-path prefixes etc). Pre-seeded, not auto-stubbed.
PRESEED = {
	MOOSE_DEVELOPMENT_FOLDER = "./",
	MOOSE_INCLUDE_FOLDER = "./",
}

-- Real tables DCS provides that MOOSE performs ARITHMETIC on at definition
-- time: the event enum. Values are stub-consistent integers; only internal
-- consistency matters for a load-time tripwire.
local S_EVENTS = { "S_EVENT_BIRTH", "S_EVENT_CRASH", "S_EVENT_DEAD", "S_EVENT_HIT",
	"S_EVENT_EJECTION", "S_EVENT_LAND", "S_EVENT_TAKEOFF", "S_EVENT_KILL",
	"S_EVENT_MISSION_END", "S_EVENT_MISSION_RESTART", "S_EVENT_BASE_CAPTURED",
	"S_EVENT_BDA", "S_EVENT_DAYNIGHT", "S_EVENT_AI_ABORT_MISSION",
	"S_EVENT_DETAILED_FAILURE", "S_EVENT_ENGINE_STARTUP", "S_EVENT_ENGINE_SHUTDOWN",
	"S_EVENT_FLIGHT_TIME", "S_EVENT_HUMAN_FAILURE", "S_EVENT_HUMAN_AIRCRAFT_REPAIR_START",
	"S_EVENT_HUMAN_AIRCRAFT_REPAIR_FINISH", "S_EVENT_LANDING_AFTER_EJECTION",
	"S_EVENT_LANDING_QUALITYMARK", "S_EVENT_LANDING_QUALITY_MARK",
	"S_EVENT_DISCARD_CHAIR_AFTER_EJECTION", "S_EVENT_DYNAMIC_CARGO_LOADED",
	"S_EVENT_DYNAMIC_CARGO_REMOVED", "S_EVENT_DYNAMIC_CARGO_UNLOADED",
	"S_EVENT_EMERGENCY_LANDING", "S_EVENT_MARK_ADDED", "S_EVENT_MARK_CHANGE",
	"S_EVENT_MARK_REMOVED", "S_EVENT_MAC_EXTRA_SCORE", "S_EVENT_MAC_EXTRA_SCOREP",
	"S_EVENT_MAC_LMS_RESTART", "S_EVENT_MAC_SUBTASK_SCORE", "S_EVENT_SHOOT",
	"S_EVENT_SHOT", "S_EVENT_HIT_ANGLE", "S_EVENT_PLAYER_ENTER_UNIT",
	"S_EVENT_PLAYER_LEAVE_UNIT", "S_EVENT_REFUELING", "S_EVENT_REFUELING_STOP",
	"S_EVENT_TOOK_CONTROL", "S_EVENT_TURNED_WHEEL", "S_EVENT_UNIT_LOST",
	"S_EVENT_KILL_RESERVED" }
local WEV = { S_EVENT_MAX = 9000 }
local wev_mt = {
	__index = function(tbl, key)
		if type(key) == "string" and key:match("^S_EVENT_[%w_]+$") then
			local nextval = (rawget(tbl, "_next") or 100)
			rawset(tbl, "_next", nextval + 1)
			rawset(tbl, key, nextval)
			return nextval
		end
		return nil
	end,
}
setmetatable(WEV, wev_mt)
for i, name in ipairs(S_EVENTS) do WEV[name] = i end
world = { event = WEV,
	addEventHandler = function(h) STUB_CALLS[#STUB_CALLS+1] = "world.addEventHandler"; return h end,
	removeEventHandler = function(h) return true end,
	getAirbases = function() return {} end,
	getSceneObjects = function() return {} end,
	searchObjects = function() return {} end,
	getPitchBankRoll = function() return 0, 0, 0 end,
}
coalition = {
	side = { NEUTRAL = 0, RED = 1, BLUE = 2 }, -- real enum table, indexed at load time
	addStaticObject = function() return true end,
	getStaticObjects = function() return {} end,
	getGroups = function() return {} end,
	getPlayers = function() return {} end,
	addGroup = function() return nil end,
}

-- lfs: LuaFileSystem, desanitized by DCS. MOOSE nil-guards it, but code that
-- runs at load time needs writedir() to return a real string. Honest minimal.
lfs = {
	writedir = function() return "./" end,
	tempdir = function() return "./" end,
	currentdir = function() return "./" end,
	dir = function() return function() return nil end end,
	attributes = function() return nil end,
	mkdir = function() return true end,
}

-- timer: the scheduling engine. Fixed clock + recording scheduler: a smoke
-- harness must be deterministic, so getTime returns a constant.
timer = setmetatable({ getTime = function()
	STUB_CALLS[#STUB_CALLS + 1] = "timer.getTime"
	return 6000.0
end }, {
	__index = function(t, k)
		if k == "scheduleFunction" then
			local f = function(fn, args, when)
				STUB_CALLS[#STUB_CALLS + 1] = "timer.scheduleFunction"
				return 0 -- fake ScheduleID
			end
			rawset(t, k, f)
			return f
		end
		if k == "scheduleFunctionFixed" then return t.scheduleFunction end
	end,
})

local function auto(name)
	local t = {}
	setmetatable(t, {
		__index = function(tt, k)
			if type(k) ~= "string" then return nil end
			local nt = auto(name .. "." .. k)
			rawset(tt, k, nt)
			return nt
		end,
		__call = function(self, ...)
			STUB_CALLS[#STUB_CALLS + 1] = name
			return nil
		end,
		__tostring = function() return "<stub:" .. name .. ">" end,
	})
	return t
end

setmetatable(_G, {
	__index = function(g, name)
		local pre = PRESEED[name]
		if pre ~= nil then rawset(g, name, pre); return pre end
		if STUB_DEPTH > 0 then return nil end -- real errors stay real inside stubs
		STUB_DEPTH = STUB_DEPTH + 1
		local t = auto(tostring(name))
		rawset(g, name, t)
		STUB_DEPTH = STUB_DEPTH - 1
		return t
	end,
})

print("[stub_env] auto-stub DCS environment active (every global = recorder)")
