# macro (storage nonios:arena h). The hologram is the text_display nearest to the marker (keep nodes 8+ blocks apart).
$execute as @e[type=text_display,tag=nx.node_holo,distance=..8,sort=nearest,limit=1] run data modify entity @s text set value [{text:"$(name)",color:"$(oc)",bold:true},{text:"\n$(s)$(p)",color:"$(sc)",bold:false},{text:"\n$(l3)",color:"aqua",bold:false}]
