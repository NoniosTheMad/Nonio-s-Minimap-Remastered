# advancement reward: runs as the victim at the moment of death (only when something gets kill credit)
advancement revoke @s only nonios:purse/killed
execute unless score @s nx.coins matches 1.. run return 0
tag @s add nx.victim
scoreboard players operation #purse nx.purse = @s nx.coins
# killer = a player, or any entity tagged nx.purse_holder (e.g. the demo's Purse Thief). Anything else: death/died drops a coin bag.
execute on attacker unless entity @s[tag=nx.victim] if entity @s[type=player] run function nonios:purse/death/take
execute on attacker unless entity @s[tag=nx.victim] if entity @s[tag=nx.purse_holder,type=!player] run function nonios:purse/death/take
tag @s remove nx.victim
