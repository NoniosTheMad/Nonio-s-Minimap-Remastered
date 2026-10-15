attribute @s minecraft:max_health modifier remove nonios:champ_hp
attribute @s minecraft:attack_damage modifier remove nonios:champ_dmg
$attribute @s minecraft:max_health modifier add nonios:champ_hp $(hp) add_value
$attribute @s minecraft:attack_damage modifier add nonios:champ_dmg $(dmg) add_value
