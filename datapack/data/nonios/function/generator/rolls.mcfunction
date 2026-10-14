# as + at a generator marker; macro $(team), $(lvl). Rolls #left times.
$function nonios:generator/roll/$(team)_lvl$(lvl)
scoreboard players remove #left nx.gen 1
$execute if score #left nx.gen matches 1.. run function nonios:generator/rolls {team:"$(team)",lvl:$(lvl)}
