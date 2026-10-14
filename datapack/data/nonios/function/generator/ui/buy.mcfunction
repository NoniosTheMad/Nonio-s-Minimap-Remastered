# as + at a player who clicked "Upgrade": re-check (match phase, own generator within 8) and pay from the purse (generator/buy_m)
scoreboard players reset @s nx.genup
execute if score #map nx.state matches 1 unless score #state nx.state matches 1..2 run return 0
execute unless entity @e[type=marker,tag=nx.gen,distance=..8] run return run title @s actionbar {text:"Too far from the generator",color:"red"}
tag @s add nx.gen_buyer
execute as @e[type=marker,tag=nx.gen,distance=..8,sort=nearest,limit=1] at @s run function nonios:generator/ui/buy_at
tag @s remove nx.gen_buyer
