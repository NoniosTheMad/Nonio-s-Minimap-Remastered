# as + at a generator marker whose single block just went (same tick). The miner = nearest player whose mined stat for
# the block (nx.gen_mn) went up; they roll the level's loot table with their tool (Fortune counts).
tag @s remove nx.gen_one
scoreboard players operation @s nx.gen_t = @s nx.gen_iv
tag @a[scores={nx.gen_mn=1..},distance=..8,sort=nearest,limit=1] add nx.gen_miner
scoreboard players set @a[tag=nx.gen_miner] nx.gen_mn 0
data modify storage nonios:gen one set from entity @s data
execute if entity @a[tag=nx.gen_miner] as @a[tag=nx.gen_miner] run function nonios:generator/one/loot with storage nonios:gen one
execute unless entity @a[tag=nx.gen_miner] run function nonios:generator/one/loot_any with storage nonios:gen one
# yield tokens (emeralds with custom_data nx_yield): the miner is paid as if the V2 block had been mined (purse yields)
execute as @e[type=item,distance=..2] if data entity @s Item.components."minecraft:custom_data".nx_yield run function nonios:generator/one/token
tag @a remove nx.gen_miner
particle minecraft:wax_off ~ ~0.5 ~ 0.3 0.3 0.3 0 10
