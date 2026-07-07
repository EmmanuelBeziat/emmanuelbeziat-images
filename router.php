<?php
$uri = $_SERVER['REQUEST_URI'];
$path = parse_url($uri, PHP_URL_PATH);

$frontendPath = __DIR__ . '/frontend' . $path;
$mediaPath = __DIR__ . '/media' . $path;

if (file_exists($frontendPath) && !is_dir($frontendPath)) {
    if (substr($path, -4) === '.php') {
        require $frontendPath;
        return true;
    }
    return false;
}

if (substr($path, 0, 7) === '/media/' && file_exists($mediaPath) && !is_dir($mediaPath)) {
    $mimeTypes = [
        'jpg' => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'png' => 'image/png',
        'gif' => 'image/gif',
        'webp' => 'image/webp',
        'avif' => 'image/avif',
        'svg' => 'image/svg+xml',
        'bmp' => 'image/bmp',
        'heic' => 'image/heic',
        'mp4' => 'video/mp4',
        'webm' => 'video/webm',
        'mov' => 'video/quicktime'
    ];
    $ext = strtolower(pathinfo($mediaPath, PATHINFO_EXTENSION));
    $mime = isset($mimeTypes[$ext]) ? $mimeTypes[$ext] : 'application/octet-stream';
    header('Content-Type: ' . $mime);
    header('Content-Length: ' . filesize($mediaPath));
    readfile($mediaPath);
    return true;
}

if (substr($path, -4) === '.php') {
    http_response_code(404);
    echo '404 Not Found';
    return true;
}

return false;
