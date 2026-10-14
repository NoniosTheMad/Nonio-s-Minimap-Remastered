# A team loses when its Nexus is destroyed (#<team> nx.last = 1) and nobody of it is left alive.
# "Alive" = online non-spectator players + test dummies (husks tagged nx.dummy on the team).
# Runs on death events (eliminated, nexus_lost, dummy_killed) and once per second in battle as a safety net.
execute unless score #state nx.state matches 2 run return 0
execute store result score #wa nx.tmp if entity @a[team=white,gamemode=!spectator]
execute store result score #t nx.tmp if entity @e[type=husk,tag=nx.dummy,team=white]
scoreboard players operation #wa nx.tmp += #t nx.tmp
execute store result score #ba nx.tmp if entity @a[team=black,gamemode=!spectator]
execute store result score #t nx.tmp if entity @e[type=husk,tag=nx.dummy,team=black]
scoreboard players operation #ba nx.tmp += #t nx.tmp
scoreboard players set #wout nx.tmp 0
scoreboard players set #bout nx.tmp 0
execute if score #white nx.last matches 1 if score #wa nx.tmp matches 0 run scoreboard players set #wout nx.tmp 1
execute if score #black nx.last matches 1 if score #ba nx.tmp matches 0 run scoreboard players set #bout nx.tmp 1
execute if score #wout nx.tmp matches 1 if score #bout nx.tmp matches 1 run return run function nonios:game/end/draw
execute if score #wout nx.tmp matches 1 run return run function nonios:game/end/win {team:"black",Team:"BLACK",loser:"white"}
execute if score #bout nx.tmp matches 1 run return run function nonios:game/end/win {team:"white",Team:"WHITE",loser:"black"}
