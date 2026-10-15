execute if data storage nonios:config {spawn_guard:0b} run return run function demo:say {m:"Spawn defense ON",cmd:"data modify storage nonios:config spawn_guard set value 1b"}
function demo:say {m:"Spawn defense OFF",cmd:"data modify storage nonios:config spawn_guard set value 0b"}
