<?php

// Incluir la librería de parsing
include_once(__DIR__.'/../dom.php');

// VARIABLES DE CONFIGURACIÓN
$SEASON = "2018";
$TEAN = "Rio-Natura-Monbus-Obradoiro";

function get_home($url, $TEAM) {
    $tmp = substr(str_replace("https://basketball.realgm.com/international/boxscore/", "", $url), 11);
    if (substr($tmp, 0, strlen($TEAM)) === $TEAM) {
        return 1;
    }
    return 2;
}

$URL = "https://basketball.realgm.com/international/league/4/Spanish-ACB/team/651/".$TEAM."/schedule/".$SEASON;

$urls = array();
$all = file_get_contents($URL); 

preg_match_all('/\/international\/boxscore\/(.*?)\"/s', $all, $matches);
foreach ($matches[0] as $path) {
    $urls[] = "https://basketball.realgm.com".rtrim($path,"\"");
}

$content = array();
foreach ($urls as $index => $url) {
    $html = str_get_html(file_get_contents($url));

    $i = 1;
    foreach($html->find('table[class=tablesaw]') as $element) {
        if ($i == get_home($url, $TEAM)) {
            $table = $element;
            break;
        }
        $i++;
    }
    $out = array();
    $keys = array();
    $skip = false;
    foreach($table->find('tr') as $row) {
        if ($skip) {
            break;
        }
        if (!empty($keys)) {
            $rowData = array();
            $i = 0;
            foreach($row->find('td') as $cell) {
                if ($cell->innertext == "Team") {
                    $skip = true;
                }
                $rowData[$keys[$i]] = $cell->innertext;
                $i++;
            }
            $out[] = $rowData;
        }
        foreach($row->find('th') as $cell) {
            $keys[] = $cell->innertext;
        }
    }
    $content[] = $out;

    $i = 1;
    foreach($html->find('table[class=tablesaw]') as $element) {
        if ($i != get_home($url, $TEAM)) {
            $table = $element;
            break;
        }
        $i++;
    }
    $out = array();
    $keys = array();
    $skip = false;
    foreach($table->find('tr') as $row) {
        if ($skip) {
            break;
        }
        if (!empty($keys)) {
            $rowData = array();
            $i = 0;
            foreach($row->find('td') as $cell) {
                if ($cell->innertext == "Team") {
                    $skip = true;
                }
                $rowData[$keys[$i]] = $cell->innertext;
                $i++;
            }
            $out[] = $rowData;
        }
        foreach($row->find('th') as $cell) {
            $keys[] = $cell->innertext;
        }
    }

    $content[] = $out;
    print("PROCESADO");
    print("\n");
    print($index+1 . ") " . $url);
    print("\n\n");
}

// Escribir el archivo JSON
$f = fopen(__DIR__."/out.json","wb");
fwrite($f, json_encode($content));
fclose($f);



// CONVERTIR DE JSON A CSV
// Basado en https://stackoverflow.com/questions/20667418/converting-json-to-csv-format-using-php

$json = file_get_contents(__DIR__."/out.json");
$array = json_decode($json, true);

$desired = true;
$counter = 1;
foreach ($array as $match) {
    // Aquí hay que pensar en parejas: el primer archivo es el del equipo deseado, el segundo del rival
    // Y así siempre, entonces  1 es deseado  2 es oppnente  3 es deseado  4 es oponente
    $f = fopen(__DIR__.'/csv/output'.$counter.($desired?"A":"B").'.csv', 'wb');
    $firstLineKeys = false;
    foreach ($match as $value) {
        if (empty($firstLineKeys)) {
                $firstLineKeys = array_keys($value);
                fputcsv($f, $firstLineKeys);
                $firstLineKeys = array_flip($firstLineKeys);
        }
        fputcsv($f, array_merge($firstLineKeys, $value));
    }
    if ($desired == false) {
        $counter = $counter+1;
    }
    $desired = ($desired?false:true);
}

?>
