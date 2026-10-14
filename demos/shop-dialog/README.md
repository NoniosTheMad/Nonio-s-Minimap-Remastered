# shop-dialog
M1 spike: buy items from a dialog with no op prompts.
Game code: `datapack/data/nonios/function/shop/` (+ advancement `nonios:shop/npc`). The G entry "Shop" is the demo dialog `demo:shop_open` (the game has no G shop entry).
- Catalog = storage `nonios:shop items` (set in `shop/catalog.mcfunction`): name, item, count, price, sprite (+ atlas).
- `trigger nx.shop set 1` opens; `100+i` buys `items[i]`. The tick resets only the triggerer and enables `@a` last.
- The dialog is rebuilt per open by recursive macros (`shop/open` -> `ui/each` -> `ui/action`) and shown with `$dialog show @s $(d)`:
  balance line, last result line (bought / not enough coins), one button per item (icon via `object` text component, price red if unaffordable).
- `after_action: wait_for_response`: after a click the client waits and the server re-opens the shop with the new balance.
- Shopkeeper: NoAI villager + interaction entity (tag nx.shop_npc), `nonios:shop/spawn_npc {team,x,y,z,yaw}`. The shop opens only next to a shopkeeper of your team (`team:"any"` = everyone, used here);
  players tagged `nx.shop_anywhere` (demo players) can open it anywhere. Full inventory = refused, no coins taken.
- `nx.coins` is shared with the coin purse (mining feeds it in the game).
