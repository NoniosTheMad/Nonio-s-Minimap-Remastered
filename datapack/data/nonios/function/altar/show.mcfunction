# with storage nonios:altar v: hologram = kit now -> next, then each block type paid / needed.
# The list starts with an empty plain root: in a text list every later element inherits the FIRST one's style, and
# sprite objects are tinted by their colour, so a coloured first element ("OFFERINGS", light purple) dyed the block icons
# (feedback #41). Icons also say color white (= untinted) explicitly.
$data modify entity @e[type=text_display,tag=nx.altar_txt,tag=nx.$(team),limit=1] text set value [{text:""},{text:"OFFERINGS",color:"light_purple",bold:true},{text:"\nKit $(cur) ",color:"gray"},{text:"→ $(nxt)",color:"white"},{text:"\n"},{type:"object",atlas:"minecraft:blocks",sprite:"minecraft:block/iron_block",color:"white"},{text:" $(i)/$(ni)  ",color:"white"},{type:"object",atlas:"minecraft:blocks",sprite:"minecraft:block/gold_block",color:"white"},{text:" $(g)/$(ng)  ",color:"gold"},{type:"object",atlas:"minecraft:blocks",sprite:"minecraft:block/diamond_block",color:"white"},{text:" $(d)/$(nd)",color:"aqua"}]
$data modify entity @e[type=block_display,tag=nx.altar_fx,tag=nx.$(team),limit=1] block_state set value {id:"minecraft:respawn_anchor",properties:{charges:"$(ch)"}}
