<?php
$apiUrl = 'http://localhost:8000/api/images';
$response = @file_get_contents($apiUrl);
$images = $response ? json_decode($response) : [];
$isEmpty = empty($images);
?>
<!doctype html>
<html lang="fr">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<meta name="robots" content="noindex">
		<title>Emmanuel Béziat :: Images</title>
		<link rel="preconnect" href="https://fonts.googleapis.com">
		<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
		<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&family=Source+Sans+3:ital,wght@0,200..900;1,200..900&family=Yanone+Kaffeesatz:wght@200..700&display=swap">
		<link rel="stylesheet" href="/assets/css/custom-properties.css">
		<link rel="stylesheet" href="/assets/css/base.css">
		<link rel="stylesheet" href="/assets/css/viewer.css">
	</head>
	<body>
		<div class="site">
			<main class="<?= $isEmpty ? 'main' : 'main gallery' ?>">
				<?php if ($isEmpty) : ?>
					<h1>Aucune image</h1>
					<p>Aucune image disponible pour le moment.</p>
				<?php else : ?>
					<?php foreach ($images as $image) : ?>
						<a href="/media/<?= $image->url ?>" class="image" target="_blank">
							<img src="/media/<?= $image->url ?>" alt="<?= htmlspecialchars($image->original_filename) ?>" loading="lazy" decoding="async">
							<div class="image-infos">
								<?= htmlspecialchars($image->original_filename) ?>
							</div>
						</a>
					<?php endforeach; ?>
				<?php endif; ?>
			</main>
		</div>
	</body>
</html>
