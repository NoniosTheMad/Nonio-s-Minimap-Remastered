# current interest terms from the match clock (#108): #ppm nx.eco = rate per period in parts per million (10000 = 1%),
# from the curve (bank/curve, config interest_curve) x interest_scale %. #ibase = coins of a bank that earn (interest_base),
# #ithr = 1/1000000 coin per paid coin x the period in ticks (bank/interest/team). #esec / #emin nx.eco = match seconds / minutes.
# storage nonios:eco rtxt = "0.50%/min", unit = "min" | "s" | "<n>s". Outside a match: the starting values.
# Everything about the interest lives in storage nonios:config (economy/load), so the unit is one number (interest_period).
# Modes (#110, interest_mode): 1 = A: interest_a_rate per second on the bank, #ibase = the coins whose interest is the cap
# now (interest_a_cap curve); 2 = B: the curve per period, no base (huge banks: #ppm and #ithr / 100, #idiv says so);
# 3 = C: the curve per period on at most interest_base coins. #idiv nx.eco = #ppm units per coin (bank/interest/team).
scoreboard players set #esec nx.eco 0
execute if score #state nx.state matches 1..2 store result score #esec nx.eco run time query gametime
execute if score #state nx.state matches 1..2 run scoreboard players operation #esec nx.eco -= #t0 nx.eco
scoreboard players operation #esec nx.eco /= #20 nx.eco
execute if score #esec nx.eco matches ..-1 run scoreboard players set #esec nx.eco 0
scoreboard players operation #emin nx.eco = #esec nx.eco
scoreboard players operation #emin nx.eco /= #60 nx.eco
# the rest changes at most once a second (admin changes and load set #rsec -1)
execute if score #esec nx.eco = #rsec nx.eco run return 0
scoreboard players operation #rsec nx.eco = #esec nx.eco
scoreboard players operation #ct nx.eco = #esec nx.eco
execute store result score #imode nx.eco run data get storage nonios:config interest_mode
execute unless score #imode nx.eco matches 1..3 run scoreboard players set #imode nx.eco 1
execute if score #imode nx.eco matches 1 run function nonios:bank/curve/eval_cap
execute if score #imode nx.eco matches 1 store result score #ppm nx.eco run data get storage nonios:config interest_a_rate
execute if score #imode nx.eco matches 2.. run function nonios:bank/curve/eval
execute store result score #c nx.eco run data get storage nonios:config interest_scale
scoreboard players operation #ppm nx.eco *= #c nx.eco
scoreboard players operation #ppm nx.eco /= #100 nx.eco
execute if score #ppm nx.eco matches ..-1 run scoreboard players set #ppm nx.eco 0
execute if score #ppm nx.eco matches 1000001.. run scoreboard players set #ppm nx.eco 1000000
# period 1..100 s (x 20 ticks x 1000000 stays inside an int); mode A is per second
execute store result score #iper nx.eco run data get storage nonios:config interest_period
execute if score #imode nx.eco matches 1 run scoreboard players set #iper nx.eco 1
execute if score #iper nx.eco matches ..0 run scoreboard players set #iper nx.eco 1
execute if score #iper nx.eco matches 101.. run scoreboard players set #iper nx.eco 100
scoreboard players operation #ithr nx.eco = #iper nx.eco
scoreboard players operation #ithr nx.eco *= #20 nx.eco
scoreboard players operation #ithr nx.eco *= #1000000 nx.eco
# text: "<w>.<ff>%/<unit>"
scoreboard players operation #rw nx.eco = #ppm nx.eco
scoreboard players operation #rw nx.eco /= #10000 nx.eco
scoreboard players operation #rt nx.eco = #ppm nx.eco
scoreboard players operation #rt nx.eco %= #10000 nx.eco
scoreboard players operation #rt nx.eco /= #100 nx.eco
data modify storage nonios:eco rt set value {u:"s"}
execute store result storage nonios:eco rt.w int 1 run scoreboard players get #rw nx.eco
execute store result storage nonios:eco rt.f int 1 run scoreboard players get #rt nx.eco
execute store result storage nonios:eco rt.p int 1 run scoreboard players get #iper nx.eco
execute if score #iper nx.eco matches 2.. run function nonios:economy/rate_unit with storage nonios:eco rt
execute if score #iper nx.eco matches 60 run data modify storage nonios:eco rt.u set value "min"
data modify storage nonios:eco unit set from storage nonios:eco rt.u
function nonios:economy/rate_txt with storage nonios:eco rt
# B: coarser units so big banks fit (bank x ppm per tick)
scoreboard players operation #idiv nx.eco = #1000000 nx.eco
execute if score #imode nx.eco matches 2 if score #ppm nx.eco matches 100.. run scoreboard players set #idiv nx.eco 10000
execute if score #imode nx.eco matches 2 if score #ppm nx.eco matches 100.. run scoreboard players operation #ppm nx.eco /= #100 nx.eco
execute if score #imode nx.eco matches 2 if score #idiv nx.eco matches 10000 run scoreboard players operation #ithr nx.eco /= #100 nx.eco
# base: bank coins that earn (A: cap / rate; B: all; C: interest_base); also bounded so acc + base x ppm never overflows
scoreboard players operation #d nx.eco = #ppm nx.eco
execute if score #d nx.eco matches ..0 run scoreboard players set #d nx.eco 1
execute if score #imode nx.eco matches 1 run scoreboard players operation #ibase nx.eco = #capm nx.eco
execute if score #imode nx.eco matches 1 run scoreboard players operation #ibase nx.eco *= #1000 nx.eco
execute if score #imode nx.eco matches 1 run scoreboard players operation #ibase nx.eco /= #d nx.eco
execute if score #imode nx.eco matches 2 run scoreboard players set #ibase nx.eco 2147483647
execute if score #imode nx.eco matches 3 store result score #ibase nx.eco run data get storage nonios:config interest_base
execute if score #ibase nx.eco matches ..-1 run scoreboard players set #ibase nx.eco 0
scoreboard players set #c nx.eco 2147000000
scoreboard players operation #c nx.eco -= #ithr nx.eco
scoreboard players operation #c nx.eco /= #d nx.eco
scoreboard players operation #ibase nx.eco < #c nx.eco
