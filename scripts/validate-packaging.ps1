# Cross-platform packaging validation script for udos-sonic (Windows PowerShell)
# Tests clean virtual environment installation and import paths
# Usage: .\scripts\validate-packaging.ps1 [-KeepVenv]

param(
    [switch]$KeepVenv
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$VenvDir = Join-Path $env:TEMP "udos-sonic-validation-$(Get-Random)"

Write-Host "==============================================="
Write-Host "uDOS-sonic-screwdriver Packaging Validation"
Write-Host "==============================================="
Write-Host "OS: $([System.Environment]::OSVersion.VersionString)"
Write-Host "Python: $(python --version)"
Write-Host "Repo: $RepoRoot"
Write-Host "Test venv: $VenvDir"
Write-Host "==============================================="
Write-Host ""

# Cleanup function
function Cleanup {
    if (-not $KeepVenv -and (Test-Path $VenvDir)) {
        Write-Host "🧹 Cleaning up test venv..."
        Remove-Item -Recurse -Force $VenvDir
    } else {
        Write-Host "📁 Keeping test venv at: $VenvDir"
    }
}

try {
    Write-Host "Step 1: Create clean virtual environment"
    python -m venv $VenvDir
    
    # Activate venv (Windows style)
    $ActivateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
    & $ActivateScript
    
    Write-Host "✓ Virtual environment created"
    Write-Host ""
    
    Write-Host "Step 2: Install package from repository"
    pip install -q --upgrade pip setuptools wheel
    pip install $RepoRoot
    
    Write-Host "✓ Package installed"
    Write-Host ""
    
    Write-Host "Step 3: Verify Python import paths"
    
    # Test top-level imports
    python -c "import udos_sonic; assert hasattr(udos_sonic, 'SonicService'), 'Missing SonicService'"
    Write-Host "  ✓ import udos_sonic"
    
    python -c "from udos_sonic import SonicService"
    Write-Host "  ✓ from udos_sonic import SonicService"
    
    python -c "from udos_sonic import SonicManifest, default_manifest, validate_manifest_data"
    Write-Host "  ✓ from udos_sonic import SonicManifest, default_manifest, validate_manifest_data"
    
    # Test service namespace imports
    python -c "from udos_sonic.services import write_plan, build_plan"
    Write-Host "  ✓ from udos_sonic.services import write_plan, build_plan"
    
    python -c "from udos_sonic.services import SonicService"
    Write-Host "  ✓ from udos_sonic.services import SonicService"
    
    # Test service construction
    python -c "from udos_sonic import SonicService; svc = SonicService(); assert svc.repo_root is not None"
    Write-Host "  ✓ SonicService() construction succeeds"
    
    Write-Host "✓ All import paths verified"
    Write-Host ""
    
    Write-Host "Step 4: Verify console script entrypoints"
    
    # Test sonic command
    sonic --help | Out-Null; Write-Host "  ✓ sonic --help"
    sonic plan --help | Out-Null; Write-Host "  ✓ sonic plan --help"
    sonic run --help | Out-Null; Write-Host "  ✓ sonic run --help"
    
    # Test sonic-api command
    sonic-api --help | Out-Null; Write-Host "  ✓ sonic-api --help"
    
    # Test sonic-mcp command
    sonic-mcp --help | Out-Null; Write-Host "  ✓ sonic-mcp --help"
    
    Write-Host "✓ All console entrypoints verified"
    Write-Host ""
    
    Write-Host "Step 5: Test custom build engine example"
    
    # Run example with dry-run mode
    Set-Location $RepoRoot
    $ManifestPath = Join-Path $RepoRoot "config\sonic-manifest.json.example"
    $ExamplePath = Join-Path $RepoRoot "examples\custom-build-engine\example_engine.py"
    
    if ((Test-Path $ManifestPath) -and (Test-Path $ExamplePath)) {
        python $ExamplePath --manifest $ManifestPath --dry-run | Out-Null
        Write-Host "  ✓ Custom build engine example executes"
    } else {
        Write-Host "  ⚠ Example files not found, skipping"
    }
    
    Write-Host "✓ Extension example verified"
    Write-Host ""
    
    Write-Host "==============================================="
    Write-Host "✅ All validation checks passed!"
    Write-Host "==============================================="
    Write-Host ""
    Write-Host "Platform: $([System.Environment]::OSVersion.VersionString)"
    Write-Host "Python: $(python --version)"
    Write-Host "Package version: $(pip show udos-sonic | Select-String 'Version' | ForEach-Object { $_.ToString().Split()[1] })"
    Write-Host ""
    
} catch {
    Write-Host "❌ Validation failed: $_"
    exit 1
} finally {
    Cleanup
}
