# macro (node config): bossbar + hologram
$bossbar remove nonios:arena/$(id)
$bossbar add nonios:arena/$(id) {text:"$(name)"}
$execute store result bossbar nonios:arena/$(id) max run scoreboard players get #capture nx.arena
$bossbar set nonios:arena/$(id) style notched_10
$bossbar set nonios:arena/$(id) value 0
$summon minecraft:text_display ~ ~$(hy) ~ {Tags:["nx.node_part","nx.node_holo"],billboard:"center",alignment:"center",line_width:220,text:{text:"$(name)"}}
