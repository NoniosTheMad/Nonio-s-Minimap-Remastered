# with storage nonios:altar v: top level reached
$data modify entity @e[type=text_display,tag=nx.altar_txt,tag=nx.$(team),limit=1] text set value [{text:"OFFERINGS",color:"light_purple",bold:true},{text:"\nKit $(cur)",color:"white"}]
$data modify entity @e[type=block_display,tag=nx.altar_fx,tag=nx.$(team),limit=1] block_state set value {id:"minecraft:respawn_anchor",properties:{charges:"$(ch)"}}
