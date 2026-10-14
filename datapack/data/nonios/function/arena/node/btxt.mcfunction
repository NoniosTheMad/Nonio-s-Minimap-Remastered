# macro (storage n): the bonus's display text (config.bonus_text.<bonus>; unknown bonus = no text)
$data modify storage nonios:arena n.btxt set from storage nonios:arena config.bonus_text.$(bonus)
