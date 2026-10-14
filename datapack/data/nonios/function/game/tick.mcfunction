# players arriving / coming back (only once the map exists)
execute if score #map nx.state matches 1 as @a[tag=!nx.seen] run function nonios:game/join
execute if score #map nx.state matches 1 as @a[scores={nx.left=1..}] run function nonios:game/join
# dialogs (/trigger: permission 0, no op prompt). Handlers reset only the triggerer; enable @a last.
execute as @a[scores={nx.team=1..}] at @s run function nonios:team/act
execute as @a[scores={nx.admin=1..}] at @s run function nonios:admin/act
scoreboard players enable @a nx.team
scoreboard players enable @a nx.admin
# phase logic: only the current phase runs
execute if score #state nx.state matches 1 run function nonios:game/prep/tick
execute if score #state nx.state matches 2 run function nonios:game/battle/tick
execute if score #state nx.state matches 3 run function nonios:game/end/tick
