# as + at a player: 100 coins in your purse and a Purse Thief (a husk tagged nx.purse_holder) 4 blocks away.
# If it kills you inside the arena it keeps centre_killer_share % of your purse; the rest drops as coin bags.
scoreboard players add @s nx.coins 100
kill @e[type=husk,tag=demo.thief]
summon minecraft:husk ^ ^ ^4 {Tags:["nx.purse_holder","demo.thief"],CustomName:{text:"Purse Thief",color:"red"},CustomNameVisible:1b,PersistenceRequired:1b,equipment:{mainhand:{id:"minecraft:iron_sword",count:1}},drop_chances:{mainhand:0.0f}}
