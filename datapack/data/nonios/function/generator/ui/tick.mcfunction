# upgrade dialog clicks (/trigger: permission 0). Reset only the triggerer; enable @a last.
execute as @a[scores={nx.genup=1..}] at @s run function nonios:generator/ui/buy
scoreboard players enable @a nx.genup
