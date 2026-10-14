# {k: button key w/b/a/n, why: tooltip}: grey out one team-picker button (no action)
$data modify storage nonios:ui team.$(k)c set value "dark_gray"
$data modify storage nonios:ui team.$(k)t set value "$(why)"
$data modify storage nonios:ui team.$(k)a set value ""
