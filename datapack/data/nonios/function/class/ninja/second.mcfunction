# Ninja, once a second: nothing but the sandals (other armour goes back to the inventory)
execute if items entity @s armor.head * run return run function nonios:class/ninja/unarmour
execute if items entity @s armor.chest * run return run function nonios:class/ninja/unarmour
execute if items entity @s armor.legs * run function nonios:class/ninja/unarmour
