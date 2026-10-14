# ALL zone coordinates of the (placeholder) map live here, in storage nonios:map. Logic never hardcodes positions.
# The real map (M6) only has to replace this file (+ map/gen/* if it is built by hand instead of generated).
# Layout (void world): lobby at the origin; along +z: White field | wall | Arena | wall | Black field.
#   White field x -15..15, z 55..85   Arena z 86..114   Black field z 115..145   (mirror plane z = 100)
# Island layers: y 60 stone, 61-62 dirt, 63 grass (top). Players stand at y 64.
data modify storage nonios:map lobby set value {x:0.5d,y:64,z:0.5d,yaw:0,bx:0,bz:0,x1:-9,x2:9,z1:-9,z2:9,y:63}
data modify storage nonios:map arena set value {x1:-15,x2:15,z1:86,z2:114,y:63,cx:0.5d,cy:75,cz:100.5d}
# area cleared on every rebuild (blocks y1..y2 + all non-player entities). Keep dx*dz*2 <= 32768 (one fill per 2 layers).
data modify storage nonios:map area set value {x1:-48,x2:48,z1:44,z2:156,y1:40,y2:135,dx:96,dz:112}
# chunks kept loaded (map + lobby), so the Nexus/regen/NPCs tick with nobody near
data modify storage nonios:map load set value {x1:-48,z1:-16,x2:48,z2:160}
data modify storage nonios:map white set value {\
  team:"white",Team:"WHITE",x1:-15,x2:15,z1:55,z2:85,y:63,\
  trim:"minecraft:white_concrete",accent:"minecraft:light_blue_stained_glass",\
  spawn:{x:0.5d,y:64,z:70.5d,yaw:0,bx:0,bz:70},\
  nexus:{team:"white",x:0,y:65,z:60},\
  shop:{team:"white",x:-8.5d,y:64,z:64.5d,yaw:-90},\
  bank:{team:"white",x:9,y:63,z:64},\
  mine:{x:8,y:64,z:74},\
  wall:{team:"white",z:85,tint:11069695},label:{Team:"WHITE",color:"white",x:0,y:68,z:76},\
  out:"x=-1000,y=-200,z=87,dx=2000,dy=900,dz=2000"\
}
data modify storage nonios:map black set value {\
  team:"black",Team:"BLACK",x1:-15,x2:15,z1:115,z2:145,y:63,\
  trim:"minecraft:black_concrete",accent:"minecraft:purple_stained_glass",\
  spawn:{x:0.5d,y:64,z:130.5d,yaw:180,bx:0,bz:130},\
  nexus:{team:"black",x:0,y:65,z:140},\
  shop:{team:"black",x:-8.5d,y:64,z:136.5d,yaw:-90},\
  bank:{team:"black",x:9,y:63,z:136},\
  mine:{x:8,y:64,z:121},\
  wall:{team:"black",z:115,tint:12086271},label:{Team:"BLACK",color:"dark_purple",x:0,y:68,z:124},\
  out:"x=-1000,y=-200,z=-1887,dx=2000,dy=900,dz=2000"\
}
