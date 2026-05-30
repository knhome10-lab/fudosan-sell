<?php
$result = mail('info-mail@knhome.jp', 'mailtest', 'test body', 'From: info-mail@knhome.jp');
echo $result ? 'OK' : 'NG';
echo '<br>';
echo 'PHP: ' . PHP_VERSION;
echo '<br>';
$e = error_get_last();
echo 'Error: ' . ($e ? $e['message'] : 'none');
?>
