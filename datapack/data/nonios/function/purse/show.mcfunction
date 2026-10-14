execute if score @s nx.pslow matches ..0 run return run title @s actionbar [{"text":"Coins ","color":"gold"},{"score":{"name":"@s","objective":"coins"},"color":"yellow","bold":true}]
scoreboard players operation #pct nx.purse = @s nx.pslow
scoreboard players operation #pct nx.purse /= #10 nx.purse
execute if score @s nx.pslow >= #w_cap nx.purse run return run title @s actionbar [{"text":"Coins ","color":"gold"},{"score":{"name":"@s","objective":"coins"},"color":"yellow","bold":true},{"text":"   Weight -","color":"red"},{"score":{"name":"#pct","objective":"nx.purse"},"color":"red"},{"text":"% speed (max)","color":"red"}]
title @s actionbar [{"text":"Coins ","color":"gold"},{"score":{"name":"@s","objective":"coins"},"color":"yellow","bold":true},{"text":"   Weight -","color":"gray"},{"score":{"name":"#pct","objective":"nx.purse"},"color":"white"},{"text":"% speed","color":"gray"}]
