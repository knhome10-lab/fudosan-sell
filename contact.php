<?php
header('Content-Type: application/json; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Invalid request']);
    exit;
}

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

$to      = 'info@knhome.jp';
$subject = '【KNホーム】不動産売却LP お問い合わせ';

$body  = "■ お問い合わせ内容\n\n";
$body .= "お名前：{$name}\n";
$body .= "電話番号：{$phone}\n";
$body .= "メールアドレス：{$email}\n";
$body .= "物件の種類：{$type}\n";
$body .= "エリア：{$area}\n";
$body .= "ご相談内容：\n{$message}\n\n";
$body .= "--------------------\n";
$body .= "送信日時：" . date('Y/m/d H:i:s') . "\n";
$body .= "送信元：https://knhome.jp/fudosan-sell/\n";

$headers  = "From: noreply@knhome.jp\r\n";
$headers .= "Reply-To: {$email}\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

mb_language('Japanese');
mb_internal_encoding('UTF-8');

$result = mb_send_mail($to, $subject, $body, $headers);

if ($result) {
    echo json_encode(['success' => true, 'message' => 'お問合せありがとうございました']);
} else {
    echo json_encode(['success' => false, 'message' => '送信に失敗しました。お電話にてご連絡ください。']);
}
?>
