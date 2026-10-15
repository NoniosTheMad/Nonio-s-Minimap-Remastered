# (economy/load) storage nonios:config interest_curve -> nonios:bank curve, each point + d (secant to the next, ppm per
# 1000 s) and m (tangent: ends = their secant; inside = harmonic mean of the two secants, 0 at a peak/valley). Monotone
# data gives a monotone, smooth (C1) curve: no kinks at the points, no overshoot.
# Two curves (#110): interest_a_cap (mode A cap, kept in nonios:bank capc / #cnA, read by bank/curve/eval_cap) and
# interest_curve (modes B, C) in nonios:bank curve / #cn, read by bank/curve/eval.
data modify storage nonios:bank curve set from storage nonios:config interest_a_cap
function nonios:bank/curve/prep
data modify storage nonios:bank capc set from storage nonios:bank curve
scoreboard players operation #cnA nx.eco = #cn nx.eco
data modify storage nonios:bank curve set from storage nonios:config interest_curve
function nonios:bank/curve/prep
