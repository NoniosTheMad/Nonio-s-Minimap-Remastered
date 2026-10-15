# advancement nonios:class/champion_bounty: this player killed a Champion with 3+ kills. Bounty = 10 coins per kill.
advancement revoke @s only nonios:class/champion_bounty
scoreboard players set #b nx.cls_tmp 0
execute as @a[scores={nx.class=11,nx.cls_champ=3..}] if data entity @s {Health:0.0f} run scoreboard players operation #b nx.cls_tmp = @s nx.cls_champ
scoreboard players operation #b nx.cls_tmp *= #10 nx.cls_tmp
scoreboard players operation @s nx.coins += #b nx.cls_tmp
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 1.4
title @s actionbar [{"text":"Bounty +","color":"gold"},{"score":{"name":"#b","objective":"nx.cls_tmp"},"color":"yellow"}]
