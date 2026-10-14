# #enemy demo: storage demo:tmp enemy = the team opposite to @s (no team = black)
data modify storage demo:tmp enemy set value "black"
execute if entity @s[team=black] run data modify storage demo:tmp enemy set value "white"
