# with <team>.guard {team,foe,x,y,z,r}
$execute in minecraft:overworld positioned $(x) $(y) $(z) as @a[team=$(foe),gamemode=!spectator,gamemode=!creative,distance=..$(r)] at @s run function nonios:guard/hit
