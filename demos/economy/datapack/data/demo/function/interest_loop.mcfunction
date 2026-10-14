function nonios:bank/interest/pay
scoreboard players remove #demo_n nx.eco 1
execute if score #demo_n nx.eco matches 1.. run function demo:interest_loop
