<?php
error_reporting(-1);
phpinfo();
// Если кнопка нажата, то выполняет тело условия
if ($_FILES) {

    echo "файлы на месте!<br>";
    print_r($_FILES);
    echo $_FILES['images']['name']['0'];

    $fp = fopen($_FILES['images']['tmp_name']['0'], "r");

    $ch = curl_init("http://localhost:8065/delete_background");
    curl_setopt($ch, CURLOPT_URL, "http://localhost:8065/delete_background");
    curl_setopt($ch, CURLOPT_UPLOAD, 1);
    curl_setopt($ch, CURLOPT_TIMEOUT, 86400); // 1 Day Timeout
    curl_setopt($ch, CURLOPT_INFILE, $fp);

    $response = curl_exec($ch);
    $info = curl_getinfo($ch);

    if ($info['http_code'] == 200) {
        echo 'good';
    } else {
        echo 'bad';
    }
}
?>
