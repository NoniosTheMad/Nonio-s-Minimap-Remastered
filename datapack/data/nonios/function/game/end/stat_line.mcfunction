scoreboard players add @s nx.kills 0
scoreboard players add @s nx.deaths 0
scoreboard players add @s nx.mined 0
scoreboard players add @s nx.nxdmg 0
scoreboard players add @s nx.nxkill 0
# barrier damage as % of one full barrier
scoreboard players operation @s nx.nxpct = @s nx.nxdmg
scoreboard players operation @s nx.nxpct *= #100 nx.const
scoreboard players operation @s nx.nxpct /= #barrier_max nx.const
tellraw @a [{"selector":"@s"},{"text":"  ⚔ ","color":"gray"},{"score":{"name":"@s","objective":"nx.kills"},"color":"white"},{"text":" kills  ☠ ","color":"gray"},{"score":{"name":"@s","objective":"nx.deaths"},"color":"white"},{"text":" deaths  ⛏ ","color":"gray"},{"score":{"name":"@s","objective":"nx.mined"},"color":"gold"},{"text":" coins mined  ⛨ ","color":"gray"},{"score":{"name":"@s","objective":"nx.nxpct"},"color":"aqua"},{"text":"% barrier damage","color":"gray"}]
execute if score @s nx.nxkill matches 1.. run tellraw @a [{"text":"  ★ ","color":"gold"},{"selector":"@s"},{"text":" broke the enemy Nexus","color":"gold"}]
