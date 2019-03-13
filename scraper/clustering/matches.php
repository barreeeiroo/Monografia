<?php

ini_set('error_reporting', E_ALL & ~E_NOTICE & ~E_STRICT & ~E_DEPRECATED); 

// Incluir la librería de parsing
include_once(__DIR__.'/../dom.php');


// Variables de Configuración
$SEASON = "2018";
$LEAGUE = "55"; // Spanish-LEB-Gold
$MAX_PAGES = 2;

$POSITIONS = ['PG', 'SG', 'SF', 'PF', 'C'];



$out = array();
$keys = array();
$page = 1;

while ($page<=$MAX_PAGES) {
    $URL = "https://basketball.realgm.com/international/league/".$LEAGUE."/League/stats/".$SEASON."/Averages/Qualified/All/points/All/desc/".$page;

    $html = str_get_html(file_get_contents($URL));
    $table = $html->find('table[class=tablesaw]')[0];

    foreach($table->find('tr') as $row) {
        if (!empty($keys)) {
            $rowData = array();
            $i = 0;
            foreach($row->find('td') as $cell) {
                $txt = str_get_html($cell->innertext)->find('a')[0]->innertext;
                $rowData[$keys[$i]] = empty($txt)?$cell->innertext:$txt;
                $i++;
            }
            $out[] = $rowData;
        }
        if (empty($keys)) {
            foreach($row->find('th') as $cell) {
                $txt = str_get_html($cell->innertext)->find('a')[0]->innertext;
                $keys[] = empty($txt)?$cell->innertext:$txt;
            }
        }
    }
    $page++;
}

$f = fopen(__DIR__."/out1.json","wb");
fwrite($f, json_encode($out));
fclose($f);
print("FINISHED AVERAGES\n");



$out = array();
$keys = array();

foreach ($POSITIONS as $id => $pos) {
    $URL = "https://basketball.realgm.com/international/league/".$LEAGUE."/League/stats/".$SEASON."/Advanced_Stats/Qualified/All/points/".$pos."/desc/1";

    $html = str_get_html(file_get_contents($URL));
    $table = $html->find('table[class=tablesaw]')[0];

    foreach($table->find('tr') as $row) {
        if (!empty($keys)) {
            $rowData = array();
            $i = 0;
            foreach($row->find('td') as $cell) {
                $txt = str_get_html($cell->innertext)->find('a')[0]->innertext;
                $rowData[$keys[$i]] = empty($txt)?$cell->innertext:$txt;
                $i++;
            }
            $rowData['POS'] = $id;
            $out[] = $rowData;
        }
        if (empty($keys)) {
            foreach($row->find('th') as $cell) {
                $txt = str_get_html($cell->innertext)->find('a')[0]->innertext;
                $keys[] = empty($txt)?$cell->innertext:$txt;
            }
        }
    }
    print("FINISHED ".$pos." (".$id.")\n");
}

$f = fopen(__DIR__."/out2.json","wb");
fwrite($f, json_encode($out));
fclose($f);



// UNIR AMBOS ARCHIVOS
$f1 = json_decode(file_get_contents(__DIR__.'/out1.json'), true);
$f2 = json_decode(file_get_contents(__DIR__.'/out2.json'), true);
$f0 = array();

foreach ($f1 as $player1) {
    foreach ($f2 as $player2) {
        if ($player1['Player'] == $player2['Player'] && preg_match("/[a-z]/i", $player1['Player'])) {
            $f0[] = array_merge($player1, $player2);
            break;
        }
    }
}

$f = fopen(__DIR__."/out.json","wb");
fwrite($f, json_encode($f0));
fclose($f);






// CONVERTIR JSON A CSV
// Basado en https://stackoverflow.com/questions/20667418/converting-json-to-csv-format-using-php

$array = json_decode(file_get_contents(__DIR__.'/out.json'), true);

$firstLineKeys = false;
$f = fopen(__DIR__.'/out.csv', 'wb');
foreach ($array as $player) {
    if (empty($firstLineKeys)) {
        $firstLineKeys = array_keys($player);
        fputcsv($f, $firstLineKeys);
        $firstLineKeys = array_flip($firstLineKeys);
    }
    fputcsv($f, array_merge($firstLineKeys, $player));
}



?>
