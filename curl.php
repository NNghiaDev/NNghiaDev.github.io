<?php
$pasteId = 'kWqVsaUA'; // Thay thế bằng ID paste bạn muốn lấy
$url = "https://pastebin.com/raw/{$pasteId}"; // Đường dẫn raw của paste

// Khởi tạo cURL session
$ch = curl_init();

// Thiết lập các tùy chọn cho cURL
curl_setopt($ch, CURLOPT_URL, $url); // URL cần lấy dữ liệu
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); // Chuyển kết quả trả về dưới dạng chuỗi thay vì in trực tiếp
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0'); // Tạo user-agent giả, tương tự như khi dùng curl trong terminal

// Thực thi cURL và nhận dữ liệu
$response = curl_exec($ch);

// Kiểm tra lỗi cURL
if(curl_errno($ch)) {
    echo 'Lỗi cURL: ' . curl_error($ch);
} else {
    // In kết quả (nội dung của paste)
    echo '<div>' . htmlspecialchars($response) . '</div>';
}

// Đóng cURL session
curl_close($ch);
?>
