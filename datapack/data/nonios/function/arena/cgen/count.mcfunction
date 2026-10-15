# as an emerald item near the centre generator: add its stack size to #items
execute store result score #c nx.arena run data get entity @s Item.count
scoreboard players operation #items nx.arena += #c nx.arena
