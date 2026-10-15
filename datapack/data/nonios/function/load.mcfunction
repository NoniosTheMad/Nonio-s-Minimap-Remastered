# One load for the whole game pack: each subsystem sets up its own objectives/config.
scoreboard objectives add nx.state dummy
scoreboard objectives add nx.const dummy
scoreboard objectives add nx.tmp dummy
function nonios:nexus/load
function nonios:shop/load
function nonios:purse/load
function nonios:game/load
function nonios:economy/load
function nonios:generator/load
function nonios:dream/load
function nonios:arena/load
function nonios:portal/load
function nonios:class/load
function nonios:altar/load
function nonios:guard/load
function nonios:talisman/load
