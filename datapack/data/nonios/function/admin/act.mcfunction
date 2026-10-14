# as a player who used /trigger nx.admin. Values: 1 open | 10/11 prep -/+30s | 12/13 coins -/+25 | 14/15 barrier -/+250
# 16 keep inventory | 17 auto-balance | 20 start | 21 skip phase | 22 stop | 23 rebuild map | 30..49 economy page
scoreboard players operation #av nx.tmp = @s nx.admin
scoreboard players reset @s nx.admin
execute unless entity @s[tag=nx.admin] run return run function nonios:admin/denied
# 30..49: economy page (admin/economy/act)
execute if score #av nx.tmp matches 30..49 run return run function nonios:admin/economy/act
execute if score #av nx.tmp matches 10 run function nonios:admin/adjust {key:"prep_time",op:"remove",n:30,min:0,max:3600}
execute if score #av nx.tmp matches 11 run function nonios:admin/adjust {key:"prep_time",op:"add",n:30,min:0,max:3600}
execute if score #av nx.tmp matches 12 run function nonios:admin/adjust {key:"start_coins",op:"remove",n:25,min:0,max:1000}
execute if score #av nx.tmp matches 13 run function nonios:admin/adjust {key:"start_coins",op:"add",n:25,min:0,max:1000}
execute if score #av nx.tmp matches 14 run function nonios:admin/adjust {key:"barrier_hp",op:"remove",n:250,min:250,max:5000}
execute if score #av nx.tmp matches 15 run function nonios:admin/adjust {key:"barrier_hp",op:"add",n:250,min:250,max:5000}
execute if score #av nx.tmp matches 16 run function nonios:admin/toggle {key:"keep_inventory"}
execute if score #av nx.tmp matches 16 if score #state nx.state matches 1..2 run function nonios:game/apply_config
execute if score #av nx.tmp matches 17 run function nonios:admin/toggle {key:"auto_balance"}
execute if score #av nx.tmp matches 20 run function nonios:game/start
execute if score #av nx.tmp matches 21 run function nonios:game/skip
execute if score #av nx.tmp matches 22 run function nonios:game/stop
execute if score #av nx.tmp matches 23 run function nonios:admin/rebuild
function nonios:admin/open
