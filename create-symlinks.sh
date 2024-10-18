#!/bin/bash

# Define the source file and the target directory using absolute paths
SOURCE="$(pwd)/pages/viewer.php"  # Get the absolute path to the source file
TARGET_DIR="$(pwd)/media"          # Get the absolute path to the target directory

# Find all directories in the target directory, excluding .well-known, and create a symlink
find "$TARGET_DIR" -type d -not -path "$TARGET_DIR/.well-known/*" -exec sh -c '
    for dir; do
        echo "Processing directory: $dir"
        SYMLINK="$dir/viewer.php"
        if [ ! -e "$SYMLINK" ]; then
            echo "Creating symlink in: $dir"
            ln -s "$0" "$SYMLINK"  # Use "$0" to refer to the SOURCE variable passed as the first argument
        else
            echo "Symlink already exists in: $dir"
        fi
    done
' "$SOURCE" {} +
