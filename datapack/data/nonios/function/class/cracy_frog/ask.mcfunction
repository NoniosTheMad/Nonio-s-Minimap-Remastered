# trigger nx.cls_ask (dialogs nonios:class/frog_ask_1..3, the V2 CracyFrogCheck chain). Shop: "trigger nx.cls_ask set 1".
# 1 = open, 2/3/4 = "Yes" on step 1/2/3, 5/6/7 = "No" on step 1/2/3. nx.cls_askst = step shown (no skipping ahead).
scoreboard players operation #a nx.cls_tmp = @s nx.cls_ask
scoreboard players set @s nx.cls_ask 0
execute if score #a nx.cls_tmp matches 1 run return run function nonios:class/cracy_frog/ask_step {step:1}
execute if score #a nx.cls_tmp matches 2 if score @s nx.cls_askst matches 1 run return run function nonios:class/cracy_frog/ask_step {step:2}
execute if score #a nx.cls_tmp matches 3 if score @s nx.cls_askst matches 2 run return run function nonios:class/cracy_frog/ask_step {step:3}
execute if score #a nx.cls_tmp matches 4 if score @s nx.cls_askst matches 3 run return run function nonios:class/cracy_frog/ask_yes
execute if score #a nx.cls_tmp matches 5 run return run function nonios:class/cracy_frog/ask_no {m:"Don't mess with people, kid."}
execute if score #a nx.cls_tmp matches 6 run return run function nonios:class/cracy_frog/ask_no {m:"Hahaha! I almost believed it!"}
execute if score #a nx.cls_tmp matches 7 run return run function nonios:class/cracy_frog/ask_no {m:"You scared me!"}
