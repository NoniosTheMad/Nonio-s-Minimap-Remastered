# macro (config.center). V2 rabbit: 200 HP, 0.6 speed, burning, silent, regeneration. Here 100 HP + Regeneration V
# so it survives its own bolts but a few players can kill it.
scoreboard players operation #lt_rt nx.arena = #lt_resp nx.arena
scoreboard players operation #lt_t nx.arena = #lt_every nx.arena
$summon minecraft:lightning_bolt $(x) $(y) $(z)
$summon minecraft:rabbit $(x) $(y) $(z) {Tags:["nx.lrabbit"],PersistenceRequired:1b,Silent:1b,HasVisualFire:1b,Glowing:1b,CustomName:{text:"Lightning Rabbit",color:"yellow",bold:true},Health:100f,attributes:[{id:"minecraft:max_health",base:100d},{id:"minecraft:movement_speed",base:0.6d},{id:"minecraft:knockback_resistance",base:1d}],active_effects:[{id:"minecraft:regeneration",amplifier:4b,duration:-1,show_particles:0b},{id:"minecraft:fire_resistance",amplifier:0b,duration:-1,show_particles:0b}],DeathLootTable:"nonios:arena/lightning_rabbit"}
tellraw @a [{text:"⚡ ",color:"yellow"},{text:"The Lightning Rabbit is loose in the Arena!",color:"yellow"}]
