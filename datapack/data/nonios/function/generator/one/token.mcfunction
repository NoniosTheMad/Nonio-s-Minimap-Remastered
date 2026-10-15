# as a yield token item next to the generator: credit its block to the miner's mined stat (purse/gen/check pays it,
# Fortune included, like a real block of that kind), then remove it. Nobody to pay: just remove it.
data modify storage nonios:gen tok set value {b:""}
data modify storage nonios:gen tok.b set from entity @s Item.components."minecraft:custom_data".nx_yield
execute if entity @a[tag=nx.gen_miner] run function nonios:generator/one/pay with storage nonios:gen tok
kill @s
