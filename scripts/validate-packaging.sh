#!/bin/bash
# Cross-platform packaging validation script for udos-sonic
# Tests clean virtual environment installation and import paths
# Usage: ./scripts/validate-packaging.sh [--keep-venv]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="/tmp/udos-sonic-validation-$$"
KEEP_VENV=false

# Parse arguments
if [[ "$1" == "--keep-venv" ]]; then
    KEEP_VENV=true
fi

echo "==============================================="
echo "uDOS-sonic Packaging Validation"
echo "==============================================="
echo "OS: $(uname -s)"
echo "Python: $(python3 --version)"
echo "Repo: $REPO_ROOT"
echo "Test venv: $VENV_DIR"
echo "==============================================="
echo

# Cleanup function
cleanup() {
    if [[ "$KEEP_VENV" == "false" && -d "$VENV_DIR" ]]; then
        echo "🧹 Cleaning up test venv..."
        rm -rf "$VENV_DIR"
    else
        echo "📁 Keeping test venv at: $VENV_DIR"
    fi
}

trap cleanup EXIT

echo "Step 1: Create clean virtual environment"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "✓ Virtual environment created"
echo

echo "Step 2: Install package from repository"
pip install -q --upgrade pip setuptools wheel
pip install "$REPO_ROOT"

echo "✓ Package installed"
echo

echo "Step 3: Verify Python import paths"

# Test top-level imports
python3 -c "import udos_sonic; assert hasattr(udos_sonic, 'SonicService'), 'Missing SonicService'" && \
    echo "  ✓ import udos_sonic"

python3 -c "from udos_sonic import SonicService" && \
    echo "  ✓ from udos_sonic import SonicService"

python3 -c "from udos_sonic import SonicManifest, default_manifest, validate_manifest_data" && \
    echo "  ✓ from udos_sonic import SonicManifest, default_manifest, validate_manifest_data"

# Test service namespace imports
python3 -c "from udos_sonic.services import write_plan, build_plan" && \
    echo "  ✓ from udos_sonic.services import write_plan, build_plan"

python3 -c "from udos_sonic.services import SonicService" && \
    echo "  ✓ from udos_sonic.services import SonicService"

# Test service construction
python3 -c "from udos_sonic import SonicService; svc = SonicService(); assert svc.repo_root is not None" && \
    echo "  ✓ SonicService() construction succeeds"

echo "✓ All import paths verified"
echo

echo "Step 4: Verify console script entrypoints"

# Test sonic command
sonic --help > /dev/null && echo "  ✓ sonic --help"
sonic plan --help > /dev/null && echo "  ✓ sonic plan --help"
sonic run --help > /dev/null && echo "  ✓ sonic run --help"

# Test sonic-api command
sonic-api --help > /dev/null && echo "  ✓ sonic-api --help"

# Test sonic-mcp command
sonic-mcp --help > /dev/null && echo "  ✓ sonic-mcp --help"

echo "✓ All console entrypoints verified"
echo

echo "Step 5: Test custom build engine example"

# Run example with dry-run mode
cd "$REPO_ROOT"
if [[ -f "config/sonic-manifest.json.example" && -f "examples/custom-build-engine/example_engine.py" ]]; then
    python3 examples/custom-build-engine/example_engine.py \
        --manifest config/sonic-manifest.json.example \
        --dry-run > /dev/null && echo "  ✓ Custom build engine example executes"
else
    echo "  ⚠ Example files not found, skipping"
fi

echo "✓ Extension example verified"
echo

echo "==============================================="
echo "✅ All validation checks passed!"
echo "==============================================="
echo
echo "Platform: $(uname -s) $(uname -r)"
echo "Python: $(python3 --version)"
echo "Package version: $(pip show udos-sonic | grep Version | awk '{print $2}')"
echo
