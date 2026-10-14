# with storage nonios:bank ui.a: both sliders, always (same size and place whatever the balances)
$data modify storage nonios:bank ui.d.inputs append value {type:"minecraft:number_range",key:"dep",label:{text:"Deposit",color:"$(dc)"},width:300,start:1,end:$(pm),step:1,initial:$(pi)}
$data modify storage nonios:bank ui.d.inputs append value {type:"minecraft:number_range",key:"wd",label:{text:"Withdraw",color:"$(wc)"},width:300,start:1,end:$(bm),step:1,initial:$(wi)}
