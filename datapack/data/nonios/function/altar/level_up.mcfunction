# {team}: the step is paid: team level +1. Basic classes pick it up on the next respawn (V2: "a kit each life").
$scoreboard players add #$(team) nx.cls_lvl 1
$scoreboard players set #$(team)_iron nx.altar 0
$scoreboard players set #$(team)_gold nx.altar 0
$scoreboard players set #$(team)_diamond nx.altar 0
$function nonios:altar/refresh {team:"$(team)"}
$execute as @e[type=marker,tag=nx.altar,tag=nx.$(team)] at @s run particle minecraft:witch ~ ~0.5 ~ 0.3 0.3 0.3 1 300 force
$execute as @e[type=marker,tag=nx.altar,tag=nx.$(team)] at @s run playsound minecraft:block.respawn_anchor.set_spawn block @a ~ ~ ~ 1 0.8
$execute as @a[team=$(team)] at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
$tellraw @a[team=$(team)] [{text:"✦ ",color:"light_purple"},{text:"The offering is accepted. Kit ",color:"gray"},{storage:"nonios:altar",nbt:"v.cur",color:"light_purple",bold:true},{text:".",color:"gray"}]
