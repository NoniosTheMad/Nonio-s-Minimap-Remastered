# as/at shield: shell back to its resting pose: stage tint, size shrinks 1.40 -> 1.25 as damage grows
scoreboard players operation #col nx.const = @s nx.col
scoreboard players operation #scale nx.const = @s nx.stage
scoreboard players operation #scale nx.const *= #5 nx.const
scoreboard players operation #scale nx.const *= #-1 nx.const
scoreboard players add #scale nx.const 140
execute as @n[type=item_display,tag=nx.shield_fx,distance=..2] run function nonios:nexus/fx/rest_shell
