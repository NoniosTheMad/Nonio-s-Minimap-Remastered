# shop2
V2 shop catalog demo (branch `feat/shop-v2`). Copy of `demos/full` (trigger `demo.full`, dialog `demo:full`, titled "Demo: V2 shop")
with three extra buttons on top: 53 = +10000 coins, 54 = open the shop anywhere (tag `nx.shop_anywhere`), 55 = clear inventory.
Buttons 1-52 are the `demos/full` ones (whole match + classes).

Game code: `src/shop.json` -> `python tools/build_shop.py` -> `function/shop/catalog.mcfunction` (storage `nonios:shop items/sections/menu`).
Shop flow: `shop/act` (trigger nx.shop: 1 = section menu, 10+k = page k, 100+i = buy items[i]), `shop/open` + `shop/ui/*` build the dialog,
`shop/buy` (+ `buy_enchant` = /enchant on the held item, `buy_xp`, `buy_class`), purse `nx.coins`, full inventory refused.
