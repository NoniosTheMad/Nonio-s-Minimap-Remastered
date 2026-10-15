# every tick in prep + battle (economy/tick): smooth interest, +1 coin at a time (#94, #108). economy/rate gives the
# rate per period (#ppm), the earning base (#ibase) and the threshold (#ithr = period ticks x 1000000).
function nonios:economy/rate
function nonios:bank/interest/team {team:"white"}
function nonios:bank/interest/team {team:"black"}
# the Emerald Talisman: interest on its own price (#112)
function nonios:talisman/accrue
