node2 =document.getElementsByClassName("log2")[0]
node2.insertAdjacentHTML('afterend', '<nav class="navbar navbar-expand-lg navbar-light bg-light">\
    <div class="container-fluid">\
\
        <button type="button" id="sidebarCollapse" class="btn btn-info">\
            <i class="fas fa-align-left"></i>\
            <span>Menu</span>\
        </button>\
        <button class="btn btn-dark d-inline-block d-lg-none ml-auto" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">\
            <i class="fas fa-align-justify"></i>\
        </button>\
        <h1 style="color:green;  text-align:center;">\
            Interface d\'administration du serveur\
        </h1>\
        <div class="collapse navbar-collapse" id="navbarSupportedContent">\
            <ul class="nav navbar-nav ml-auto">\
                <li class="nav-item active">\
                    <a class="nav-link"><button onclick="sendMail(); return false">Nous contacter</button></a>\
                </li>\
                <li class="nav-item">\
                    <a class="nav-link" href="#">Page</a>\
                </li>\
                <li class="nav-item">\
                    <a class="nav-link" href="#">Page</a>\
                </li>\
                <li class="nav-item">\
                    <a class="nav-link" href="#">Page</a>\
                </li>\
            </ul>\
        </div>\
    </div>\
</nav>');

node =document.getElementsByClassName("log")[0]
node.insertAdjacentHTML('afterend', '<nav id="sidebar">\
        <div id="dismiss">\
            <i class="fas fa-arrow-left"></i>\
        </div>\
\
        <div class="sidebar-header">\
            <h3>Jardin de la bruyere</h3>\
        </div>\
\
        <ul class="list-unstyled components">\
            <p>Fonctionnalités</p>\
            <li>\
                <a class="blackColor" href="index.php">Accueil</a>\
            </li>\
            <li class="active">\
                <a class="blackColor" href="#homeSubmenu" data-toggle="collapse" aria-expanded="false">Statistiques</a>\
                <ul class="collapse list-unstyled" id="homeSubmenu">\
                    <li>\
                        <a class="blackColor sousCat" href="service.php">Etat des services</a>\
                    </li>\
                    <li>\
                        <a class="blackColor sousCat"  href="informationAPI.php">Information de l\'api</a>\
                    </li>\
                    <li>\
                        <a class="blackColor sousCat" href="stockage.php">Stockage</a>\
                    </li>\
                </ul>\
            </li>\
            <li>\
                <a class="blackColor" href="about.php">About</a>\
            </li>\
            <li>\
                <a class="blackColor" href="database.php">Database</a>\
            </li>\
            <li>\
                <a class="blackColor" href="contact.php">Contact</a>\
            </li>\
        </ul>\
\
        <ul class="list-unstyled CTAs">\
            <li>\
                <a class="blackColor" href="https://github.com/JardinsBruyere" class="download">Le projet</a>\
            </li>\
            <li>\
                <a class="blackColor" href="https://www.esiea.fr/" class="article">Notre école</a>\
            </li>\
        </ul>\
    </nav>');


function sendMail() {
    var link = "mailto:JardinBruyere@et.esiea.fr";
    window.location.href = link;
}
