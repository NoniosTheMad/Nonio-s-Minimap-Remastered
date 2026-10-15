# macro (node config): bossbar (max = capture x 10: arena/rune/slide fills it a little every tick)
$bossbar remove nonios:arena/$(id)
$bossbar add nonios:arena/$(id) {text:"$(label)"}
$execute store result bossbar nonios:arena/$(id) max run scoreboard players get #cap10 nx.arena
$bossbar set nonios:arena/$(id) style progress
$bossbar set nonios:arena/$(id) value 0
