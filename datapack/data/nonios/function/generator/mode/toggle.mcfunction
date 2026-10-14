# generator style switch (#47): 0 = V2 blocks (a different block per outcome), 1 = single block + loot table.
# Default from src/generators.json (single.on); every generator regrows at once in the new style.
execute store success score #was nx.gen if score #single nx.gen matches 1
execute if score #was nx.gen matches 1 run scoreboard players set #single nx.gen 0
execute if score #was nx.gen matches 0 run scoreboard players set #single nx.gen 1
execute as @e[type=marker,tag=nx.gen] at @s run function nonios:generator/mode/regrow
