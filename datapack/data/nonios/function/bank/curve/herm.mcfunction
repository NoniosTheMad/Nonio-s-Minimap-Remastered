# cubic Hermite on segment k: u = s/h (permille), y = h00 y0 + h10 T0 + h01 y1 + h11 T1, T = tangent x h
$execute store result score #x0 nx.eco run data get storage nonios:bank curve[$(k)].t
$execute store result score #h nx.eco run data get storage nonios:bank curve[$(k1)].t
scoreboard players operation #h nx.eco -= #x0 nx.eco
$execute store result score #y0 nx.eco run data get storage nonios:bank curve[$(k)].r
$execute store result score #y1 nx.eco run data get storage nonios:bank curve[$(k1)].r
$execute store result score #t0c nx.eco run data get storage nonios:bank curve[$(k)].m
$execute store result score #t1c nx.eco run data get storage nonios:bank curve[$(k1)].m
scoreboard players operation #t0c nx.eco *= #h nx.eco
scoreboard players operation #t0c nx.eco /= #1000 nx.eco
scoreboard players operation #t1c nx.eco *= #h nx.eco
scoreboard players operation #t1c nx.eco /= #1000 nx.eco
scoreboard players operation #u nx.eco = #ct nx.eco
scoreboard players operation #u nx.eco -= #x0 nx.eco
scoreboard players operation #u nx.eco *= #1000 nx.eco
scoreboard players operation #u nx.eco /= #h nx.eco
scoreboard players operation #u2 nx.eco = #u nx.eco
scoreboard players operation #u2 nx.eco *= #u nx.eco
scoreboard players operation #u2 nx.eco /= #1000 nx.eco
scoreboard players operation #u3 nx.eco = #u2 nx.eco
scoreboard players operation #u3 nx.eco *= #u nx.eco
scoreboard players operation #u3 nx.eco /= #1000 nx.eco
# h01 = 3u2 - 2u3, h00 = 1000 - h01, h11 = u3 - u2, h10 = h11 - u2 + u
scoreboard players operation #h01 nx.eco = #u2 nx.eco
scoreboard players operation #h01 nx.eco *= #3 nx.eco
scoreboard players operation #c nx.eco = #u3 nx.eco
scoreboard players operation #c nx.eco *= #2 nx.eco
scoreboard players operation #h01 nx.eco -= #c nx.eco
scoreboard players set #h00 nx.eco 1000
scoreboard players operation #h00 nx.eco -= #h01 nx.eco
scoreboard players operation #h11 nx.eco = #u3 nx.eco
scoreboard players operation #h11 nx.eco -= #u2 nx.eco
scoreboard players operation #h10 nx.eco = #h11 nx.eco
scoreboard players operation #h10 nx.eco -= #u2 nx.eco
scoreboard players operation #h10 nx.eco += #u nx.eco
scoreboard players operation #ppm nx.eco = #h00 nx.eco
scoreboard players operation #ppm nx.eco *= #y0 nx.eco
scoreboard players operation #h01 nx.eco *= #y1 nx.eco
scoreboard players operation #ppm nx.eco += #h01 nx.eco
scoreboard players operation #h10 nx.eco *= #t0c nx.eco
scoreboard players operation #ppm nx.eco += #h10 nx.eco
scoreboard players operation #h11 nx.eco *= #t1c nx.eco
scoreboard players operation #ppm nx.eco += #h11 nx.eco
scoreboard players operation #ppm nx.eco /= #1000 nx.eco
