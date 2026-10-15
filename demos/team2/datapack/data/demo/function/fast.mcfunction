# toggle time x10 for generators, arena timers (drops, payouts, events) and the Emerald Talisman income
execute if score #speed nx.gen matches 10 run return run function demo:say {m:"Generator + arena + talisman time x1",cmd:"function demo:speed {s:1}"}
function demo:say {m:"Generator + arena + talisman time x10",cmd:"function demo:speed {s:10}"}
