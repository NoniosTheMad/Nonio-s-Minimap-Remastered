function nonios:arena/event/mob/clear
function nonios:arena/event/frogs_despawn
scoreboard players set #ev_run nx.arena 0
scoreboard players set #ev_wait nx.arena 0
bossbar set nonios:arena/event visible false
function demo:say {m:"Events cleared"}
