<?php

namespace Golf;

require "vendor/autoload.php";

use Golf\TotalScore;

ini_set('xdebug.var_display_max_children', -1);
ini_set('xdebug.var_display_max_data', -1);
ini_set('xdebug.var_display_max_depth', -1);

// warning もエラーにする
set_error_handler(function ($errno, $errstr, $errfile, $errline) {
    throw new \RuntimeException(sprintf('errno=%s: %s on line %d in file %s', $errno, $errstr, $errline, $errfile));
});


class MyGolf
{
    public function __construct()
    {
    }

    /**
     *@SuppressWarnings(PHPMD.ExitExpression)
     */
    public function execute()
    {
        $shortopts = 'h';//スイッチだけ
        $shortopts .= 'i:';//:は値を必須で受け取る
        $shortopts .= 'm:';//:は値を必須で受け取る
        $longopts[] = 'help';//スイッチだけ

        $options = getopt($shortopts, $longopts);
        if($options === false) {
            fputs(STDERR, "There was a problem reading in the options.\n" . print_r($argv, true));
            exit(1);
        }
        $output = '';

        if(empty($options) || isset($options['h']) || isset($options['help'])) {
            $output = <<<'EOL'
-h [--help]  helpこのコマンド
-m Parse MarshalI site date
-i Parse IGolf site date

Usage:
php index.php -i "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a"
php index.php -m "https://marshal-i.com/ops/score/oakvillage_20231031_7bf14538"

EOL;
            echo $output;
            exit(0);
        }

        $x = new TotalScore();
        if($url = $options["i"] ?? false) {
            $r = $x->getIGolf($url);
        }
        if($url = $options["m"] ?? false) {
            $r = $x->getMarshalI($url);
        }
        var_dump(json_encode($r, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
        $x->storeScores();
    }
}


$x = new MyGolf();
$x->execute();
