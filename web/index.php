

<?php
error_reporting(-1);
ini_set('display_errors',1);
$page = $_GET['page'] ?? 'main';
?>

<html>
<head>
    <title>Удаление фона</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
    <script type="text/javascript" src="script.js"></script>
    <!-- Подключить скрипты для драг дроп -->
</head>
<body>
<header>
    <img src="MyLogo.png" alt="Logo">
    <div>
        <h3>Удалите фон из фотографии</h3>
        <p>Бесплатно и без ограничений</p>
    </div>
</header>

<main role="main">
    <?php include basename($page).'.php'; ?>
</main>


<footer>
    <div>
        <p>Вы так же можете воспользоваться ботом для удаления фона фото в telegram.</p>
        <p>Автор - <a href="https://portfolio.devopalev.ru" target="_blank">DevOpalev</a></p>
    </div>
</footer>
</body>
</html>