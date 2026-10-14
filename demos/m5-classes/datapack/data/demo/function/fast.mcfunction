# toggle time x10 for generators and arena timers (drops, payouts, events)
execute if score #speed nx.gen matches 10 run return run function demo:say {m:"Generator + arena time x1",cmd:"function demo:speed {s:1}"}
function demo:say {m:"Generator + arena time x10",cmd:"function demo:speed {s:10}"}
