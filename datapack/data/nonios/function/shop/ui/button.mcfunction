# one item slot: icon, name xquantity, total price; tooltip: name, unit price, blurb, why it is greyed.
# Greyed (unaffordable) = same button without action: the client renders it inactive.
execute if data storage nonios:shop ui.c{act:0b} run return run function nonios:shop/ui/button_off with storage nonios:shop ui.c
$data modify storage nonios:shop ui.d.actions append value {label:[{type:"object",atlas:"$(atlas)",sprite:"$(sprite)"},{text:" $(label)$(qt) ",color:"$(ncol)"},{text:"$(pt)",color:"$(pcol)"}],tooltip:[{text:"$(label)$(qt)\n",color:"$(ncol)"},{text:"$(unit)",color:"gray"},{text:"$(blurb)",color:"dark_gray",italic:true},{text:"$(tip)",color:"red"}],width:120,action:{type:"minecraft:run_command",command:"trigger nx.shop set $(n)"}}
