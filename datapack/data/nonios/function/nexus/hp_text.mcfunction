# as shield: copy HP to fake players so player-context text can show it
scoreboard players operation #hp nx.const = @s nx.hp
scoreboard players operation #hp_max nx.const = @s nx.hp_max
