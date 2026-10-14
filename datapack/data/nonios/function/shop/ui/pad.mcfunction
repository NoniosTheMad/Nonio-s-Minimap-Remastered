# fill the grid to 16 slots so the dialog keeps its size and every button its place
execute if score #ne nx.tmp matches 16.. run return 0
data modify storage nonios:shop ui.d.actions append from storage nonios:shop ctl.blank
scoreboard players add #ne nx.tmp 1
function nonios:shop/ui/pad
