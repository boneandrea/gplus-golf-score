<?php

namespace Golf;

require "vendor/autoload.php";
use Symfony\Component\DomCrawler\Crawler;
use GuzzleHttp\Client;
use GuzzleHttp\Cookie\CookieJar;

ini_set('xdebug.var_display_max_children', -1);
ini_set('xdebug.var_display_max_data', -1);
ini_set('xdebug.var_display_max_depth', -1);

class TotalScore
{
    public function getIGolf()
    {
        // Guzzleを使用してWebページを取得
        $url0 = "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre#/landscape-a";
        $url1 = "https://v2anegasaki.igolfshaper.com/anegasaki/score/2nf6slre/leaderboard";

        $client = new Client(['cookies' => true]);
        $response = $client->request('GET', $url0);
        $response = $client->request('GET', $url1);

        // ページのコンテンツをDomCrawlerに渡す
        $html = $response->getBody()->getContents();
        $dom = new Crawler($html);

        $tr = $dom->filter(".ui-table-view tr");

        $count_members = $tr->count() - 2;

        $scores = [];

        for($i = 0;$i < $count_members;$i++) {
            $score = $tr->eq($i + 2);
            $scores[] = [
                "name" => $score->filter("td")->eq(1)->text(),
                "gross" => intval($score->filter("td")->eq(28)->text())
            ];
        }
        return $scores;
    }

    public function getMarshalI()
    {
        $url = "https://marshal-i.com/ops/score/oakvillage_20231219_5d0e4f2f";
        $url = "https://marshal-i.com/ops/score/kazusamona_20240123_4fcf31a0";
        $url = "https://marshal-i.com/ops/score/oakvillage_20231031_7bf14538";

        $client = new Client(['cookies' => true]);
        $response = $client->request('GET', $url);

        // ページのコンテンツをDomCrawlerに渡す
        $html = $response->getBody()->getContents();
        $dom = new Crawler($html);

        $table = $dom->filter("table.holebyholeTable")->eq(0);
        $tr = $table->filter("tbody tr");

        $d = $dom->filter(".panel-heading")->eq(0)->text();
        if(preg_match("/(.*)プレー日：(.*)/", $d, $m)) {
            $course = trim($m[1]);
            $date = date_parse_from_format("Y年m月d日", trim($m[2]));
            $date = sprintf(
                "%s/%s/%s",
                $date["year"],
                $date["month"],
                $date["day"],
            );
        }

        $count_members = $tr->count() - 1;

        $pars = [];
        for($i = 0;$i < 18;$i++) {
            $par = $table->filter("thead tr")->eq(1)->filter("th")->eq($i)->text();
            $pars[] = intval($par);
        }
        $all_par = array_sum($pars);

        $scores = [];
        for($i = 0;$i < $count_members;$i++) {
            $name = $tr->eq($i)->filter("td")->eq(1)->text();
            $td = $tr->eq($i)->filter("td");
            $_scores = [];
            for($j = 0;$j < 20;$j++) {
                $_scores[] = intval($td->eq(3 + $j)->filter("span")->eq(0)->attr("data-par"));
            }
            unset($_scores[9]);
            unset($_scores[19]);
            // add par
            $gross = 0;
            $_scores = array_values($_scores);
            $score = array_map(function ($e, $index) use ($pars, &$gross) {
                $gross += $e + $pars[$index];
                $prize = $this->getPrize(diff:$e);
                return[
                    "hole" => $index + 1,
                    "score" => $e + $pars[$index],
                    "prize" => $prize,
                ];
            }, $_scores, range(0, 17));

            $scores[] = compact("name", "score", "gross");
        }

        $results = [
            "course" => $course,
            "date" => $date,
            "par" => $all_par,
            "scores" => $scores,
        ];

        return $results;
    }

    public function getPrize($diff = 0, $score = 0)
    {
        if($score === 1) {
            return "HOLEINONE";
        }
        switch($diff) {
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
                return "DOUBLEBOGEY";
            case 3:
                return "TRIPLEBOGEY";
            default:
                return "";
        }
    }

    public function storeScores()
    {
    }
}
