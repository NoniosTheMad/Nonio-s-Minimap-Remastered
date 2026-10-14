# schedule loop (every interest_period s): banks earn interest only while a match runs (prep + battle)
execute if score #state nx.state matches 1..2 run function nonios:bank/interest/pay
function nonios:bank/interest/arm
