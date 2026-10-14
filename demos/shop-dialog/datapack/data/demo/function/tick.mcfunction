execute as @a[tag=!demo.init] run function demo:init
execute as @a[scores={demo.shop=1}] run function demo:coins {op:"add",n:10,m:"+10 coins"}
execute as @a[scores={demo.shop=2}] run function demo:coins {op:"add",n:100,m:"+100 coins"}
execute as @a[scores={demo.shop=3}] run function demo:coins {op:"set",n:0,m:"Coins set to 0"}
execute as @a[scores={demo.shop=4}] run clear @s
execute if entity @a[scores={demo.shop=5}] run function nonios:shop/spawn_npc {x:0.5,y:64,z:-3.5,yaw:0}
scoreboard players reset @a demo.shop
scoreboard players enable @a demo.shop
