# as a player with a kill reward / taken purse to show (tag nx.k.show): one actionbar line, then the coin HUD pauses ~2 s
tag @s remove nx.k.show
scoreboard players add @s nx.krw 0
scoreboard players add @s nx.kbty 0
scoreboard players add @s nx.kbon 0
scoreboard players add @s nx.kpurse 0
data modify storage nonios:eco ab set value {k:"",b:"",t:"",p:""}
execute if score @s nx.krw matches 1.. run function nonios:economy/kill/part {key:"k",obj:"nx.krw",label:"kill"}
execute if score @s nx.kbty matches 1.. run function nonios:economy/kill/part {key:"b",obj:"nx.kbty",label:"bounty"}
execute if score @s nx.kbon matches 1.. run function nonios:economy/kill/part {key:"t",obj:"nx.kbon",label:"bonus"}
execute if score @s nx.kpurse matches 1.. run function nonios:economy/kill/part {key:"p",obj:"nx.kpurse",label:"purse"}
scoreboard players operation #sum nx.eco = @s nx.krw
scoreboard players operation #sum nx.eco += @s nx.kbty
scoreboard players operation #sum nx.eco += @s nx.kbon
scoreboard players operation #sum nx.eco += @s nx.kpurse
execute store result storage nonios:eco ab.sum int 1 run scoreboard players get #sum nx.eco
scoreboard players set @s nx.krw 0
scoreboard players set @s nx.kbty 0
scoreboard players set @s nx.kbon 0
scoreboard players set @s nx.kpurse 0
execute if score #sum nx.eco matches ..0 run return 0
function nonios:economy/kill/show_line with storage nonios:eco ab
function nonios:hud/hold
