# as/at shield: shell back to its resting size and team tint
scoreboard players operation #col nx.const = @s nx.col
execute as @n[type=item_display,tag=nx.shield_fx,distance=..2] run function nonios:nexus/fx/rest_shell
