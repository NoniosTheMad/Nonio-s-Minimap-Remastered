# (Re)generate the placeholder test map from storage nonios:map. Map reset = run this again.
# Clears the map area (blocks + non-player entities), rebuilds lobby, fields, arena and props. Nexus/walls come with the match.
function nonios:map/config
function nonios:map/gen/forceload with storage nonios:map load
# forceloaded chunks load on the next ticks: retry until they are in
execute unless loaded -48 64 156 run return run schedule function nonios:map/build 10t
execute unless loaded 48 64 44 run return run schedule function nonios:map/build 10t
execute unless loaded 0 64 0 run return run schedule function nonios:map/build 10t
function nonios:map/gen/clear with storage nonios:map area
function nonios:map/gen/lobby with storage nonios:map lobby
function nonios:map/gen/field with storage nonios:map white
function nonios:map/gen/field with storage nonios:map black
function nonios:map/gen/arena with storage nonios:map arena
function nonios:map/gen/props {t:"white"}
function nonios:map/gen/props {t:"black"}
scoreboard players set #map nx.state 1
# arena nodes from map/config (needs #map = 1 for the config hook), portal labels for the current unlocks
function nonios:map/arena_config
function nonios:arena/setup
function nonios:portal/labels
function nonios:altar/reset
scoreboard players set #dirty nx.state 0
tellraw @a[tag=nx.admin] {"text":"[map] Placeholder map rebuilt.","color":"gray"}
