# both team banks + n/2 each (the centre generator reads the total)
$scoreboard players set #demo_b nx.bank $(n)
scoreboard players set #demo_2 nx.bank 2
scoreboard players operation #demo_b nx.bank /= #demo_2 nx.bank
scoreboard players add #white nx.bank 0
scoreboard players add #black nx.bank 0
scoreboard players operation #white nx.bank += #demo_b nx.bank
scoreboard players operation #black nx.bank += #demo_b nx.bank
tellraw @s [{"text":"[demo] Banks: White ","color":"yellow"},{"score":{"name":"#white","objective":"nx.bank"},"color":"gold"},{"text":", Black ","color":"yellow"},{"score":{"name":"#black","objective":"nx.bank"},"color":"gold"}]
