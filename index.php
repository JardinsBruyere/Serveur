<!DOCTYPE html>
<html>
      
<head>
    <link href="style.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>
        Gestionnaire serveur
    </title>
</head>
  
<body>
      
    <h1 style="color:green;  text-align:center;">
        Interface d'administration du serveur
    </h1>
      
    <h3 style="text-align:center;">
        Vous pouvez ici consulter l'état des différents services :
    </h3>
    <br>
    <br>
      
    <div class="card bg-primary text-white">
    <?php
        if(array_key_exists('StateApi', $_POST)) {
            StateApi();
        }
        else if(array_key_exists('StateListen', $_POST)) {
            StateListen();
        }
        function StateApi() {
            $output = shell_exec("sudo systemctl status api | grep Active");
            echo "<h4>Etat de l'API :</h4><p> $output</p>";
        }
        function StateListen() {
            $output = shell_exec("sudo systemctl status listen | grep Active");
            echo "<h4>Etat du listen :</h4><p> $output</p>";
        }
    ?>
    <br>
    <br>
  
    <form method="post">
        <input type="submit" name="StateApi"
                class="button btn btn-primary" value="Etat de l'api" />
          
        <input type="submit" name="StateListen"
                class="btn btn-primary button" value="Etat du listen" />
    </form>
    </div>
    <br>
    <div>
    <h3>
        Etat du serveur :
    </h3>
    <?php
        $url = 'http://localhost:5001/status';
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_HTTPGET, true);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = curl_exec($ch);
        curl_close($ch);
        if ($response=="OK") {
            echo "OK";
        }else{
            echo "Fail";
        }
    ?>
    </div>
    <br>
    </div>

    <div>
    <h3>
        Les différents appels à l'api possibles sont :
    </h3>
    <?php
        $url = 'http://localhost:5001/help';
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_HTTPGET, true);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response_json = curl_exec($ch);
        curl_close($ch);
        $arr = json_decode($response_json, true);
        foreach ($arr as $k=>$v){
            $key=array_keys($v);
            $content=$v[$key[0]];
            echo"<a><a style=\"text-decoration: underline;\">$key[0] :</a> $content</a><br>";
        }
    ?>
    </div>
     <br>
    <div>
    <h3>
        Statistiques :
    </h3>
    <?php
        $output2 = shell_exec("du -sh capteur.db | cut -f1 | sed -e \"s/ //g\"");
        $output = shell_exec("df . | cut -d ' ' -f13");
        echo "<h4>Espace restant (en octet): ${output}";
        echo "<h4>Espace occupé par la base de donnée : $output2";
        
    ?>
    </div>
    <br>
    <div>
    <h3>
        Liste des tables :
    </h3>
    <?php
    $connection = new SQLite3('capteur.db');
    if($connection){
       $tablesquery1 = $connection->query("SELECT name FROM sqlite_master WHERE type='table';");
        while ($table = $tablesquery1->fetchArray(SQLITE3_ASSOC)) {
            $currentTable=$table['name'];
            if($currentTable!="sqlite_sequence"){
                echo '<hr>';
                echo "La table \"$currentTable\" contient:";
                echo '<div class="tableFixHead">';
                $tablesquery2 = $connection->query("PRAGMA table_info($currentTable);");
                $myArray = []; 
                while ($table2 = $tablesquery2->fetchArray(SQLITE3_ASSOC)['name']) {
                    $myArray[]=$table2;
                }

                $results = $connection->query("SELECT * FROM $currentTable");
                echo '<table class="table-wrap table">';
                echo '<thead>';
                echo '<tr class ="thead-dark">';
                foreach($myArray as $currentCol){
                  echo "<td> $currentCol </td>";
                }
               echo '</tr>';
                echo '</thead>';
                echo '<tbody>';
                while($row=$results->fetchArray(SQLITE3_ASSOC)){
                    echo '<tr>';
                    foreach($myArray as $currentCol){
                      echo "<td>$row[$currentCol] </td>";
                    }
                    echo '</tr>';
                }
                echo '</tbody>';
                echo '</table>';
                echo '</div>';
            }
        }
    }
    ?>
    </div>
</head>
  
</html>