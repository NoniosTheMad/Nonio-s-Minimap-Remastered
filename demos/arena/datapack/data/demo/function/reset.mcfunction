function nonios:arena/lightning/off
function nonios:arena/reset
scoreboard players set #speed nx.arena 1
scoreboard players set #bank demo.c 0
scoreboard players set White demo.bank 0
scoreboard players set Black demo.bank 0
kill @e[type=frog]
function demo:build
function demo:say {m:"Arena reset: neutral nodes, time x1, lightning off, dummies and drops cleared"}
