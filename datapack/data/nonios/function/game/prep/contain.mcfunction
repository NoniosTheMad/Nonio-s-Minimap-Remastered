# with storage nonios:map <team>: anyone past their own wall (built around it, pillared over...) goes back to spawn
$execute as @a[team=$(team),gamemode=!spectator,gamemode=!creative,$(out)] run function nonios:game/prep/bounce {team:"$(team)"}
