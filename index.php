<?php
namespace Golf;

require "vendor/autoload.php";

use \Golf\TotalScore;

ini_set('xdebug.var_display_max_children', -1);
ini_set('xdebug.var_display_max_data', -1);
ini_set('xdebug.var_display_max_depth', -1);

// warning もエラーにする
set_error_handler(function ($errno, $errstr, $errfile, $errline) {
    throw new \RuntimeException(sprintf('errno=%s: %s on line %d in file %s', $errno, $errstr, $errline, $errfile));
});

$x=new TotalScore();
$r=$x->getIGolf();
//var_dump(json_encode($r,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE));
$r=$x->getMarshalI();
var_dump(json_encode($r,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE));
$x->storeScores();
