# the page's buttons (catalog items, or the classes from the items list), then Back
execute if data storage nonios:shop ui.s{classes:1} run data modify storage nonios:shop ui.tmp set from storage nonios:shop items
execute if data storage nonios:shop ui.s{classes:1} run scoreboard players set #n nx.tmp 99
execute if data storage nonios:shop ui.s{classes:1} run function nonios:shop/ui/each
execute if data storage nonios:shop ui.s{classes:0} run data modify storage nonios:shop ui.tmp set from storage nonios:shop ui.s.items
execute if data storage nonios:shop ui.s{classes:0} run function nonios:shop/ui/each_item
data modify storage nonios:shop ui.d.actions append value {label:{text:"◀ Back",color:"gray"},width:150,action:{type:"minecraft:run_command",command:"trigger nx.shop set 1"}}
