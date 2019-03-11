<?php

// Include the parsing library
include_once('dom.php');

// CONFIG VARIABLES
$SEASON = "2018";
$TEAN = "Rio-Natura-Monbus-Obradoiro";

// This function is for debug only, to check the JSON output format
function indent($json) {
    $result      = '';
    $pos         = 0;
    $strLen      = strlen($json);
    $indentStr   = '  ';
    $newLine     = "\n";
    $prevChar    = '';
    $outOfQuotes = true;

    for ($i=0; $i<=$strLen; $i++) {
        $char = substr($json, $i, 1);

        if ($char == '"' && $prevChar != '\\') {
            $outOfQuotes = !$outOfQuotes;
        } else if(($char == '}' || $char == ']') && $outOfQuotes) {
            $result .= $newLine;
            $pos --;
            for ($j=0; $j<$pos; $j++) {
                $result .= $indentStr;
            }
        }

        $result .= $char;
        if (($char == ',' || $char == '{' || $char == '[') && $outOfQuotes) {
            $result .= $newLine;
            if ($char == '{' || $char == '[') {
                $pos ++;
            }

            for ($j = 0; $j < $pos; $j++) {
                $result .= $indentStr;
            }
        }
        $prevChar = $char;
    }
    return $result;
}

function get_home($url, $TEAM) {
    $tmp = substr(str_replace("https://basketball.realgm.com/international/boxscore/", "", $url), 11);
    // CHANGE "Rio-Natura-Monbus-Obradoiro" TO CHANGE THE TEAM FOR THE SCRIPT
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
    print("PROCESSED");
    print("\n");
    print($index+1 . ") " . $url);
    print("\n\n");
}

// Write the JSON file
$f = fopen(__DIR__."/out.json","wb");
fwrite($f, json_encode($content));
fclose($f);



// CONVERT JSON TO CSV
// Based from https://stackoverflow.com/questions/20667418/converting-json-to-csv-format-using-php

$json = file_get_contents(__DIR__."/out.json");
$array = json_decode($json, true);

$desired = true;
$counter = 1;
foreach ($array as $match) {
    // Here we have to think in pairs: first item is desired team stats, and the second one is opponent stats
    // And so on, so  1 is desired  2 is opp  3 is desired  4 is opp
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
