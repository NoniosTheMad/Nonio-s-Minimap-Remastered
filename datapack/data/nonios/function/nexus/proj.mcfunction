# as a projectile within 10 blocks of a Barrier, at the shield (bottom centre of the obsidian; #cx #cy #cz = the core's
# centre x100). Interaction entities can't be hit by projectiles (they fly through), so hits are found geometrically:
# this tick's move (Pos -> Pos + Motion) passes within 0.8 blocks of the core's centre = it hit the shell (the 1.4 cube
# around the obsidian); a stuck one (inGround) counts within 1 block (in the obsidian). Only enemy players' projectiles
# count; teammates' and mobs' fly through and are never looked at again.
$function nonios:nexus/proj_owner {team:"$(team)"}
execute if score #ao nx.tmp matches 0 run return run tag @s add nx.arrow_done
execute store result score #px nx.tmp run data get entity @s Pos[0] 100
execute store result score #py nx.tmp run data get entity @s Pos[1] 100
execute store result score #pz nx.tmp run data get entity @s Pos[2] 100
execute store result score #mx nx.tmp run data get entity @s Motion[0] 100
execute store result score #my nx.tmp run data get entity @s Motion[1] 100
execute store result score #mz nx.tmp run data get entity @s Motion[2] 100
execute if data entity @s {inGround:1b} run scoreboard players set #mx nx.tmp 0
execute if data entity @s {inGround:1b} run scoreboard players set #my nx.tmp 0
execute if data entity @s {inGround:1b} run scoreboard players set #mz nx.tmp 0
# D = centre - position
scoreboard players operation #dx nx.tmp = #cx nx.tmp
scoreboard players operation #dx nx.tmp -= #px nx.tmp
scoreboard players operation #dy nx.tmp = #cy nx.tmp
scoreboard players operation #dy nx.tmp -= #py nx.tmp
scoreboard players operation #dz nx.tmp = #cz nx.tmp
scoreboard players operation #dz nx.tmp -= #pz nx.tmp
function nonios:nexus/proj_seg
execute if score #mm nx.tmp matches ..99 if score #d2 nx.tmp matches ..10000 run return run function nonios:nexus/proj_hit
execute if score #d2 nx.tmp matches ..6400 run function nonios:nexus/proj_hit
