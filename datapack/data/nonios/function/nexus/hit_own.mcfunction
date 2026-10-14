# a defender hit their own Barrier: no damage, just tell them what it is (no HP numbers)
execute on attacker if function nonios:nexus/msg_gate run title @s actionbar {"text":"⛨ Your team's Barrier","color":"aqua"}
function nonios:nexus/hit_end
