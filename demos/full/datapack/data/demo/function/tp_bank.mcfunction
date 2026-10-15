# just outside my team's bank zone (4 blocks east of the vault), facing the vault
execute if entity @s[team=] run return run tellraw @s {"text":"[demo] Join a team first.","color":"red"}
execute if entity @s[team=white] run function demo:tp_bank_at with storage nonios:map white.bank
execute if entity @s[team=black] run function demo:tp_bank_at with storage nonios:map black.bank
