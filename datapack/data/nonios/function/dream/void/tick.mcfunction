# as a landed dreamer, at them, every 5 ticks: remember the last solid ground; the void below the islands catches you
execute if predicate nonios:dream/on_ground unless block ~ ~-0.5 ~ #nonios:dream_passable run function nonios:dream/void/remember
execute if entity @s[y=-512,dy=518] run function nonios:dream/void/catch
