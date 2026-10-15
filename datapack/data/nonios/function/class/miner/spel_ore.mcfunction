# an ore cell (from spel_z): a marker that remembers the ore and its Miner
scoreboard players add #n nx.cls_tmp 1
function nonios:class/miner/spel_mark
scoreboard players operation @e[type=marker,tag=nx.spel_new] nx.pid = #me nx.cls_tmp
tag @e[type=marker,tag=nx.spel_new] remove nx.spel_new
