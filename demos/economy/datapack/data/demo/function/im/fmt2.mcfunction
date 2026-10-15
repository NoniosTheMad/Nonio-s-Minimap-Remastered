# with demo:im f {k, w, f, m}
$execute if score #df nx.eco matches ..9 run data modify storage demo:im a.$(k)s set value "$(w).0$(f)"
$execute if score #df nx.eco matches 10.. run data modify storage demo:im a.$(k)s set value "$(w).$(f)"
$data modify storage demo:im a.$(k)m set value $(m)
