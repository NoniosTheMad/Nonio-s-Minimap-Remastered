kill @e[tag=nx.cls_dummy]
summon minecraft:husk ^ ^ ^4 {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["nx.soul","nx.cls_dummy"],CustomName:{text:"Test Dummy",color:"gray"},CustomNameVisible:1b}
summon minecraft:husk ^2.5 ^ ^4 {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["nx.soul","nx.cls_dummy"],CustomName:{text:"Test Dummy",color:"gray"},CustomNameVisible:1b}
summon minecraft:husk ^-2.5 ^ ^4 {NoAI:1b,PersistenceRequired:1b,Silent:1b,Tags:["nx.soul","nx.cls_dummy"],CustomName:{text:"Test Dummy",color:"gray"},CustomNameVisible:1b}
function demo:say {m:"3 dummies in front of you. They count as souls for the Reaper."}
