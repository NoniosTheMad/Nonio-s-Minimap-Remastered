# lifesteal heals through Instant Health, which lands on the player's next tick: the first rise after it is allowed
# (up to the granted amount); a grant nobody used expires after 3 ticks
execute if score #hp nx.cls_tmp > @s nx.cls_bhp run return run function nonios:class/berserker/grant_use
scoreboard players remove @s nx.cls_bgt 1
execute if score @s nx.cls_bgt matches ..0 run scoreboard players set @s nx.cls_bgr 0
