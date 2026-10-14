# full
Integration demo for `main`: the whole match (M2 core, economy, generators, Emerald Dream, arena nodes/events,
arena V2 gates + regrowing core) and every class (Reaper, Cracy Frog, Warrior + the 7 V2 shop classes).
Copy of `demos/classes2` (trigger `demo.full`, dialog `demo:full`): buttons 1-45 are the classes2 ones,
46-52 are the arena2 gate/core buttons (TP gate, TP active exit, re-roll slot, gate status, TP core, break core, core status).
53-55 are the shop2 buttons (+10000 coins, open the shop anywhere, clear inventory); 56-64 are the team2 buttons
(offering blocks, partial offering, TP altar, TP enemy spawn, talisman, Dragon Skull, team status, spawn defense on/off,
+3,200,000 coins; team2's 53-61 shifted by 3). "Time x10" (15) also speeds the talisman income.
No game-pack code here; see `demos/m5-classes`, `demos/arena2`, `demos/classes2`, `demos/shop2`, `demos/team2` READMEs for each system.

**Dialog layout (#41/#44):** `demo:full` is a hub of 8 pages (`demo:full/{match,econ,shop,arena,gens,nexus,classes,debug}`,
opened with `show_dialog`); each page's footer button is "◀ Back" to the hub. The trigger values 1-71 are unchanged; some
buttons appear on two pages (+10000 coins, Match clock +10 min). Regenerating the pages: keep each button's `trigger demo.full set N`.
