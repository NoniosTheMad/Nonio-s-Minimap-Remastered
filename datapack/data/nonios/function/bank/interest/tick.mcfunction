# every tick in prep + battle (economy/tick): smooth interest. Same terms as before (economy/rate: rate per second, cap
# #icap coins per second), paid +1 coin at a time: each tick a team adds its per-second interest (1/10000 coin) to
# #acc_<team> and gets a coin per 200000 (= 20 ticks x 10000). At the 20/s cap that is exactly +1 every tick.
function nonios:economy/rate
function nonios:bank/interest/team {team:"white"}
function nonios:bank/interest/team {team:"black"}
