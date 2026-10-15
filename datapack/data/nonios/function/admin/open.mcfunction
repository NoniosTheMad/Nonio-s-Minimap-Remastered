# as the admin: current config + phase into storage nonios:ui adm, then show the panel
execute store result score #sec nx.tmp run data get storage nonios:config prep_time
function nonios:game/clock
execute store result storage nonios:ui adm.pm int 1 run scoreboard players get #mm nx.tmp
execute store result storage nonios:ui adm.ps int 1 run scoreboard players get #ss nx.tmp
data modify storage nonios:ui adm.coins set from storage nonios:config start_coins
data modify storage nonios:ui adm.hp set from storage nonios:config barrier_hp
data modify storage nonios:ui adm.ki set value "OFF"
execute if data storage nonios:config {keep_inventory:1b} run data modify storage nonios:ui adm.ki set value "ON"
data modify storage nonios:ui adm.ab set value "OFF"
execute if data storage nonios:config {auto_balance:1b} run data modify storage nonios:ui adm.ab set value "ON"
data modify storage nonios:ui adm.lt set value "OFF"
execute if score #lt_on nx.arena matches 1 run data modify storage nonios:ui adm.lt set value "ON"
data modify storage nonios:ui adm.phase set value "Lobby"
execute if score #state nx.state matches 1 run data modify storage nonios:ui adm.phase set value "Preparation"
execute if score #state nx.state matches 2 run data modify storage nonios:ui adm.phase set value "Battle"
execute if score #state nx.state matches 3 run data modify storage nonios:ui adm.phase set value "End screen"
execute store result storage nonios:ui adm.w int 1 if entity @a[team=white]
execute store result storage nonios:ui adm.b int 1 if entity @a[team=black]
# Rebuild map: lobby only; elsewhere the same button greyed (no action) with a tooltip (dialog rule #41)
data modify storage nonios:ui adm.rbc set value "gray"
data modify storage nonios:ui adm.rbt set value "Regenerate the placeholder map"
data modify storage nonios:ui adm.rba set value ',action:{type:"minecraft:run_command",command:"trigger nx.admin set 23"}'
execute unless score #state nx.state matches 0 run data modify storage nonios:ui adm.rbc set value "dark_gray"
execute unless score #state nx.state matches 0 run data modify storage nonios:ui adm.rbt set value "Lobby only"
execute unless score #state nx.state matches 0 run data modify storage nonios:ui adm.rba set value ""
function nonios:admin/show with storage nonios:ui adm
