<!DOCTYPE html>
<html>
      
<head>
    <link href="style.css" rel="stylesheet">
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
      
    <div>
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
                class="button" value="Etat de l'api" />
          
        <input type="submit" name="StateListen"
                class="button" value="Etat du listen" />
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
        $output = shell_exec("du -sh capteur.db | cut -f1 | sed -e \"s/ //g\"");
        echo "<h4>Espace restant (en octet): :${output}";
        $output2 = shell_exec("df . | cut -d ' ' -f13");
        echo "<h4>Espace occupé par la base de donnée : :$output2";
        
    ?>
    </div>
    <br>
</head>
  
</html>