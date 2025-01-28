<?php

function convertOctets ($octet, $round) {
	$unite_spec = ['o', 'Ko', 'Mo', 'Go', 'To'];
	$count = 0;
	$c = count($unite_spec);

	while ($octet >= 1024 && $count < $c - 1) {
		$count++;
		$octet /= 1024;
	}

	$number = $round >= 0 ? round($octet * 10 ** $round) / 10 ** $round : $octet;

	return str_replace(".", ",", sprintf('%s %s', $number, $unite_spec[$count]));
}

$directory = dirname($_SERVER['SCRIPT_FILENAME']);
$allItems = new DirectoryIterator($directory);
$files = [];

foreach ($allItems as $fileInfo) {
	if (!$fileInfo->isDot() && !$fileInfo->isDir() && !$fileInfo->isLink() && !in_array(strtolower($fileInfo->getExtension()), ['php', 'html']) ) {
		$files[] = (object) [
			'path' => htmlspecialchars($fileInfo->getPathname()),
			'name' => htmlspecialchars($fileInfo->getFilename()),
			'size' => convertOctets($fileInfo->getSize(), 2)
		];
	}
}

asort($files);

if (empty($files)) {
	header("Location: /404.html");
	exit;
}
?>
<!doctype html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta name="robots" content="noindex">
		<link rel="shortcut icon" href="https://www.emmanuelbeziat.com/favicons/favicon-16x16.png">

		<title>Emmanuel Béziat :: Image viewer</title>
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Source+Sans+3:ital,wght@0,200..900;1,200..900&family=Yanone+Kaffeesatz:wght@200..700&display=swap">
		<link rel="stylesheet" href="/assets/css/custom-properties.css">
		<link rel="stylesheet" href="/assets/css/base.css">
		<link rel="stylesheet" href="/assets/css/viewer.css">
		<link rel="icon" type="image/png" href="assets/favicons/favicon-96x96.png?v=1" sizes="96x96">
		<link rel="icon" type="image/svg+xml" href="assets/favicons/favicon.svg?v=1">
		<link rel="shortcut icon" href="assets/favicons/favicon.ico?v=1">
		<link rel="apple-touch-icon" sizes="180x180" href="assets/favicons/apple-touch-icon.png?v=1">
		<meta name="apple-mobile-web-app-title" content="EB::Images">
		<link rel="manifest" href="assets/favicons/site.webmanifest">
		<script defer src="https://unpkg.com/@popperjs/core@2"></script>
		<script defer src="https://unpkg.com/tippy.js@6"></script>
		<script defer src="/assets/js/viewer.js"></script>
		<script defer>
			new Viewer(document.querySelectorAll('[data-action="copy"]'))
		</script>
	</head>

	<body>
		<div class="site">
			<main class="main gallery">
				<?php foreach ($files as $file) : ?>
				<a href="<?= $file->name ?>" class="image" data-action="copy">
					<img src="<?= $file->name ?>" alt="<?= $file->name ?>" loading="lazy">
					<div class="image-infos">
						<?= $file->name ?> <br>(<?= $file->size ?>)
					</div>
				</a>
				<?php endforeach; ?>
			</main>
		</div>
	</body>
</html>
