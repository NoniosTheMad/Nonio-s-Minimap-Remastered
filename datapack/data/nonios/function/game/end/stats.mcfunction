# short summary in chat: one line per player (team order), nexus breaker highlighted
tellraw @a {"text":"──── Match summary ────","color":"gold"}
execute as @a[team=white] run function nonios:game/end/stat_line
execute as @a[team=black] run function nonios:game/end/stat_line
