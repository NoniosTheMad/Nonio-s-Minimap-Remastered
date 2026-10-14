# as/at shield, every tick: crack stage from HP%, flicker when critical, back to rest pose after a pulse.
scoreboard players operation #pct nx.const = @s nx.hp
scoreboard players operation #pct nx.const *= #100 nx.const
scoreboard players operation #pct nx.const /= @s nx.hp_max
scoreboard players set #stage nx.const 0
execute if score #pct nx.const matches ..50 run scoreboard players set #stage nx.const 1
execute if score #pct nx.const matches ..25 run scoreboard players set #stage nx.const 2
execute unless score #stage nx.const = @s nx.stage run function nonios:nexus/fx/stage
execute if score @s nx.stage matches 2 if score @s nx.fx matches 0 store result score #rnd nx.const run random value 1..16
execute if score @s nx.stage matches 2 if score @s nx.fx matches 0 if score #rnd nx.const matches 1 run function nonios:nexus/fx/flicker
scoreboard players set #rnd nx.const 0
execute if score @s nx.fx matches 1 run function nonios:nexus/fx/rest
scoreboard players remove @s[scores={nx.fx=1..}] nx.fx 1
