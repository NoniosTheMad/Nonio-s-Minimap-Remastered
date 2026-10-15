function nonios:arena/lightning/off
function nonios:arena/reset
scoreboard players set #speed nx.arena 1
kill @e[type=husk,tag=demo.thief]
kill @e[type=frog]
function demo:build
function demo:say {m:"Arena reset: neutral nodes, time x1, lightning off, dummies and drops cleared"}
