# a dragged-down flyer touched the ground: minor, fixed fall damage (2 hearts)
damage @s 4 minecraft:fall
playsound minecraft:entity.player.big_fall player @a ~ ~ ~ 1 0.9
particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.1 ~ 0.4 0.05 0.4 0 20
function nonios:class/cracy_frog/yank_end
