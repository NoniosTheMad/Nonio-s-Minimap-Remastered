# as the Angel: 1 if its halo exists (#me = its nx.pid)
execute as @e[type=text_display,tag=nx.ang_halo] if score @s nx.pid = #me nx.cls_tmp run return 1
return fail
