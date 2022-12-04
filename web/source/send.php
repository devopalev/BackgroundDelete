<?php
if ($_FILES) {
    $type = $_FILES['images']['type']['0'];
    if ($type == "image/jpeg" || $type == "image/png"|| $type == "image/jpg") {
        $postFields = ['file' => new CURLFile($_FILES['images']['tmp_name']['0'])];

        $ch = curl_init("http://" . $_ENV["EDIT_IMAGES_HOST"] . ":8080/delete_background");
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_HEADER, false);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);

        $response = curl_exec($ch);
        $info = curl_getinfo($ch);

        $curl_errno = curl_errno($ch);
        curl_close($ch);

        if ($curl_errno == 0 and $info['http_code'] == 200) {
                header('Content-Description: File Transfer');
                header('Content-Type: ' . $type);
                header('Content-Disposition: attachment; filename=' . $_FILES['images']['name']['0']);
                header('Expires: 0');
                header('Cache-Control: must-revalidate');
                header('Pragma: public');
                header('Content-Length: ' . strlen($response));

                echo $response;
                exit();
        }
    }
}
http_response_code(500);
echo '500 Internal Server Error :(';
?>
