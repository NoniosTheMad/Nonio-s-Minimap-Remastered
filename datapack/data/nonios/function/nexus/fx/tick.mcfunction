# as/at shield, every tick: damage stage from HP%, flicker (more often when lower), back to rest pose after a pulse.
scoreboard players operation #pct nx.const = @s nx.hp
scoreboard players operation #pct nx.const *= #100 nx.const
scoreboard players operation #pct nx.const /= @s nx.hp_max
scoreboard players set #stage nx.const 0
execute if score #pct nx.const matches ..75 run scoreboard players set #stage nx.const 1
execute if score #pct nx.const matches ..50 run scoreboard players set #stage nx.const 2
execute if score #pct nx.const matches ..25 run scoreboard players set #stage nx.const 3
$execute unless score #stage nx.const = @s nx.stage run function nonios:nexus/fx/stage {team:"$(team)"}
scoreboard players set #rnd nx.const 0
execute if score @s nx.stage matches 2 if score @s nx.fx matches 0 store result score #rnd nx.const run random value 1..40
execute if score @s nx.stage matches 3 if score @s nx.fx matches 0 store result score #rnd nx.const run random value 1..8
execute if score #rnd nx.const matches 1 run function nonios:nexus/fx/flicker
execute if score @s nx.fx matches 1 run function nonios:nexus/fx/rest
scoreboard players remove @s[scores={nx.fx=1..}] nx.fx 1
