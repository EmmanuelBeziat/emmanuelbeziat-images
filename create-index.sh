#!/bin/bash

# Define the source file and the target directory
SOURCE="$(pwd)/pages/viewer.php"  # Absolute path to the viewer.php file
TARGET_DIR="$(pwd)/media"          # Absolute path to the media directory

# Find all directories in the target directory, excluding .well-known, and create an index.php file
find "$TARGET_DIR" -type d -not -path "$TARGET_DIR/.well-known/*" -exec sh -c '
    for dir; do
        INDEX_FILE="$dir/index.php"
        if [ ! -e "$INDEX_FILE" ]; then
            echo "Creating index.php in: $dir"
            echo "<?php include \"$0\"; ?>" > "$INDEX_FILE"  # Create index.php that includes viewer.php
        else
            echo "index.php already exists in: $dir"
        fi
    done
' "$SOURCE" {} +
