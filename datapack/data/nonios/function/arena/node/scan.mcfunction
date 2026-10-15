# macro (node data): count capturers in the zone box; bossbar to everyone inside
$execute store result score #w nx.arena if entity @a[x=$(x0),y=$(y),z=$(z0),dx=$(dx),dy=$(dy),dz=$(dx),team=white,gamemode=!spectator]
$execute store result score #b nx.arena if entity @a[x=$(x0),y=$(y),z=$(z0),dx=$(dx),dy=$(dy),dz=$(dx),team=black,gamemode=!spectator]
$execute store result score #cw nx.arena if entity @e[x=$(x0),y=$(y),z=$(z0),dx=$(dx),dy=$(dy),dz=$(dx),type=!player,tag=nx.captor,team=white]
$execute store result score #cb nx.arena if entity @e[x=$(x0),y=$(y),z=$(z0),dx=$(dx),dy=$(dy),dz=$(dx),type=!player,tag=nx.captor,team=black]
scoreboard players operation #w nx.arena += #cw nx.arena
scoreboard players operation #b nx.arena += #cb nx.arena
$bossbar set nonios:arena/$(id) players @a[x=$(x0),y=$(y),z=$(z0),dx=$(dx),dy=$(dy),dz=$(dx)]
