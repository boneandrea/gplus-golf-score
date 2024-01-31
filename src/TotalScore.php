<?php
namespace Golf;

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
        return $scores;
    }

    public function getMarshalI(){
        $url="https://marshal-i.com/ops/score/oakvillage_20231219_5d0e4f2f";
        $url="https://marshal-i.com/ops/score/kazusamona_20240123_4fcf31a0";

        $client = new Client(['cookies' => true]);
        $jar = new CookieJar;
        $response = $client->request('GET', $url);

        // ページのコンテンツをDomCrawlerに渡す
        $html = $response->getBody()->getContents();
        $dom = new Crawler($html);

        $tr=$dom->filter("#table_start tr");

        $d=$dom->filter(".panel-heading")->eq(0)->text();
        if(preg_match("/(.*)プレー日：(.*)/", $d, $m)){
            $course=trim($m[1]);
            $date=date_parse_from_format("Y年m月d日",trim($m[2]));
            $date=sprintf("%s/%s/%s",
                    $date["year"],
                    $date["month"],
                    $date["day"],
            );
        }

        $count_members=($tr->count()-4)/2;
        $_pars=$tr->eq(2)->filter("td");

        $pars=[];
        for($i=1;$i<20;$i++){
            $par=$_pars->eq($i);
            $pars[]=intval($par->text());
        }
        unset($pars[9]);
        $pars=array_values($pars);

        $ss=[];
        for($i=0;$i<$count_members;$i++){
            $name=$tr->eq($i*2+3)->filter("td")->eq(0)->text();
            $td=$tr->eq($i*2+3)->filter("td");
            $scores=[];
            for($j=1;$j<20;$j++){
                $score=$td->eq($j);
                $scores[]=intval($score->text());
            }
            unset($scores[9]);
            $scores=array_values($scores);
            $ss[]=[
                "name"=>$name,
                "scores"=>$scores
            ];
        }

        $results=[
            "course"=>$course,
            "date"=>$date,
            "scores"=>[]
        ];
        for($member_index=0;$member_index<$count_members;$member_index++){
            $r=[];
            $s=[];
            $gross=0;
            foreach($pars as $index=>$p){
                $prize=$this->getPrize($p,$ss[$member_index]["scores"][$index]);
                $s[]=[
                    "hole"=>$index+1,
                    "score"=>$ss[$member_index]["scores"][$index],
                    "prize"=>$prize,
                ];
                $gross+=$ss[$member_index]["scores"][$index];
            }
            $r=[
                "name"=>$ss[$member_index]["name"],
                "scores"=>$s,
                "gross"=>$gross
            ];
            $results["scores"][]=$r;

        }
        return $results;
    }

    public function getPrize($par, $score){
        if($score === 1) return "HOLEINONE";
        switch($score - $par){
        case -1:
            return "BIRDIE";
        case -2:
            return "EAGLE";
        case -3:
            return "ALBATROSS";
        case 0:
            return "PAR";
        case 1:
            return "BOGEY";
        case 2:
            return "DOUBLE BOGEY";
        case 3:
            return "TROUBLE BOGEY";
        default:
            return "";
        }
    }

    public function storeScores(){
    }
}
