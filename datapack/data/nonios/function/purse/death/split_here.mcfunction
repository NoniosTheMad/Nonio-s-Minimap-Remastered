# as + at the victim: success if this kill splits the purse (purse_drop_scope "everywhere", or "centre" and inside the Arena box)
execute if data storage nonios:config {purse_drop_scope:"everywhere"} run return 1
execute unless data storage nonios:config {purse_drop_scope:"centre"} run return fail
execute unless data storage nonios:arena config.bounds.x run return fail
return run function nonios:arena/in_bounds
