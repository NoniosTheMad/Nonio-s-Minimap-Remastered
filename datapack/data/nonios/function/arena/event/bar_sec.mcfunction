# announced event: bossbar name "NAME  where  Ns" (real seconds = ceil(wait / (20 x speed)))
scoreboard players operation #div nx.arena = #speed nx.arena
scoreboard players operation #div nx.arena *= #20 nx.arena
scoreboard players operation #sec nx.arena = #ev_wait nx.arena
scoreboard players operation #sec nx.arena += #div nx.arena
scoreboard players remove #sec nx.arena 1
scoreboard players operation #sec nx.arena /= #div nx.arena
execute store result storage nonios:arena ev.sec int 1 run scoreboard players get #sec nx.arena
function nonios:arena/event/bar_name with storage nonios:arena ev
