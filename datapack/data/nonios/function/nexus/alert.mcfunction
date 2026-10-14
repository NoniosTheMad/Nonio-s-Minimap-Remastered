scoreboard players set @s nx.alert 100
$title @a[team=$(team)] actionbar {"text":"⚠ Your Barrier is under attack! ⚠","color":"red","bold":true}
$execute as @a[team=$(team)] at @s run playsound minecraft:block.bell.use master @s ~ ~ ~ 1 0.5
