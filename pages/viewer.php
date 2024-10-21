<?php

function convertOctets ($octet, $round) {
	$unite_spec = ['o', 'Ko', 'Mo', 'Go', 'To'];
	$count = 0;
	$c = count($unite_spec);

	while ($octet >= 1024 && $count < $c - 1) {
		$count++;
		$octet /= 1024;
	}

	$number = $round >= 0
		? round($octet * 10 ** $round) / 10 ** $round
		: $octet;

	return str_replace(".", ",", sprintf('%s %s', $number, $unite_spec[$count]));
}

$files = array_filter(iterator_to_array(new DirectoryIterator('./')), fn($fileInfo) =>
	!$fileInfo->isDot() && !$fileInfo->isDir() && !$fileInfo->isLink() && !in_array($fileInfo->getExtension(), ['php', 'html'])
);

$files = array_map(fn($fileInfo) => (object) [
	'path' => htmlspecialchars($fileInfo->getPathname()),
	'name' => htmlspecialchars($fileInfo->getFilename()),
	'size' => convertOctets($fileInfo->getSize(), 2)
], $files);

asort($files);
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
	</head>

	<body>
		<div class="site">
			<main class="main">
				<?php if (empty($files)): ?>
					<h1 class="h2">Il n’y a rien à voir ici</h2>

				<?php else : ?>
					<div class="gallery">
						<?php foreach ($files as $file) : ?>
						<a href="<?= $file->path ?>" class="image">
							<img src="<?= $file->name ?>" alt="<?= $file->name ?>" loading="lazy">
							<div class="image-infos">
								<?= $file->name ?> <br>(<?= $file->size ?>)
							</div>
						</a>
						<?php endforeach; ?>
					</div>
				<?php endif; ?>
			</main>
		</div>
	</body>
</html>
