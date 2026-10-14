function nonios:arena/core/pick
execute if score #ci nx.arena matches 0 run scoreboard players add #c0 demo.tal 1
execute if score #ci nx.arena matches 1 run scoreboard players add #c1 demo.tal 1
execute if score #ci nx.arena matches 2 run scoreboard players add #c2 demo.tal 1
execute if score #ci nx.arena matches 3 run scoreboard players add #c3 demo.tal 1
execute if score #ci nx.arena matches 4 run scoreboard players add #c4 demo.tal 1
scoreboard players remove #n demo.tal 1
execute if score #n demo.tal matches 1.. run function demo:sample_step
