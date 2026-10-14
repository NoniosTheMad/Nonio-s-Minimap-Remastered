# API: as/at a player, become class number $(num) (src/classes.json "num"). function nonios:class/set {num:1}
# Shop classes are applied as is (the shop charges before calling this); basic classes use the team's level.
$scoreboard players set @s nx.cls_req $(num)
function nonios:class/gen/apply
