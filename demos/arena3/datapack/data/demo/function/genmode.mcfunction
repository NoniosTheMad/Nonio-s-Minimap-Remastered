function nonios:generator/mode/toggle
execute if score #single nx.gen matches 1 run tellraw @s {"text":"[demo] Generators: single block (gilded blackstone; drops roll the V2 odds).","color":"yellow"}
execute if score #single nx.gen matches 0 run tellraw @s {"text":"[demo] Generators: V2 blocks.","color":"yellow"}
