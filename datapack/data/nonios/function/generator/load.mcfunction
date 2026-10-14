# Field generators (feedback #39, V2 style). A generator = marker (state) on top of a sea lantern + an interaction
# over its 3x3 base (right-click = upgrade dialog; it also shields the base). The block on the lantern is mined
# like any block: coins only come from the normal purse payout (emerald ore/block). Once mined, the spot stays
# empty for the level's regrow delay, then a new outcome grows (V2 odds, 1 of 81). Upgrades = shorter delay +
# better odds. One schedule loop (every 20 ticks) drives all of them.
#
# API (run as + at the generator marker unless noted):
#   function nonios:generator/spawn {team:"white",lvl:1}   positioned at the spot ON TOP of the sea lantern
#                                                          (the 3x3 base replaces the 3x3 blocks two below)
#   function nonios:generator/upgrade | downgrade | reset | remove | grow
#   function nonios:generator/set_level {lvl:N}
#   function nonios:generator/buy_upgrade                  as a player: pay #cost<N> coins, upgrade the nearest (8 blocks)
#   function nonios:generator/lucky/toggle                 lucky block proposal on/off (#lucky nx.gen)
# Scores on the marker: nx.gen_lvl (1-3), nx.gen_t (game ticks until regrowth, counts only while the spot is empty),
# nx.gen_iv (regrow delay). Tags: nx.gen, nx.gen.<team>, nx.gen_lucky (the current block is a lucky block).
# Regrowth speed: x (1 + (team players - 1) / #per_roll), x1.5 while the team holds a "regrow" capture node.
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
# lucky block: the runtime switch keeps its value across reloads; the first load takes the config default
execute unless score #lucky nx.gen matches 0..1 run scoreboard players operation #lucky nx.gen = #lucky_def nx.gen
# per-team look; merged into each generator's marker data at spawn
data modify storage nonios:gen teams set value {white:{name:"White",col:"#f0f0f0"},black:{name:"Black",col:"#9a9a9a"}}
schedule function nonios:generator/loop 20t replace
