# as a held interest node: real seconds to the next payout = ceil(t / (20 x speed)) -> h.l3 "<bonus> · Ns"
scoreboard players operation #div nx.arena = #speed nx.arena
scoreboard players operation #div nx.arena *= #20 nx.arena
scoreboard players operation #sec nx.arena = @s nx.ar_t
scoreboard players operation #sec nx.arena += #div nx.arena
scoreboard players remove #sec nx.arena 1
scoreboard players operation #sec nx.arena /= #div nx.arena
execute store result storage nonios:arena h.sec int 1 run scoreboard players get #sec nx.arena
function nonios:arena/node/holo_pay_m with storage nonios:arena h
