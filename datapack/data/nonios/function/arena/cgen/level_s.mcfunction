# as the core display: scale it to storage cg.s (interpolated)
data modify entity @s transformation.scale set value [1f,1f,1f]
data modify entity @s transformation.scale[0] set from storage nonios:arena cg.s
data modify entity @s transformation.scale[1] set from storage nonios:arena cg.s
data modify entity @s transformation.scale[2] set from storage nonios:arena cg.s
data modify entity @s interpolation_duration set value 20
data modify entity @s start_interpolation set value 0
