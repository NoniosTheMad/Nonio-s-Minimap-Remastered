# every tick (nonios:tick, before purse/tick): a protected block changed -> restore
execute if score #prot nx.arena matches 1 run function nonios:arena/protect/check with storage nonios:arena prot
