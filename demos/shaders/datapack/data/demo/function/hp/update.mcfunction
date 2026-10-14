# HP tags are on while anyone has the Thermal look
execute store result score #thermal demo.st if entity @a[scores={demo.look=3}]
execute if score #thermal demo.st matches 1.. run function demo:hp/tick
execute if score #thermal demo.st matches 0 if score #hp demo.st matches 1 run function demo:hp/off
execute store success score #hp demo.st if score #thermal demo.st matches 1..
