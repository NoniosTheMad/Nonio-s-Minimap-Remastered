# #gon nx.arena = 1 while the gates work: arena running (= battle in the match), at least one gate and one slot.
# Labels: red when open, dark grey when shut.
scoreboard players set #gon nx.arena 0
execute if score #on nx.arena matches 1 if score #gates nx.arena matches 1.. if score #slots nx.arena matches 1.. run scoreboard players set #gon nx.arena 1
execute if score #gon nx.arena matches 1 as @e[type=text_display,tag=nx.agate_label] run data modify entity @s text set value {text:"ARENA",color:"red",bold:true}
execute if score #gon nx.arena matches 0 as @e[type=text_display,tag=nx.agate_label] run data modify entity @s text set value {text:"ARENA",color:"dark_gray",bold:true}
