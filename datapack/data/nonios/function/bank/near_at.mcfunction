# macro {bank_range} (= storage nonios:config): #near nx.eco 1 at own vault; #why 3 when only the other team's vault is near
scoreboard players set #near nx.eco 0
$execute if entity @s[team=white] if entity @e[type=marker,tag=nx.bank_zone,tag=nx.white,distance=..$(bank_range)] run scoreboard players set #near nx.eco 1
$execute if entity @s[team=black] if entity @e[type=marker,tag=nx.bank_zone,tag=nx.black,distance=..$(bank_range)] run scoreboard players set #near nx.eco 1
$execute if score #near nx.eco matches 0 if entity @e[type=marker,tag=nx.bank_zone,distance=..$(bank_range)] run scoreboard players set #why nx.eco 3
