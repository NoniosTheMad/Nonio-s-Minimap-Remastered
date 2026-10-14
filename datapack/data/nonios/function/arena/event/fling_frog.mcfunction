tag @s remove nx.ev_frog_new
execute store result entity @s Motion[0] double 0.01 run random value -45..45
execute store result entity @s Motion[1] double 0.01 run random value 10..40
execute store result entity @s Motion[2] double 0.01 run random value -45..45
