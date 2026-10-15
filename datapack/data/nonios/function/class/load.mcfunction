# Class framework (DESIGN 2.12): objectives + defaults. Called from nonios:load.
# Definitions: src/classes.json -> python tools/build_classes.py -> class/gen/**, loot_table/class/**, enchantment/class/**.
# current class number (0/unset = none) and the chosen basic class (re-applied on respawn)
scoreboard objectives add nx.class dummy
scoreboard objectives add nx.cls_basic dummy
# argument for class/gen/apply
scoreboard objectives add nx.cls_req dummy
# basic-class upgrade level per team (1-3): #white #black #solo (players without a team)
scoreboard objectives add nx.cls_lvl dummy
# victim tier for the kill bonus (economy kill_bonus/tier reads it): owned by classes, set on apply, 0 without a class
scoreboard objectives add nx.tier dummy
scoreboard objectives add nx.cls_tmp dummy
# Reaper souls / lifesteal gate (gametime of the last heal)
scoreboard objectives add nx.cls_souls dummy
scoreboard objectives add nx.cls_bid dummy
scoreboard objectives add nx.cls_bnd dummy
scoreboard objectives add nx.food food
scoreboard objectives add nx.cls_heal dummy
# Reaper: untouchable-until gametime, last "No souls" tick, flight state (1 = in the air), last 2 heights (milliblocks), gravity sent
scoreboard objectives add nx.cls_ward dummy
scoreboard objectives add nx.cls_nos dummy
# last game tick a cooldown item (goat-horn based, build_classes _horn) was held up
scoreboard objectives add nx.cls_use dummy
# Miner ore sense ticks left (miner/spel_*)
scoreboard objectives add nx.cls_spel dummy
scoreboard players set #3 nx.cls_tmp 3
scoreboard objectives add nx.cls_rfly dummy
scoreboard objectives add nx.cls_ry1 dummy
scoreboard objectives add nx.cls_ry2 dummy
scoreboard objectives add nx.cls_rg dummy
# Berserker: Rage tier 0..4 (berserker/fury)
scoreboard objectives add nx.cls_blvl dummy
# Berserker heal guard (#89): last allowed health x100, ticks left on the max-health clamp
scoreboard objectives add nx.cls_bhp dummy
scoreboard objectives add nx.cls_bcap dummy
scoreboard objectives add nx.cls_bgr dummy
scoreboard objectives add nx.cls_bgt dummy
# Berserker Rage 0..100 (#93), last combat / last fed hit (gametime)
scoreboard objectives add nx.cls_brg dummy
scoreboard objectives add nx.cls_brt dummy
scoreboard objectives add nx.cls_brh dummy
scoreboard players set #5 nx.cls_tmp 5
scoreboard players set #25 nx.cls_tmp 25
scoreboard players set #50 nx.cls_tmp 50
scoreboard players set #100 nx.cls_tmp 100
# Angel (#94): beam ticks left, locked on (0/1), wave age; on the beamed ally: the Angel's nx.pid
scoreboard objectives add nx.cls_abm dummy
scoreboard objectives add nx.cls_alk dummy
scoreboard objectives add nx.cls_aw dummy
scoreboard objectives add nx.cls_atg dummy
scoreboard players set #4 nx.cls_tmp 4
# Champion: kills while undefeated (0..5)
scoreboard objectives add nx.cls_champ dummy
# Cracy Frog tongue: ticks left in flight, spring countdown; victims: ticks yanked / immune, launch Y and peak Y (x10). nx.pid = player id (dream/pid)
scoreboard objectives add nx.pid dummy
scoreboard objectives add nx.cls_tng dummy
scoreboard objectives add nx.cls_leap dummy
scoreboard objectives add nx.cls_yk dummy
scoreboard objectives add nx.cls_y0 dummy
scoreboard objectives add nx.cls_ypk dummy
# Cracy Frog broom: fuel (ticks), >0 while right-click is held, forward-impulse gate read by the frog_broom enchantment
scoreboard objectives add nx.cls_fuel dummy
scoreboard objectives add nx.cls_fly dummy
scoreboard objectives add nx.cls_kick dummy
# Archer quiver timer (seconds), Balrog trail marker life (ticks)
scoreboard objectives add nx.cls_quiv dummy
scoreboard objectives add nx.cls_ttl dummy
# a consumable class item was used up (survival): give it back next tick
scoreboard objectives add nx.cls_restock dummy
# 1 = class items are given with the alternate cooldown group (demo "reset cooldowns")
scoreboard objectives add nx.cls_cdalt dummy
# rejoin detection (post effects are client state, lost on reconnect)
scoreboard objectives add nx.cls_left minecraft.custom:minecraft.leave_game
# Cracy Frog confirmation chain (dialog buttons) + the step each player reached
scoreboard objectives add nx.cls_ask trigger
scoreboard objectives add nx.cls_askst dummy
execute unless score #white nx.cls_lvl matches 1.. run scoreboard players set #white nx.cls_lvl 1
execute unless score #black nx.cls_lvl matches 1.. run scoreboard players set #black nx.cls_lvl 1
execute unless score #solo nx.cls_lvl matches 1.. run scoreboard players set #solo nx.cls_lvl 1
scoreboard players set #6 nx.cls_tmp 6
scoreboard players set #2 nx.cls_tmp 2
scoreboard players set #10 nx.cls_tmp 10
function nonios:class/gen/catalog
