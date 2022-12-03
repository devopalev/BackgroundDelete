<html>
<head>
    <title>Удаление фона</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
    <script type="text/javascript" src="script.js"></script>
</head>
<body>
<header>
    <a href="/"><img src="MyLogo.png" alt="Logo"></a>
    <div>
        <h3>Удалите фон из фотографии</h3>
        <p>Бесплатно и без ограничений</p>
    </div>
</header>

<main role="main">
    <h2 id="upload-header">Поехали!</h2>
    <form id="upload-container" method="POST" action="send.php">
        <img id="upload-image" src="upload.svg" alt="upload">
        <div>
            <input id="file-input" type="file" name="file" multiple>
            <label for="file-input">Выберите файл</label>
            <br><span>или перетащите его сюда</span>
            <br><i>(jpg, jpeg, png)</i>
        </div>
    </form>

    <div class="loader">
        <div class="inner one"></div>
        <div class="inner two"></div>
        <div class="inner three"></div>
    </div>
</main>


<footer>
    <div>
        <p>Вы так же можете воспользоваться ботом для удаления фона фото в telegram.</p>
        <p>Автор - <a href="https://portfolio.devopalev.ru" target="_blank">DevOpalev</a></p>
    </div>
</footer>
</body>
</html>