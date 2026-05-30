<?php
mb_language('Japanese');
mb_internal_encoding('UTF-8');

// テスト1: mail()
$r1 = mail('info-mail@knhome.jp', 'mail test', 'test body', 'From: info-mail@knhome.jp');
echo 'mail(): ' . ($r1 ? 'OK' : 'NG') . '<br>';

// テスト2: mb_send_mail
$r2 = mb_send_mail('info-mail@knhome.jp', 'mbテスト', 'テスト本文', 'From: info-mail@knhome.jp');
echo 'mb_send_mail(): ' . ($r2 ? 'OK' : 'NG') . '<br>';

// テスト3: mail()で日本語
$r3 = mail('info-mail@knhome.jp',
    '=?UTF-8?B?' . base64_encode('日本語テスト') . '?=',
    'テスト本文',
    "From: info-mail@knhome.jp\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n"
);
echo 'mail() 日本語: ' . ($r3 ? 'OK' : 'NG') . '<br>';

$e = error_get_last();
echo 'Error: ' . ($e ? $e['message'] : 'none');
?>
