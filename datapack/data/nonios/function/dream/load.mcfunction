# Emerald Dream: custom dimension nonios:emerald_dream (floating emerald islands).
# Enter: nonios:dream/enter (ungated) or nonios:dream/try_enter (runs the #nonios:dream/gate hook first).
# Exit: sneak for #channel_ticks; taking damage or releasing sneak cancels. Regrowing ore veins = markers tagged nx.dream_vein.
scoreboard objectives add nx.dream dummy
scoreboard objectives add nx.coins dummy
scoreboard objectives add nx.pid dummy
scoreboard objectives add nx.dch dummy
scoreboard objectives add nx.drol dummy
scoreboard objectives add nx.dtry dummy
scoreboard objectives add nx.dvt dummy
scoreboard objectives add nx.dvs dummy
scoreboard objectives add nx.dhit minecraft.custom:minecraft.damage_taken
scoreboard objectives add nx.dabs minecraft.custom:minecraft.damage_absorbed

# --- config (fake players in nx.dream; only set when missing so tweaks survive /reload) ---
# exit channel length in ticks (100 = 5 s)
execute unless score #channel_ticks nx.dream = #channel_ticks nx.dream run scoreboard players set #channel_ticks nx.dream 100
# a mined vein regrows after this many ticks (600 = 30 s)
execute unless score #regrow_ticks nx.dream = #regrow_ticks nx.dream run scoreboard players set #regrow_ticks nx.dream 600
# arrival points are random in [-range, range] on x and z
execute unless score #range nx.dream = #range nx.dream run scoreboard players set #range nx.dream 3000
# regrowing veins planted around each arrival point, and how far from it
execute unless score #veins nx.dream = #veins nx.dream run scoreboard players set #veins nx.dream 10
execute unless score #vein_r nx.dream = #vein_r nx.dream run scoreboard players set #vein_r nx.dream 9
# veins with nobody within 64 blocks for this many ticks are forgotten (block stays as is). 6000 = 5 min
execute unless score #ttl nx.dream = #ttl nx.dream run scoreboard players set #ttl nx.dream 6000
# lowest y an arrival may land on
execute unless score #land_min_y nx.dream = #land_min_y nx.dream run scoreboard players set #land_min_y nx.dream 24

scoreboard players set #2 nx.dream 2
scoreboard players set #5 nx.dream 5
scoreboard players set #20 nx.dream 20
scoreboard players set #30 nx.dream 30
scoreboard players set #150 nx.dream 150
data modify storage nonios:dream bar.full set value "||||||||||||||||||||||||||||||"
# fallback landing pad (if the dream can't find ground for a long time) lives at 0 0 in the dream
execute in nonios:emerald_dream run forceload add 0 0
