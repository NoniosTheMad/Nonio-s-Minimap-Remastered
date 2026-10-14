# as + at a generator marker; clicker tagged nx.gen_clicker. Upgrade dialog (price + purse); paying = /trigger nx.genup set 1.
# In the match (#map nx.state = 1) only the owner team can upgrade, during prep/battle. Outside it (generators demo): anyone.
execute if score #map nx.state matches 1 unless score #state nx.state matches 1..2 run return 0
execute if score #map nx.state matches 1 if entity @s[tag=nx.gen.white] unless entity @p[tag=nx.gen_clicker,team=white] run return run title @p[tag=nx.gen_clicker] actionbar {text:"Not your generator",color:"red"}
execute if score #map nx.state matches 1 if entity @s[tag=nx.gen.black] unless entity @p[tag=nx.gen_clicker,team=black] run return run title @p[tag=nx.gen_clicker] actionbar {text:"Not your generator",color:"red"}
execute if score @s nx.gen_lvl matches 3.. run return run title @p[tag=nx.gen_clicker] actionbar {text:"Max level",color:"yellow"}
data modify storage nonios:gen ui set from entity @s data
execute if score @s nx.gen_lvl matches ..1 store result storage nonios:gen ui.cost int 1 run scoreboard players get #cost2 nx.gen
execute if score @s nx.gen_lvl matches 2 store result storage nonios:gen ui.cost int 1 run scoreboard players get #cost3 nx.gen
scoreboard players operation #nl nx.gen = @s nx.gen_lvl
execute store result storage nonios:gen ui.next int 1 run scoreboard players add #nl nx.gen 1
scoreboard players add @p[tag=nx.gen_clicker] nx.coins 0
execute store result storage nonios:gen ui.coins int 1 run scoreboard players get @p[tag=nx.gen_clicker] nx.coins
execute as @p[tag=nx.gen_clicker] run function nonios:generator/ui/show with storage nonios:gen ui
