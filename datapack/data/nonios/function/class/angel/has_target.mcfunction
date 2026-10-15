# as/at the Angel: 1 if its locked ally is still an ally within 16 blocks
execute as @e[tag=nx.ang_t,tag=nx.cls_ally,distance=..16] if score @s nx.cls_atg = #me nx.cls_tmp run return 1
return fail
