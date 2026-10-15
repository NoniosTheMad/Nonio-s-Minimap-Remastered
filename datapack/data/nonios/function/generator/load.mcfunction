# Field generators (feedback #39, V2 style). A generator = marker (state) on top of a sea lantern + an interaction
# over its 3x3 base (right-click = upgrade dialog; it also shields the base). The block on the lantern is mined
# like any block: coins only come from the normal purse payout (emerald ore/block). Once mined, the spot stays
# empty only for the tick it takes generator/tick to regrow it (instant, #109). Upgrades only change the pool:
# better odds per level (V2 odds, 1 of 81). One schedule loop (every 20 ticks) drives the rest.
#
# API (run as + at the generator marker unless noted):
#   function nonios:generator/spawn {team:"white",lvl:1}   positioned at the spot ON TOP of the sea lantern
#                                                          (the 3x3 base replaces the 3x3 blocks two below)
#   function nonios:generator/upgrade | downgrade | reset | remove | grow
#   function nonios:generator/set_level {lvl:N}
#   function nonios:generator/buy_upgrade                  as a player: pay #cost<N> coins, upgrade the nearest (8 blocks)
#   function nonios:generator/mode/toggle                  V2 blocks <-> single block (#single nx.gen, feedback #47)
# Scores on the marker: nx.gen_lvl (1-3), nx.gen_t (game ticks until regrowth, counts only while the spot is empty),
# nx.gen_iv (regrow delay). Tags: nx.gen, nx.gen.<team>, nx.gen_one (its single block is standing: generator/tick watches it).
# Single-block mode: one block type (src/generators.json single.block) grows every time; mined, it rolls the V2 odds as a
# loot table (generator/one/<team>_lvlN) and pays the purse yield of the outcome's V2 block (generator/one/mined).
# Default style (#109): single block. nx.gen_t / nx.gen_iv / team-size and node speed-ups no longer matter (instant regrowth).
# Config: function generator/config (generated from src/generators.json), plus runtime #speed / #sim in nx.gen.
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.gen dummy
scoreboard objectives add nx.gen_lvl dummy
scoreboard objectives add nx.gen_t dummy
scoreboard objectives add nx.gen_iv dummy
# the centre generator's coin pot (arena/cgen); also read by old demo status lines
scoreboard objectives add nx.gen_pot dummy
# upgrade dialog (generator/ui): /trigger nx.genup set 1
scoreboard objectives add nx.genup trigger
function nonios:generator/config
scoreboard players set #2 nx.gen 2
scoreboard players set #3 nx.gen 3
scoreboard players set #20 nx.gen 20
# time multiplier (demo / admin): 1 = normal
execute unless score #speed nx.gen matches 1.. run scoreboard players set #speed nx.gen 1
# style switch (#47): the runtime value keeps across reloads; the first load takes the config default
execute unless score #single nx.gen matches 0..1 run scoreboard players operation #single nx.gen = #single_def nx.gen
# #109: single block becomes the default; worlds saved before take it once (regrowing every generator in that style)
execute unless score #single_v nx.gen matches 2 run function nonios:generator/mode/default
# #109: interactions summoned before were 2 high (top face flush with the base: not clickable from above)
execute as @e[type=interaction,tag=nx.gen_click] run data merge entity @s {height:2.02f}
# the lucky block proposal is gone (#47)
scoreboard players reset #lucky nx.gen
scoreboard players reset #lucky_def nx.gen
scoreboard players reset #lucky_n nx.gen
data remove storage nonios:gen lucky
# per-team look; merged into each generator's marker data at spawn
data modify storage nonios:gen teams set value {white:{name:"White",col:"#f0f0f0"},black:{name:"Black",col:"#9a9a9a"}}
schedule function nonios:generator/loop 20t replace
