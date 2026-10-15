# as/at a player who just entered a bank zone. Own team's zone in prep/battle: the whole purse goes to the team bank.
# The other team's zone: the vault refuses (sound only).
tag @s add nx.bk.on
execute unless score #state nx.state matches 1..2 run return 0
execute if entity @s[team=white] if entity @e[type=marker,tag=nx.bank_zone,tag=nx.white,distance=..6] run return run function nonios:bank/zone/deposit {team:"white",Team:"White",color:"white",enemy:"black"}
execute if entity @s[team=black] if entity @e[type=marker,tag=nx.bank_zone,tag=nx.black,distance=..6] run return run function nonios:bank/zone/deposit {team:"black",Team:"Black",color:"light_purple",enemy:"white"}
playsound minecraft:block.vault.reject_rewarded_player player @s ~ ~ ~ 1 1
