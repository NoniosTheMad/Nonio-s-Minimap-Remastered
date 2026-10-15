# toggle time x10 for arena timers (gate rotation, core regrow delay, payouts, events) and generators
execute if score #speed nx.arena matches 10 run return run function demo:say {m:"Arena + generator time x1",cmd:"function demo:speed {s:1}"}
function demo:say {m:"Arena + generator time x10",cmd:"function demo:speed {s:10}"}
