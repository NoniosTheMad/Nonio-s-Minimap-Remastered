# as the Angel (tagged nx.cls_me): tag its allies nx.cls_ally: everything on its team, and demo patients
execute if entity @s[team=white] run tag @e[team=white] add nx.cls_ally
execute if entity @s[team=black] run tag @e[team=black] add nx.cls_ally
tag @e[tag=nx.ang_patient] add nx.cls_ally
tag @s remove nx.cls_ally
