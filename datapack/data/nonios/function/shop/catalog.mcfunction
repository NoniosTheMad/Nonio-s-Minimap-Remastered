# Shop catalog (PLACEHOLDER items and prices). Edit + /reload: the dialog is rebuilt from this list every time it opens.
# Fields: name (label), item (id for /give, may carry [components]), count, price (coins),
#         sprite (button icon: a texture in the atlas), atlas (optional, default minecraft:items; block textures: minecraft:blocks).
data modify storage nonios:shop items set value [\
  {name:"Bread",item:"minecraft:bread",count:4,price:5,sprite:"minecraft:item/bread"},\
  {name:"Steak",item:"minecraft:cooked_beef",count:4,price:10,sprite:"minecraft:item/cooked_beef"},\
  {name:"Arrows",item:"minecraft:arrow",count:16,price:8,sprite:"minecraft:item/arrow"},\
  {name:"Iron Sword",item:"minecraft:iron_sword",count:1,price:25,sprite:"minecraft:item/iron_sword"},\
  {name:"Ender Pearl",item:"minecraft:ender_pearl",count:2,price:30,sprite:"minecraft:item/ender_pearl"},\
  {name:"Golden Apple",item:"minecraft:golden_apple",count:1,price:40,sprite:"minecraft:item/golden_apple"},\
  {name:"TNT",item:"minecraft:tnt",count:2,price:50,atlas:"minecraft:blocks",sprite:"minecraft:block/tnt_side"}\
]
