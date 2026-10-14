# Nexus = obsidian core (final target) + Barrier (HP pool that protects it).
# Scores live on the shield interaction entity.
scoreboard objectives add nx.hp dummy
scoreboard objectives add nx.hp_max dummy
scoreboard objectives add nx.cd dummy
scoreboard objectives add nx.alert dummy
scoreboard objectives add nx.regen dummy
# shell visuals: nx.col team tint, nx.stage 0 ok/1 cracked/2 critical, nx.fx ticks until rest pose
scoreboard objectives add nx.col dummy
scoreboard objectives add nx.stage dummy
scoreboard objectives add nx.fx dummy
# per player: gametime of the next allowed explain message
scoreboard objectives add nx.msg_t dummy
data modify storage nonios:nexus col set value {white:11069695,black:12086271}
team add white
team modify white color white
team add black
team modify black color dark_purple
bossbar add nonios:barrier_white {"text":"White Barrier","color":"white"}
bossbar set nonios:barrier_white color white
bossbar set nonios:barrier_white style notched_10
bossbar add nonios:barrier_black {"text":"Black Barrier","color":"light_purple"}
bossbar set nonios:barrier_black color purple
bossbar set nonios:barrier_black style notched_10
# tuning (fake players on nx.const)
execute unless score #barrier_max nx.const matches 1.. run scoreboard players set #barrier_max nx.const 1000
execute unless score #regen_mult nx.const matches 1.. run scoreboard players set #regen_mult nx.const 1
execute unless score #regen_delay nx.const matches 0.. run scoreboard players set #regen_delay nx.const 200
scoreboard players set #regen_unit nx.const 24000
scoreboard players set #100 nx.const 100
