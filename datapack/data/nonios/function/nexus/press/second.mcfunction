# once a second while #on nx.nxs is 1 (battle), #48:
# (a) Centre pressure: the team holding the centre node (storage nonios:nexus press.node) drains the enemy Barrier;
#     the rate ramps with continuous hold time (press/drain). Losing the node (neutral or taken) resets the ramp.
# (b) Decay: from battle minute #decay_min each Barrier's ceiling drops #decay_pm per mille of max per minute
#     (press/decay): an undamaged Barrier breaks #decay_min + 1000/#decay_pm minutes in (20 + 10 = 30).
scoreboard players add #bsec nx.nxs 1
scoreboard players set #own nx.nxs 0
function nonios:nexus/press/owner with storage nonios:nexus press
# demo override (#sim 1 white / 2 black holds the centre)
execute if score #sim nx.nxs matches 1..2 run scoreboard players operation #own nx.nxs = #sim nx.nxs
execute unless score #own nx.nxs matches 1 run scoreboard players set #hold_white nx.nxs 0
execute unless score #own nx.nxs matches 2 run scoreboard players set #hold_black nx.nxs 0
execute if score #own nx.nxs matches 1 run scoreboard players add #hold_white nx.nxs 1
execute if score #own nx.nxs matches 2 run scoreboard players add #hold_black nx.nxs 1
scoreboard players operation #h nx.tmp = #hold_white nx.nxs
execute if score #h nx.tmp matches 1.. as @e[type=interaction,tag=nx.shield,tag=nx.black] at @s run function nonios:nexus/press/drain {team:"black"}
scoreboard players operation #h nx.tmp = #hold_black nx.nxs
execute if score #h nx.tmp matches 1.. as @e[type=interaction,tag=nx.shield,tag=nx.white] at @s run function nonios:nexus/press/drain {team:"white"}
scoreboard players operation #m nx.tmp = #decay_min nx.const
scoreboard players operation #m nx.tmp *= #60 nx.const
execute if score #bsec nx.nxs > #m nx.tmp as @e[type=interaction,tag=nx.shield,tag=nx.white] at @s run function nonios:nexus/press/decay {team:"white"}
execute if score #bsec nx.nxs > #m nx.tmp as @e[type=interaction,tag=nx.shield,tag=nx.black] at @s run function nonios:nexus/press/decay {team:"black"}
