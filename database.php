<!DOCTYPE html>
<html>

<head>
    <link href="style.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.min.css">

    <script defer src="https://use.fontawesome.com/releases/v5.0.13/js/solid.js" integrity="sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ" crossorigin="anonymous"></script>
    <script defer src="https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js" integrity="sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY" crossorigin="anonymous"></script>


    <title>
        Gestionnaire serveur
    </title>
</head>

<body>
<div class="wrapper">
  <div class="log"></div>

      <div id="header-margin"></div>
        <!-- Page Content  -->
        <div id="content">

          <div class="log2"></div>
        <div>
        <script src="function.js"></script>
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
                echo '<table class="table-wrap table sortable maTable">';
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
     <div class="overlay"></div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.concat.min.js"></script>

    <script type="text/javascript">
        $(document).ready(function () {
            $("#sidebar").mCustomScrollbar({
                theme: "minimal"
            });

            $('#dismiss, .overlay').on('click', function () {
                $('#sidebar').removeClass('active');
                $('.overlay').removeClass('active');
            });

            $('#sidebarCollapse').on('click', function () {
                $('#sidebar').addClass('active');
                $('.overlay').addClass('active');
                $('.collapse.in').toggleClass('in');
                $('a[aria-expanded=true]').attr('aria-expanded', 'false');
            });
        });
    </script>
</body>

</html>
