# macro (storage n): n.rune = config.rune_of.<bonus> (unknown bonus: othala)
data modify storage nonios:arena n.rune set value "othala"
$data modify storage nonios:arena n.rune set from storage nonios:arena config.rune_of.$(bonus)
