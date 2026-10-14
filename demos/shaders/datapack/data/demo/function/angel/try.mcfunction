# pick a random column within 12 blocks and look for the surface there
execute store result storage demo:angel x int 1 run random value -12..12
execute store result storage demo:angel z int 1 run random value -12..12
scoreboard players set #d demo.st 0
function demo:angel/col with storage demo:angel
