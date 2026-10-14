# storage nonios:config -> gamerules and tuning scores
gamerule immediate_respawn true
execute if data storage nonios:config {keep_inventory:1b} run gamerule keep_inventory true
execute if data storage nonios:config {keep_inventory:0b} run gamerule keep_inventory false
execute store result score #barrier_max nx.const run data get storage nonios:config barrier_hp
