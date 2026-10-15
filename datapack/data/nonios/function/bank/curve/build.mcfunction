# (economy/load) storage nonios:config interest_curve -> nonios:bank curve, each point + d (secant to the next, ppm per
# 1000 s) and m (tangent: ends = their secant; inside = harmonic mean of the two secants, 0 at a peak/valley). Monotone
# data gives a monotone, smooth (C1) curve: no kinks at the points, no overshoot.
data modify storage nonios:bank curve set from storage nonios:config interest_curve
execute store result score #cn nx.eco run data get storage nonios:bank curve
execute if score #cn nx.eco matches ..1 run return 0
scoreboard players set #ck nx.eco 0
function nonios:bank/curve/sec_loop
scoreboard players set #ck nx.eco 0
function nonios:bank/curve/tan_loop
