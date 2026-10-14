# from behind, left or right
execute if score #r demo.st matches 1..6 run playsound nonios:monster.whisper ambient @s ^2.5 ^0.5 ^-2 0.7 1
execute if score #r demo.st matches 7..12 run playsound nonios:monster.whisper ambient @s ^-2.5 ^0.5 ^-2 0.7 1
execute if score #r demo.st matches 1..3 run playsound nonios:monster.whisper ambient @s ^-2.5 ^0.5 ^-2 0.4 0.9
