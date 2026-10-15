# once a second, in the Dream: nightmare guards wake when a player comes within 20 blocks of their post,
# and their posts re-arm after #guard_ticks once nobody is within 40 blocks
execute as @e[type=marker,tag=nx.dream_guard_warden,tag=!nx.dg_spent,distance=0..] at @s if entity @a[tag=nx.in_dream,gamemode=!spectator,gamemode=!creative,distance=..20] run function nonios:dream/nightmare/wake_warden
execute as @e[type=marker,tag=nx.dream_guard_vindicator,tag=!nx.dg_spent,distance=0..] at @s if entity @a[tag=nx.in_dream,gamemode=!spectator,gamemode=!creative,distance=..20] run function nonios:dream/nightmare/wake_vindicator
execute as @e[type=marker,tag=nx.dream_guard_evoker,tag=!nx.dg_spent,distance=0..] at @s if entity @a[tag=nx.in_dream,gamemode=!spectator,gamemode=!creative,distance=..20] run function nonios:dream/nightmare/wake_evoker
execute as @e[type=marker,tag=nx.dream_guard_wither_skeleton,tag=!nx.dg_spent,distance=0..] at @s if entity @a[tag=nx.in_dream,gamemode=!spectator,gamemode=!creative,distance=..20] run function nonios:dream/nightmare/wake_wither_skeleton
execute as @e[type=marker,tag=nx.dream_guard_breeze,tag=!nx.dg_spent,distance=0..] at @s if entity @a[tag=nx.in_dream,gamemode=!spectator,gamemode=!creative,distance=..20] run function nonios:dream/nightmare/wake_breeze
execute as @e[type=marker,tag=nx.dream_guard_ravager,tag=!nx.dg_spent,distance=0..] at @s if entity @a[tag=nx.in_dream,gamemode=!spectator,gamemode=!creative,distance=..20] run function nonios:dream/nightmare/wake_ravager
execute as @e[type=marker,tag=nx.dg_spent,distance=0..] at @s if score #now nx.dream >= @s nx.dvt unless entity @a[distance=..40] run tag @s remove nx.dg_spent
execute as @e[tag=nx.dream_nm,tag=!nx.nm_buffed,distance=0..] run function nonios:dream/nightmare/buff
execute as @e[type=item_display,tag=nx.dream_exodia_fx,distance=0..] at @s run particle minecraft:sculk_soul ~ ~0.3 ~ 0.3 0.3 0.3 0.02 2
# the keep cannot be tunnelled or cheesed through its roof grille: no block breaking (or pearls) in or around it
execute as @e[type=marker,tag=nx.dream_t_nightmare,distance=0..] at @s run effect give @a[distance=..44,gamemode=survival] minecraft:mining_fatigue 3 3 true
