# as a dreamer (landed), at them, every tick: Dream Wings on whatever they wear on the chest, and the jump boost
# bare chest: a pair of Dream Wings (vanish when they wake); any chestplate: glides while it stays in the Dream
execute unless items entity @s armor.chest * run item replace entity @s armor.chest with minecraft:elytra[minecraft:custom_data={nx_dwings:1b,nx_dw:1b},minecraft:item_name={text:"Dream Wings",color:"#7dffc8"},minecraft:enchantments={"nonios:dream_wings":1,"minecraft:vanishing_curse":1},minecraft:unbreakable={},minecraft:tooltip_display={hidden_components:["minecraft:unbreakable"]}]
execute unless items entity @s armor.chest *[minecraft:custom_data~{nx_dw:1b}] run function nonios:dream/wings/grant
# spare Dream Wings (took them off for a chestplate): gone
execute unless items entity @s armor.chest *[minecraft:custom_data~{nx_dwings:1b}] if items entity @s container.* *[minecraft:custom_data~{nx_dwings:1b}] run clear @s minecraft:elytra[minecraft:custom_data~{nx_dwings:1b}]
# boost: a fresh press of jump while gliding spends one charge
scoreboard players remove @s[scores={nx.dboost=1..}] nx.dboost 1
execute if predicate nonios:dream/jump unless entity @s[tag=nx.djump] if predicate nonios:dream/gliding run function nonios:dream/wings/press
tag @s remove nx.djump
execute if predicate nonios:dream/jump run tag @s add nx.djump
# charges refill (nx.dchg in ticks: #wing_cost per charge, #wing_max full)
execute if score @s nx.dchg < #wing_max nx.dream run scoreboard players add @s nx.dchg 1
execute if predicate nonios:dream/gliding if score #t nx.dream matches 0 run function nonios:dream/wings/hud
