# Emerald Dream: custom dimension nonios:emerald_dream (floating emerald islands).
# Enter: nonios:dream/enter (ungated) or nonios:dream/try_enter (runs the #nonios:dream/gate hook first).
# Exit: sneak for #channel_ticks on foot; taking damage or releasing sneak cancels.
# v3: exploration sites (dream/site, templates from tools/build_dream.py) appear in a cell grid as dreamers come near;
# their deposits are regrowing ore veins (markers nx.dream_vein) that sometimes spread. Dream Wings (dream/wings) glide
# on any chestplate in the Dream and boost on jump; the void under the islands catches you (dream/void); a pixie shop
# follows each dreamer (dream/pixie); animals carry emerald loot (dream/fauna); one nightmare site per world (dream/nightmare).
scoreboard objectives add nx.dream dummy
scoreboard objectives add nx.coins dummy
scoreboard objectives add nx.pid dummy
scoreboard objectives add nx.dch dummy
scoreboard objectives add nx.drol dummy
scoreboard objectives add nx.dtry dummy
scoreboard objectives add nx.dvt dummy
scoreboard objectives add nx.dvs dummy
scoreboard objectives add nx.dboost dummy
scoreboard objectives add nx.dchg dummy
scoreboard objectives add nx.dgx dummy
scoreboard objectives add nx.dgy dummy
scoreboard objectives add nx.dgz dummy
scoreboard objectives add nx.dgok dummy
scoreboard objectives add nx.dhit minecraft.custom:minecraft.damage_taken
scoreboard objectives add nx.dabs minecraft.custom:minecraft.damage_absorbed

# --- config (fake players in nx.dream; only set when missing so tweaks survive /reload) ---
# #cfg_v = config version: bump it (and the check below) to push changed defaults onto existing servers
execute unless score #cfg_v nx.dream matches 3.. run scoreboard players reset #channel_ticks nx.dream
scoreboard players set #cfg_v nx.dream 3
# exit channel length in ticks (200 = 10 s)
execute unless score #channel_ticks nx.dream = #channel_ticks nx.dream run scoreboard players set #channel_ticks nx.dream 200
# a mined vein regrows after this many ticks (600 = 30 s)
execute unless score #regrow_ticks nx.dream = #regrow_ticks nx.dream run scoreboard players set #regrow_ticks nx.dream 600
# arrival points are random in [-range, range] on x and z
execute unless score #range nx.dream = #range nx.dream run scoreboard players set #range nx.dream 3000
# Dream Wings: a boost costs #wing_cost charge (1 per tick to refill), #wing_max = full, a boost pushes for #wing_ticks
execute unless score #wing_cost nx.dream = #wing_cost nx.dream run scoreboard players set #wing_cost nx.dream 60
execute unless score #wing_max nx.dream = #wing_max nx.dream run scoreboard players set #wing_max nx.dream 180
execute unless score #wing_ticks nx.dream = #wing_ticks nx.dream run scoreboard players set #wing_ticks nx.dream 12
# sites: tier odds in percent per grid cell (the rest = the nightmare, once per world)
execute unless score #p_none nx.dream = #p_none nx.dream run scoreboard players set #p_none nx.dream 30
execute unless score #p_minor nx.dream = #p_minor nx.dream run scoreboard players set #p_minor nx.dream 45
execute unless score #p_major nx.dream = #p_major nx.dream run scoreboard players set #p_major nx.dream 18
execute unless score #p_grand nx.dream = #p_grand nx.dream run scoreboard players set #p_grand nx.dream 6
# deposits: % chance a mined vein spreads into a neighbouring block; max veins within 6 blocks
execute unless score #spread_pct nx.dream = #spread_pct nx.dream run scoreboard players set #spread_pct nx.dream 25
execute unless score #deposit_cap nx.dream = #deposit_cap nx.dream run scoreboard players set #deposit_cap nx.dream 10
# animals: % that gleam (glowing, bigger, ~6x loot, Dream Key chance)
execute unless score #gleam_pct nx.dream = #gleam_pct nx.dream run scoreboard players set #gleam_pct nx.dream 10
# nightmare guard posts re-arm after this many ticks with nobody within 40 blocks (6000 = 5 min)
execute unless score #guard_ticks nx.dream = #guard_ticks nx.dream run scoreboard players set #guard_ticks nx.dream 6000
# world seed for the site grid (set once)
execute unless score #seed nx.dream = #seed nx.dream store result score #seed nx.dream run random value 0..2000000000
# lowest y an arrival may land on
execute unless score #land_min_y nx.dream = #land_min_y nx.dream run scoreboard players set #land_min_y nx.dream 24

scoreboard players set #2 nx.dream 2
scoreboard players set #5 nx.dream 5
scoreboard players set #20 nx.dream 20
scoreboard players set #30 nx.dream 30
scoreboard players set #150 nx.dream 150
scoreboard players set #100 nx.dream 100
scoreboard players set #10 nx.dream 10
scoreboard players set #65536 nx.dream 65536
scoreboard players set #32768 nx.dream 32768
scoreboard players set #cell nx.dream 192
scoreboard players set #margin nx.dream 40
scoreboard players set #sspan nx.dream 112
scoreboard players set #reach2 nx.dream 12544
scoreboard players set #k1 nx.dream 7919
scoreboard players set #k2 nx.dream 104729
scoreboard players set #lcg_a nx.dream 1103515245
scoreboard players set #lcg_c nx.dream 12345
data modify storage nonios:dream bar.full set value "||||||||||||||||||||||||||||||"
# fallback landing pad (if the dream can't find ground for a long time) lives at 0 0 in the dream
execute in nonios:emerald_dream run forceload add 0 0
