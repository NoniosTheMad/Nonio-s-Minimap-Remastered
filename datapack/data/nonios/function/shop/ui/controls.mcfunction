# fixed control buttons (rows 1-2), built once on load: storage nonios:shop ctl.*. Greyed variants (_off) and the
# blank grid filler have no action (rendered inactive).
data modify storage nonios:shop ctl.prev set value {label:{text:"◀ Prev"},width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 3"}}
data modify storage nonios:shop ctl.prev_off set value {label:{text:"◀ Prev",color:"dark_gray"},width:120,tooltip:{text:"First page",color:"gray"}}
data modify storage nonios:shop ctl.back set value {label:{text:"▲ Back"},width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 5"}}
data modify storage nonios:shop ctl.back_off set value {label:{text:"▲ Back",color:"dark_gray"},width:120,tooltip:{text:"Already at the top",color:"gray"}}
data modify storage nonios:shop ctl.next set value {label:{text:"Next ▶"},width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 4"}}
data modify storage nonios:shop ctl.next_off set value {label:{text:"Next ▶",color:"dark_gray"},width:120,tooltip:{text:"Last page",color:"gray"}}
data modify storage nonios:shop ctl.again_off set value {label:{text:"⟳ Again",color:"dark_gray"},width:120,tooltip:{text:"Nothing bought yet",color:"gray"}}
data modify storage nonios:shop ctl.blank set value {label:"",width:120}
data modify storage nonios:shop ctl.m0 set value {label:{text:"×1",color:"white"},width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 6"},tooltip:{text:"One lot per click",color:"gray"}}
data modify storage nonios:shop ctl.m0s set value {label:[{text:"▸ ",color:"gold"},{text:"×1",color:"gold",bold:true},{text:" ◂",color:"gold"}],width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 6"},tooltip:{text:"One lot per click",color:"gray"}}
data modify storage nonios:shop ctl.m1 set value {label:{text:"×8",color:"white"},width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 7"},tooltip:{text:"8 lots per click",color:"gray"}}
data modify storage nonios:shop ctl.m1s set value {label:[{text:"▸ ",color:"gold"},{text:"×8",color:"gold",bold:true},{text:" ◂",color:"gold"}],width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 7"},tooltip:{text:"8 lots per click",color:"gray"}}
data modify storage nonios:shop ctl.m2 set value {label:{text:"×64",color:"white"},width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 8"},tooltip:{text:"64 lots per click",color:"gray"}}
data modify storage nonios:shop ctl.m2s set value {label:[{text:"▸ ",color:"gold"},{text:"×64",color:"gold",bold:true},{text:" ◂",color:"gold"}],width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 8"},tooltip:{text:"64 lots per click",color:"gray"}}
data modify storage nonios:shop ctl.m3 set value {label:{text:"Stack",color:"white"},width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 9"},tooltip:{text:"A full stack per click",color:"gray"}}
data modify storage nonios:shop ctl.m3s set value {label:[{text:"▸ ",color:"gold"},{text:"Stack",color:"gold",bold:true},{text:" ◂",color:"gold"}],width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set 9"},tooltip:{text:"A full stack per click",color:"gray"}}
