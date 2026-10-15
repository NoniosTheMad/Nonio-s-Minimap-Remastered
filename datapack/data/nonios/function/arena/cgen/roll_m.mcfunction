# macro {lvl}: one roll (arena/cgen/roll/lvl<N>, generated), repeated #left times
$function nonios:arena/cgen/roll/lvl$(lvl)
scoreboard players remove #left nx.arena 1
$execute if score #left nx.arena matches 1.. run function nonios:arena/cgen/roll_m {lvl:$(lvl)}
