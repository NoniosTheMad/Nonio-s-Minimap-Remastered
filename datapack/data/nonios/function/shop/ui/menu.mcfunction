# a menu page: ready-made category buttons (tools/build_shop.py)
data modify storage nonios:shop ui.d.actions append from storage nonios:shop ui.list[]
execute store result score #ne nx.tmp run data get storage nonios:shop ui.list
