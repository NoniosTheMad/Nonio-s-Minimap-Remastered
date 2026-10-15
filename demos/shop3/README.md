# shop3
Shop v3 (#32), hotbar gear convention (#34) and arrows vs the Nexus barrier (#37), on top of the full game.
Trigger `demo.shop3`, dialog `demo:shop3` (16 buttons, 2 columns): match start/skip/stop, coins, shop anywhere, clear/fill
inventory, gear tests (`nonios:gear/give`), Power V bow, TP to the enemy Nexus, barrier HP, catalog swap.
`stress.json` = extra sections for `tools/build_shop.py --extra demos/shop3/stress.json --out .../catalog_stress.mcfunction`
(362 generated items: Colours and Wood with 11-12 subcategories each, Stone). "Real catalog" runs `nonios:shop/catalog` again.
