#!/bin/bash

# Define the source file and the target directory
SOURCE="$(pwd)/pages/viewer.php"  # Absolute path to the viewer.php file
TARGET_DIR="$(pwd)/media"          # Absolute path to the media directory

# Find all directories in the target directory, excluding .well-known, and create or update index.php
find "$TARGET_DIR" -type d -not -path "$TARGET_DIR/.well-known/*" -exec sh -c '
	for dir; do
		INDEX_FILE="$dir/index.php"
		NEW_CONTENT="<?php include \"$0\"; ?>"

		if [ -e "$INDEX_FILE" ]; then
			# Compare existing content with new content
			if ! cmp -s <(echo "$NEW_CONTENT") "$INDEX_FILE"; then
				echo "Updating index.php in: $dir"
				echo "$NEW_CONTENT" > "$INDEX_FILE"
			else
				echo "index.php is already up to date in: $dir"
			fi
		else
			echo "Creating index.php in: $dir"
			echo "$NEW_CONTENT" > "$INDEX_FILE"
		fi
	done
' "$SOURCE" {} +
