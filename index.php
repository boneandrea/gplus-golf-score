<?php

require "vendor/autoload.php";
use Symfony\Component\DomCrawler\Crawler;
use GuzzleHttp\Client;
use GuzzleHttp\Cookie\CookieJar;

ini_set('xdebug.var_display_max_children', -1);
ini_set('xdebug.var_display_max_data', -1);
ini_set('xdebug.var_display_max_depth', -1);

class TotalScore{
    public function getIGolf(){
        // Guzzleを使用してWebページを取得
        $url0="https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a";
        $url1="https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre/leaderboard";

        $client = new Client(['cookies' => true]);
        $jar = new CookieJar;
        $response = $client->request('GET', $url0);
        $response = $client->request('GET', $url1);

        // ページのコンテンツをDomCrawlerに渡す
        $html = $response->getBody()->getContents();
        $dom = new Crawler($html);

        $tr=$dom->filter(".ui-table-view tr");

        $count_members=$tr->count()-2;

        $scores=[];

        for($i=0;$i<$count_members;$i++){
            $score=$tr->eq($i+2);
            $scores[]=[
                "name"=>$score->filter("td")->eq(1)->text(),
                "gross"=>intval($score->filter("td")->eq(28)->text())
            ];
        }
        var_dump(json_encode($scores,JSON_PRETTY_PRINT|JSON_UNESCAPED_UNICODE));
    }

    public function storeScores(){
    }
}

$x=new TotalScore();
$x->getIGolf();
$x->storeScores();
