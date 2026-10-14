# macro (node data); reads #st, #sgn
$execute if score #st nx.arena matches 0 run bossbar set nonios:arena/$(id) name [{text:"$(name)",color:"yellow",bold:true},{text:"  neutral: stay inside to capture",color:"gray",bold:false}]
$execute if score #st nx.arena matches 1 run bossbar set nonios:arena/$(id) name [{text:"$(name)",color:"yellow",bold:true},{text:"  White capturing",color:"white",bold:false}]
$execute if score #st nx.arena matches 2 run bossbar set nonios:arena/$(id) name [{text:"$(name)",color:"yellow",bold:true},{text:"  Black capturing",color:"light_purple",bold:false}]
$execute if score #st nx.arena matches 3 run bossbar set nonios:arena/$(id) name [{text:"$(name)",color:"yellow",bold:true},{text:"  CONTESTED",color:"red",bold:true}]
$execute if score #st nx.arena matches 4 run bossbar set nonios:arena/$(id) name [{text:"$(name)",color:"yellow",bold:true},{text:"  held by White",color:"white",bold:false}]
$execute if score #st nx.arena matches 5 run bossbar set nonios:arena/$(id) name [{text:"$(name)",color:"yellow",bold:true},{text:"  held by Black",color:"light_purple",bold:false}]
$execute if score #st nx.arena matches 6 run bossbar set nonios:arena/$(id) name [{text:"$(name)",color:"yellow",bold:true},{text:"  White is taking it from Black",color:"white",bold:false}]
$execute if score #st nx.arena matches 7 run bossbar set nonios:arena/$(id) name [{text:"$(name)",color:"yellow",bold:true},{text:"  Black is taking it from White",color:"light_purple",bold:false}]
$execute if score #sgn nx.arena matches 0 run bossbar set nonios:arena/$(id) color yellow
$execute if score #sgn nx.arena matches 1 run bossbar set nonios:arena/$(id) color white
$execute if score #sgn nx.arena matches 2 run bossbar set nonios:arena/$(id) color purple
$execute if score #st nx.arena matches 3 run bossbar set nonios:arena/$(id) color red
