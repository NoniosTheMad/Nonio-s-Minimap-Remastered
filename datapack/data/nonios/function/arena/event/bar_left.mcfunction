# macro (storage ev): a running timed event: "NAME  Ns" (time left)
$bossbar set nonios:arena/event name [{text:"$(name)",color:"$(color)",bold:true},{text:"  $(sec)s",color:"white",bold:false}]
