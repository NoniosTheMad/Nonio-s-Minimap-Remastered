# demo-only coin stub (the real purse reads the same mined stats)
execute if score @s demo.m.em matches 1.. run function demo:coin_add {o:"demo.m.em",v:25}
execute if score @s demo.m.dem matches 1.. run function demo:coin_add {o:"demo.m.dem",v:25}
execute if score @s demo.m.dia matches 1.. run function demo:coin_add {o:"demo.m.dia",v:20}
execute if score @s demo.m.gold matches 1.. run function demo:coin_add {o:"demo.m.gold",v:8}
execute if score @s demo.m.lap matches 1.. run function demo:coin_add {o:"demo.m.lap",v:6}
execute if score @s demo.m.emb matches 1.. run function demo:coin_add {o:"demo.m.emb",v:100}
