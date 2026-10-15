# macro {p, t, e}: one point on each side of the zone square, just above the floor (normal range: players within 32)
$execute rotated 0 0 run particle $(p) ^$(t) ^0.12 ^$(e) 0 0 0 0 1
$execute rotated 90 0 run particle $(p) ^$(t) ^0.12 ^$(e) 0 0 0 0 1
$execute rotated 180 0 run particle $(p) ^$(t) ^0.12 ^$(e) 0 0 0 0 1
$execute rotated 270 0 run particle $(p) ^$(t) ^0.12 ^$(e) 0 0 0 0 1
