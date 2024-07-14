#!/bin/zsh

# Function to create directory and prompt if it already exists
create_dir() {
    if [ -d "$1" ]; then
        read "response?Directory $1 already exists. Do you want to replace it? (y/n): "
        if [[ "$response" =~ ^[Yy]$ ]]; then
            rm -rf "$1"
            mkdir -p "$1"
            echo "Replaced $1"
        else
            echo "Skipped $1"
        fi
    else
        mkdir -p "$1"
        echo "Created $1"
    fi
}

# Base project directory
PROJECT_DIR="./"

# Directory structure
DIRS=(
    "$PROJECT_DIR/src/graph"
    "$PROJECT_DIR/src/mitre"
    "$PROJECT_DIR/src/analysis"
    "$PROJECT_DIR/src/utils"
    "$PROJECT_DIR/tests"
    "$PROJECT_DIR/examples"
    "$PROJECT_DIR/benches"
)

# Create directories
for dir in $DIRS; do
    create_dir "$dir"
done

# Create mod.rs files
touch "$PROJECT_DIR/src/lib.rs"
touch "$PROJECT_DIR/src/graph/mod.rs"
touch "$PROJECT_DIR/src/graph/node.rs"
touch "$PROJECT_DIR/src/graph/edge.rs"
touch "$PROJECT_DIR/src/graph/graph.rs"
touch "$PROJECT_DIR/src/mitre/mod.rs"
touch "$PROJECT_DIR/src/mitre/parse.rs"
touch "$PROJECT_DIR/src/mitre/model.rs"
touch "$PROJECT_DIR/src/analysis/mod.rs"
touch "$PROJECT_DIR/src/analysis/stream.rs"
touch "$PROJECT_DIR/src/utils/mod.rs"
touch "$PROJECT_DIR/src/utils/validation.rs"

echo "Project structure created successfully!"
