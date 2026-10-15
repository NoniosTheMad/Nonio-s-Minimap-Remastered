# as a player: the interest mode picker (#110). Body: match minute, your team bank, each mode's rate there now
# (coins/s) and a 1-minute projection (x 60, the clock held). Buttons, fixed: modes A B C Refresh / clock 0 10 20 30 min /
# bank 500 2000 10000, +60 s interest / clock 40 50 60 90 min. Clock buttons greyed outside a match, bank buttons without a team.
function nonios:economy/rate
# talisman (#112): talisman_mult x live rate x its price -> 1/1000 coin per s = v x ppm x 1000000 / idiv / (period x 1000)
execute store result score #dv nx.eco run data get storage nonios:shop items[{name:"Emerald Talisman"}].price
execute unless score #dv nx.eco matches 1.. run scoreboard players set #dv nx.eco 200
execute store result storage demo:im tv int 1 run scoreboard players get #dv nx.eco
execute store result score #dk nx.eco run data get storage nonios:config talisman_mult
execute store result storage demo:im tm int 1 run scoreboard players get #dk nx.eco
scoreboard players operation #dv nx.eco *= #dk nx.eco
scoreboard players operation #dv nx.eco *= #ppm nx.eco
scoreboard players operation #dv nx.eco /= #iper nx.eco
scoreboard players operation #dk nx.eco = #idiv nx.eco
scoreboard players operation #dk nx.eco /= #1000 nx.eco
scoreboard players operation #dv nx.eco /= #dk nx.eco
scoreboard players operation #dtl nx.eco = #dv nx.eco
scoreboard players set #db nx.eco 0
execute if entity @s[team=white] run scoreboard players operation #db nx.eco = #white nx.bank
execute if entity @s[team=black] run scoreboard players operation #db nx.eco = #black nx.bank
data modify storage demo:im a set value {team:"No team:",pA:"   ",pB:"   ",pC:"   ",cA:"gray",cB:"gray",cC:"gray"}
execute if entity @s[team=white] run data modify storage demo:im a.team set value "White bank"
execute if entity @s[team=black] run data modify storage demo:im a.team set value "Black bank"
execute store result storage demo:im a.b int 1 run scoreboard players get #db nx.eco
execute store result storage demo:im a.m int 1 run scoreboard players get #emin nx.eco
execute store result storage demo:im a.sec int 1 run scoreboard players get #esec nx.eco
execute if score #imode nx.eco matches 1 run data modify storage demo:im a merge value {pA:"✔ ",cA:"green"}
execute if score #imode nx.eco matches 2 run data modify storage demo:im a merge value {pB:"✔ ",cB:"green"}
execute if score #imode nx.eco matches 3 run data modify storage demo:im a merge value {pC:"✔ ",cC:"green"}
# the curves at the clock (this clobbers the live #ppm: #rsec -1 makes the next interest tick recompute)
scoreboard players operation #ct nx.eco = #esec nx.eco
function nonios:bank/curve/eval_cap
function nonios:bank/curve/eval
scoreboard players set #rsec nx.eco -1
execute store result score #dsc nx.eco run data get storage nonios:config interest_scale
scoreboard players operation #ppm nx.eco *= #dsc nx.eco
scoreboard players operation #ppm nx.eco /= #100 nx.eco
execute store result score #dper nx.eco run data get storage nonios:config interest_period
execute if score #dper nx.eco matches ..0 run scoreboard players set #dper nx.eco 1
execute if score #dper nx.eco matches 101.. run scoreboard players set #dper nx.eco 100
scoreboard players operation #dper nx.eco *= #100 nx.eco
# A: bank x rate (1/1000000 per s) -> 1/1000 coin per s, at most the cap
execute store result score #dv nx.eco run data get storage nonios:config interest_a_rate
scoreboard players operation #dv nx.eco *= #dsc nx.eco
scoreboard players operation #dv nx.eco /= #100 nx.eco
scoreboard players operation #dv nx.eco *= #db nx.eco
scoreboard players operation #dv nx.eco /= #1000 nx.eco
scoreboard players operation #dv nx.eco < #capm nx.eco
function demo:im/fmt {k:"A"}
scoreboard players operation #dv nx.eco = #capm nx.eco
function demo:im/fmt {k:"K"}
# B: every coin, curve per period -> b x (ppm / 10) / (period x 100) = 1/1000 coin per s
scoreboard players operation #dp nx.eco = #ppm nx.eco
scoreboard players operation #dp nx.eco /= #10 nx.eco
scoreboard players operation #dv nx.eco = #db nx.eco
scoreboard players operation #dv nx.eco *= #dp nx.eco
scoreboard players operation #dv nx.eco /= #dper nx.eco
function demo:im/fmt {k:"B"}
# C: at most interest_base coins
execute store result score #dbc nx.eco run data get storage nonios:config interest_base
scoreboard players operation #dbc nx.eco < #db nx.eco
scoreboard players operation #dv nx.eco = #dbc nx.eco
scoreboard players operation #dv nx.eco *= #dp nx.eco
scoreboard players operation #dv nx.eco /= #dper nx.eco
function demo:im/fmt {k:"C"}
scoreboard players operation #dv nx.eco = #dtl nx.eco
function demo:im/fmt {k:"T"}
data modify storage demo:im a.tm set from storage demo:im tm
data modify storage demo:im a.tv set from storage demo:im tv
execute store result storage demo:im a.base int 1 run data get storage nonios:config interest_base
data modify storage demo:im a.unit set from storage nonios:eco unit
data modify storage demo:im a.r set from storage nonios:eco rtxt
# buttons
data modify storage demo:im acts set value []
execute if score #imode nx.eco matches 1 run function demo:im/btn {n:21,lab:"✔ A",tip:"(recommended) Flat 0.1%/s on the bank, but at most a cap that grows with the match clock: 0 at the start, 1/s at min 10, 5/s at 20, 20/s at 30, 35/s at 40, 50/s at 50, then +1/s every minute. The game default."}
execute unless score #imode nx.eco matches 1 run function demo:im/btn {n:21,lab:"A",tip:"(recommended) Flat 0.1%/s on the bank, but at most a cap that grows with the match clock: 0 at the start, 1/s at min 10, 5/s at 20, 20/s at 30, 35/s at 40, 50/s at 50, then +1/s every minute. The game default."}
execute if score #imode nx.eco matches 2 run function demo:im/btn {n:22,lab:"✔ B",tip:"Per-minute curve as now: 0% at the start, 0.5% at min 10, 1% at min 20, 2%/min from min 30. Every banked coin earns (no 2000 limit). Reference only."}
execute unless score #imode nx.eco matches 2 run function demo:im/btn {n:22,lab:"B",tip:"Per-minute curve as now: 0% at the start, 0.5% at min 10, 1% at min 20, 2%/min from min 30. Every banked coin earns (no 2000 limit). Reference only."}
execute if score #imode nx.eco matches 3 run function demo:im/btn {n:23,lab:"✔ C",tip:"The #108 version: the same per-minute curve, but only the first 2000 banked coins earn. Reference only."}
execute unless score #imode nx.eco matches 3 run function demo:im/btn {n:23,lab:"C",tip:"The #108 version: the same per-minute curve, but only the first 2000 banked coins earn. Reference only."}
function demo:im/btn {n:20,lab:"Refresh",tip:"Redraw the numbers (the match clock keeps running)"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:24,lab:"0 min",tip:"Match clock to 0:00"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:25,lab:"10 min",tip:"Match clock to 10:00"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:26,lab:"20 min",tip:"Match clock to 20:00"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:27,lab:"30 min",tip:"Match clock to 30:00"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"0 min",tip:"Start a match first"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"10 min",tip:"Start a match first"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"20 min",tip:"Start a match first"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"30 min",tip:"Start a match first"}
execute if entity @s[team=!white,team=!black] run function demo:im/off {lab:"Bank 500",tip:"Join a team first"}
execute if entity @s[team=!white,team=!black] run function demo:im/off {lab:"Bank 2000",tip:"Join a team first"}
execute if entity @s[team=!white,team=!black] run function demo:im/off {lab:"Bank 10000",tip:"Join a team first"}
execute unless entity @s[team=!white,team=!black] run function demo:im/btn {n:28,lab:"Bank 500",tip:"Your team bank = 500"}
execute unless entity @s[team=!white,team=!black] run function demo:im/btn {n:29,lab:"Bank 2000",tip:"Your team bank = 2000"}
execute unless entity @s[team=!white,team=!black] run function demo:im/btn {n:30,lab:"Bank 10000",tip:"Your team bank = 10000"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:31,lab:"+60 s",tip:"Pay one minute of interest now (live mode), then redraw"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"+60 s",tip:"Start a match first"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:33,lab:"40 min",tip:"Match clock to 40:00"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:34,lab:"50 min",tip:"Match clock to 50:00"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:35,lab:"60 min",tip:"Match clock to 60:00"}
execute if score #state nx.state matches 1..2 run function demo:im/btn {n:36,lab:"90 min",tip:"Match clock to 90:00"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"40 min",tip:"Start a match first"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"50 min",tip:"Start a match first"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"60 min",tip:"Start a match first"}
execute unless score #state nx.state matches 1..2 run function demo:im/off {lab:"90 min",tip:"Start a match first"}
data modify storage demo:im a.acts set from storage demo:im acts
function demo:im/show with storage demo:im a
