# advancement nonios:economy/kill: @s killed a player (runs inside the victim's death, same tick).
# The victim's purse goes to @s separately (purse/death/killed -> take); this only adds the kill reward, so nothing is counted twice.
# Victim = the dead player (Health 0) whose attacker is @s: works whichever of the two advancements fires first.
advancement revoke @s only nonios:economy/kill
execute unless score #state nx.state matches 1..2 run return 0
execute if entity @s[team=] run return 0
tag @s add nx.k.killer
execute as @a[tag=!nx.k.killer,tag=!nx.k.done] if function nonios:economy/kill/is_victim run tag @s add nx.k.cand
tag @a[tag=nx.k.cand,limit=1] add nx.k.v1
tag @a remove nx.k.cand
scoreboard players set #vs nx.eco 0
scoreboard players set #bonus nx.eco 0
scoreboard players set #tk nx.eco 0
execute as @a[tag=nx.k.v1] run function nonios:economy/kill/victim
execute if score #tk nx.eco matches 0 run function nonios:economy/kill/award
tag @a remove nx.k.v1
tag @s remove nx.k.killer
