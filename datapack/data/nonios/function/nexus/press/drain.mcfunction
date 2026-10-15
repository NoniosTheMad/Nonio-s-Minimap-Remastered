# as/at the Barrier of $(team), whose enemy has held the centre for #h nx.tmp seconds. Damage per minute =
# max HP x #press_pm per mille x r^2, r = min(1, hold / #press_ramp s): quadratic ramp, so a short capture does almost
# nothing (30 s of a 300 s ramp = 1% of the full rate) and a sustained hold reaches the full rate.
# Kept as 1/60000 HP in nx.prs so small rates still add up. Blocks regen like a hit.
scoreboard players operation #r nx.tmp = #h nx.tmp
scoreboard players operation #r nx.tmp *= #1000 nx.const
scoreboard players operation #r nx.tmp /= #press_ramp nx.const
execute if score #r nx.tmp matches 1001.. run scoreboard players set #r nx.tmp 1000
scoreboard players operation #r nx.tmp *= #r nx.tmp
scoreboard players operation #r nx.tmp /= #1000 nx.const
scoreboard players operation #q nx.tmp = @s nx.hp_max
scoreboard players operation #q nx.tmp *= #r nx.tmp
scoreboard players operation #q nx.tmp /= #1000 nx.const
scoreboard players operation #q nx.tmp *= #press_pm nx.const
scoreboard players operation @s nx.prs += #q nx.tmp
scoreboard players operation #d nx.tmp = @s nx.prs
scoreboard players operation #d nx.tmp /= #60000 nx.const
execute if score #d nx.tmp matches ..0 run return 0
scoreboard players operation #q nx.tmp = #d nx.tmp
scoreboard players operation #q nx.tmp *= #60000 nx.const
scoreboard players operation @s nx.prs -= #q nx.tmp
scoreboard players operation @s nx.hp -= #d nx.tmp
scoreboard players operation @s nx.cd = #regen_delay nx.const
particle minecraft:electric_spark ~ ~0.6 ~ 0.45 0.45 0.45 0.02 3
$execute if score @s nx.hp matches ..0 run function nonios:nexus/broken {team:"$(team)"}
