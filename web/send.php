<?php

if ($_FILES) {
    $fp = fopen($_FILES['images']['tmp_name']['0'], "r");

    $postFields = ['file' => new CURLFile($_FILES['images']['tmp_name']['0'])];

    $ch = curl_init("http://localhost:8065/delete_background");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_HEADER, false);

    $response = curl_exec($ch);
    $info = curl_getinfo($ch);

    if ($info['http_code'] == 200) {
        header('Content-Description: File Transfer');
        header('Content-Type: image/jpg');
        header('Content-Disposition: attachment; filename=' . $_FILES['images']['name']['0']);
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . strlen($response));

        echo $response;
        exit();
    }
}
http_response_code(500);
echo 'Упс! Что-то пошло не так :(';
?>
