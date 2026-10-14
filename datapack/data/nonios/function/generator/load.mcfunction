# Resource generators (DESIGN 2.9). A generator = marker (state) + item_display core + text_display hologram
# + interaction (right-click = collect). One schedule loop (every 20 ticks) drives all of them: no per-tick cost.
#
# API (run as + at the generator marker unless noted):
#   function nonios:generator/spawn {team:"white",lvl:1}   positioned at the spot ON TOP of the sea lantern
#                                                          (the 3x3 base replaces the 3x3 blocks two below)
#   function nonios:generator/upgrade | downgrade | reset | remove
#   function nonios:generator/set_level {lvl:N}
#   function nonios:generator/buy_upgrade                  as a player: pay #cost<N> coins, upgrade the nearest (8 blocks)
# Scores on the marker: nx.gen_lvl (1-3), nx.gen_t (game ticks to next drop), nx.gen_iv (interval), nx.gen_pot (coins
# waiting), nx.gen_cap (pot cap). Tags: nx.gen, nx.gen.<team>, nx.gen_full (item cap reached, drop on hold).
# Config: function generator/config (generated from src/generators.json), plus runtime #speed / #sim in nx.gen.
scoreboard objectives add nx.coins dummy {"text":"Coins","color":"gold"}
scoreboard objectives add nx.gen dummy
scoreboard objectives add nx.gen_lvl dummy
scoreboard objectives add nx.gen_t dummy
scoreboard objectives add nx.gen_iv dummy
scoreboard objectives add nx.gen_pot dummy
scoreboard objectives add nx.gen_cap dummy
# upgrade dialog (generator/ui): /trigger nx.genup set 1
scoreboard objectives add nx.genup trigger
function nonios:generator/config
scoreboard players set #20 nx.gen 20
scoreboard players set #45 nx.gen 45
scoreboard players set #360 nx.gen 360
# time multiplier (demo / admin): 1 = normal
execute unless score #speed nx.gen matches 1.. run scoreboard players set #speed nx.gen 1
# per-team look; merged into each generator's marker data at spawn
data modify storage nonios:gen teams set value {white:{name:"White",col:"#f0f0f0",glow:15790320},black:{name:"Black",col:"#9a9a9a",glow:4210752}}
schedule function nonios:generator/loop 20t replace
