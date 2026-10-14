# as + at the nearest generator; buyer tagged nx.gen_buyer
execute if score #map nx.state matches 1 if entity @s[tag=nx.gen.white] unless entity @p[tag=nx.gen_buyer,team=white] run return run title @p[tag=nx.gen_buyer] actionbar {text:"Not your generator",color:"red"}
execute if score #map nx.state matches 1 if entity @s[tag=nx.gen.black] unless entity @p[tag=nx.gen_buyer,team=black] run return run title @p[tag=nx.gen_buyer] actionbar {text:"Not your generator",color:"red"}
function nonios:generator/buy_m
