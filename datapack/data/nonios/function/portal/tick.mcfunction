# unlock dialog clicks (/trigger: permission 0). The handler resets only the triggerer; enable @a last.
execute as @a[scores={nx.portal_t=1..}] at @s run function nonios:portal/act
scoreboard players enable @a nx.portal_t
execute unless score #map nx.state matches 1 run return 0
# pads: act once per step onto the frame (tag nx.on_pad until they step off)
execute as @a[tag=nx.on_pad] at @s unless block ~ ~-0.3 ~ minecraft:end_portal_frame run tag @s remove nx.on_pad
execute as @a[tag=!nx.on_pad,gamemode=!spectator] at @s if dimension minecraft:overworld if block ~ ~-0.3 ~ minecraft:end_portal_frame run function nonios:portal/step
