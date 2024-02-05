#!/bin/bash

# Check if the current branch is 'main'
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" == "main" ]; then
    # Compare the latest commit with its previous commit
    changed_items=$(git diff --name-only HEAD HEAD~1)
else
    # Fetch the main branch
    git fetch origin main:main

    # Compare the current branch with the main branch
    changed_items=$(git diff --name-only HEAD main)
fi

# Initialize an empty string to hold the names of changed top-level directories
changed_dirs=""

# Loop through each item and process
for item in $changed_items; do
    # Extract the top-level directory name
    top_dir=$(echo $item | cut -d'/' -f1)

    # Check if it's a directory and not hidden
    if [[ -d $top_dir ]] && [[ ! $top_dir =~ ^\..* ]]; then
        # Add to the list if not already present
        if [[ ! $changed_dirs =~ $top_dir ]]; then
            changed_dirs+="$top_dir "
        fi
    fi
done

# Sort and remove duplicate entries
changed_dirs=$(echo $changed_dirs | tr ' ' '\n' | sort -u)

# Filter out directories listed in .deployignore, if the file exists
if [ -f ".deployignore" ]; then
    for ignore in $(cat .deployignore); do
        changed_dirs=$(echo "$changed_dirs" | grep -v "^$ignore$")
    done
fi

# Convert to JSON format and write to environment file
json_output="{\"app_name\": ["
for dir in $changed_dirs; do
    json_output+="\"$dir\","
done
json_output=$(echo "$json_output" | sed 's/,$//') # Remove trailing comma
json_output+="]}"

# Write to GitHub environment file
echo "MATRIX_JSON=$json_output" >> $GITHUB_ENV
