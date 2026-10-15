# #bw nx.eco coins requested -> must fit in the team bank (a preset larger than the bank is greyed in the dialog;
# a stale click is refused, not shrunk); #b -> purse (carried again: slows you, lost if you are killed)
execute if score #bw nx.eco matches ..0 run return run playsound minecraft:block.vault.reject_rewarded_player player @s ~ ~ ~ 1 1
execute if score #bw nx.eco > #b nx.eco run return run playsound minecraft:block.vault.reject_rewarded_player player @s ~ ~ ~ 1 1
scoreboard players operation #b nx.eco -= #bw nx.eco
scoreboard players operation @s nx.coins += #bw nx.eco
# not income (purse/changed counts purse increases as earned, for the money scale)
scoreboard players operation @s nx.earned -= #bw nx.eco
scoreboard players operation #amt nx.eco = #bw nx.eco
execute at @s run playsound minecraft:block.vault.eject_item player @s ~ ~ ~ 1 1.1
execute at @s run playsound minecraft:block.chain.break player @s ~ ~ ~ 0.6 1.2
# teammates: actionbar (repeated clicks would flood the chat)
tag @s add nx.bk.me
execute if entity @s[team=white] run title @a[team=white,tag=!nx.bk.me] actionbar [{"selector":"@s"},{"text":" took ","color":"gray"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"yellow"},{"text":" from the bank  (","color":"gray"},{"score":{"name":"#b","objective":"nx.eco"},"color":"gold"},{"text":")","color":"gray"}]
execute if entity @s[team=black] run title @a[team=black,tag=!nx.bk.me] actionbar [{"selector":"@s"},{"text":" took ","color":"gray"},{"score":{"name":"#amt","objective":"nx.eco"},"color":"yellow"},{"text":" from the bank  (","color":"gray"},{"score":{"name":"#b","objective":"nx.eco"},"color":"gold"},{"text":")","color":"gray"}]
tag @s remove nx.bk.me
