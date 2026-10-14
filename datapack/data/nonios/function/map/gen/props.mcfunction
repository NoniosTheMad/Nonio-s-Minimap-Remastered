# per team: copy the sub-compounds to flat macro args
$function nonios:map/gen/pedestal with storage nonios:map $(t).nexus
$function nonios:map/gen/spawn_pad with storage nonios:map $(t).spawn
$execute positioned 0 0 0 run function nonios:map/gen/mine with storage nonios:map $(t).mine
$function nonios:map/gen/bank with storage nonios:map $(t).bank
$function nonios:shop/spawn_npc with storage nonios:map $(t).shop
$function nonios:map/gen/label with storage nonios:map $(t).label
