# from berserker/guard: health dropped (#hp < nx.cls_bhp, both x100): +2 Rage per health point lost
scoreboard players operation #d nx.cls_tmp = @s nx.cls_bhp
scoreboard players operation #d nx.cls_tmp -= #hp nx.cls_tmp
scoreboard players operation #d nx.cls_tmp /= #50 nx.cls_tmp
scoreboard players operation @s nx.cls_brg += #d nx.cls_tmp
function nonios:class/berserker/rage_cap
