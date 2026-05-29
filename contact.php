<?php
header('Content-Type: application/json; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Invalid request']);
    exit;
}

mb_language('uni');
mb_internal_encoding('UTF-8');

$name     = isset($_POST['name'])    ? htmlspecialchars(trim($_POST['name']),    ENT_QUOTES, 'UTF-8') : '';
$phone    = isset($_POST['phone'])   ? htmlspecialchars(trim($_POST['phone']),   ENT_QUOTES, 'UTF-8') : '';
$email    = isset($_POST['email'])   ? htmlspecialchars(trim($_POST['email']),   ENT_QUOTES, 'UTF-8') : '';
$type     = isset($_POST['type'])    ? htmlspecialchars(trim($_POST['type']),    ENT_QUOTES, 'UTF-8') : '';
$area     = isset($_POST['area'])    ? htmlspecialchars(trim($_POST['area']),    ENT_QUOTES, 'UTF-8') : '';
$message  = isset($_POST['message']) ? htmlspecialchars(trim($_POST['message']), ENT_QUOTES, 'UTF-8') : '';

if (empty($name) || empty($phone)) {
    echo json_encode(['success' => false, 'message' => '必須項目を入力してください']);
    exit;
}

// 送信先・件名
$to      = 'info@knhome.jp';
$subject = '【不動産売却LP】お問い合わせが届きました';

// メール本文
$body  = "不動産売却LPよりお問い合わせがありました。\n\n";
$body .= "■ お客様情報\n";
$body .= "お名前　　　：{$name}\n";
$body .= "電話番号　　：{$phone}\n";
$body .= "メールアドレス：" . (!empty($email) ? $email : '未入力') . "\n";
$body .= "物件の種類　：{$type}\n";
$body .= "所在地　　　：{$area}\n\n";
$body .= "■ ご相談内容\n";
$body .= (!empty($message) ? $message : '未入力') . "\n\n";
$body .= "--------------------\n";
$body .= "送信日時：" . date('Y/m/d H:i:s') . "\n";
$body .= "送信元URL：https://knhome.jp/fudosan-sell/\n";

// ヘッダー（UTF-8 base64エンコード）
$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$encodedBody    = base64_encode($body);

$headers  = "From: info@knhome.jp\r\n";
if (!empty($email)) {
    $headers .= "Reply-To: {$email}\r\n";
}
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: base64\r\n";
$headers .= "X-Mailer: PHP/" . phpversion() . "\r\n";

$result = mail($to, $encodedSubject, $encodedBody, $headers);

if ($result) {
    echo json_encode(['success' => true, 'message' => 'お問合せありがとうございました']);
} else {
    echo json_encode(['success' => false, 'message' => '送信に失敗しました。お電話（0800-919-5566）にてご連絡ください。']);
}
?>
