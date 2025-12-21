<pre><?php

// start to update

$easy=$_GET['easy'] ?? "";
if($easy==="easy") $easy="--hide";

system("/home/ubuntu/golf/webpage/gplus/publish $easy 2>&1");
