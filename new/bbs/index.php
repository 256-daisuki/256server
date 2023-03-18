<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>256server|開発中 256ch</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>

<body>
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#" style="color: azure;">256</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">made</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">bbs</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">overview</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <h1>256ch</h1>
    <?php
    $datafile = "bbs.txt";
    if (!file_exists($datafile)) {
        touch($datafile);
    }
    $data = file($datafile, FILE_IGNORE_NEW_LINES);
    if (count($data) >= 9999) {
        echo "このスレッドは9999書き込みを超えたので、封鎖されました。";
    } else {
        include "form.php";
    }
    include "list.php";
    ?>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
        crossorigin="anonymous"></script>
</body>

</html>