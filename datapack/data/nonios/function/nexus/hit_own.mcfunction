# a defender hit their own Barrier: no damage, just tell them what it is
function nonios:nexus/hp_text
execute on attacker if function nonios:nexus/msg_gate run title @s actionbar [{"text":"⛨ Your team's Barrier","color":"aqua"},{"text":" — it shields your Nexus ","color":"gray"},{"text":"(HP ","color":"gray"},{"score":{"name":"#hp","objective":"nx.const"},"color":"white"},{"text":"/","color":"gray"},{"score":{"name":"#hp_max","objective":"nx.const"},"color":"white"},{"text":")","color":"gray"}]
function nonios:nexus/hit_end
