# {team, Team, loser}
function nonios:game/end/begin
$title @a[team=$(team)] subtitle {"text":"$(Team) wins the match","color":"gold"}
$title @a[team=$(team)] title {"text":"VICTORY","color":"gold","bold":true}
$title @a[team=$(loser)] subtitle {"text":"$(Team) wins the match","color":"gray"}
$title @a[team=$(loser)] title {"text":"DEFEAT","color":"red","bold":true}
$title @a[team=] title {"text":"$(Team) WINS","color":"gold","bold":true}
$execute as @a[team=$(team)] at @s run playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1
$execute as @a[team=$(loser)] at @s run playsound minecraft:entity.wither.death master @s ~ ~ ~ 0.4 1
$execute as @a[team=$(team),gamemode=!spectator] at @s run summon minecraft:firework_rocket ~ ~1 ~ {LifeTime:20,FireworksItem:{id:"minecraft:firework_rocket",count:1,components:{"minecraft:fireworks":{explosions:[{shape:"large_ball",colors:[I;16766720,16777215]}]}}}}
$tellraw @a [{"text":"\n$(Team) WINS","color":"gold","bold":true}]
function nonios:game/end/stats
