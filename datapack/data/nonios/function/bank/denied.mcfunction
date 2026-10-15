# bank request refused (#why nx.eco from bank/allowed): close any open bank dialog and say why
dialog clear @s
execute if score #why nx.eco matches 1 run tellraw @s {"text":"The bank is open during a match (preparation and battle).","color":"red"}
execute if score #why nx.eco matches 2 run tellraw @s {"text":"Join a team to use a bank.","color":"red"}
execute if score #why nx.eco matches 3 run tellraw @s {"text":"This is the other team's bank.","color":"red"}
execute if score #why nx.eco matches 4 run tellraw @s {"text":"Too far from your team's vault.","color":"red"}
execute at @s run playsound minecraft:block.note_block.bass player @s ~ ~ ~ 1 0.7
