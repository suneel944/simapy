"""Simple HTTP server to serve Allure test reports"""

import http.server
import os
import shutil
import socket
import socketserver
import subprocess
import sys
import urllib.request
import webbrowser
from pathlib import Path


def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
            return False
        except OSError:
            return True


def find_available_port(start_port: int = 8080, max_attempts: int = 10) -> int:
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    raise RuntimeError(f"Could not find an available port in range {start_port}-{start_port + max_attempts - 1}")


def get_java_command() -> str | None:
    """Get Java command path"""
    java_cmd = shutil.which("java")
    if not java_cmd:
        return None
    # Verify Java works
    try:
        subprocess.run([java_cmd, "-version"], capture_output=True, check=True)
        return java_cmd
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_allure_distribution() -> Path | None:
    """Get Allure distribution path - check SDKMAN first, then cache"""
    # Check SDKMAN installation
    sdkman_home = os.environ.get("SDKMAN_DIR", os.path.expanduser("~/.sdkman"))
    sdkman_allure = Path(sdkman_home) / "candidates" / "allure" / "current"

    if sdkman_allure.exists() and (sdkman_allure / "lib").exists():
        return sdkman_allure

    # Check if allure CLI is available
    allure_cmd = shutil.which("allure")
    if allure_cmd:
        allure_bin = Path(allure_cmd).resolve()
        possible_dirs = [
            allure_bin.parent.parent,
            allure_bin.parent,
            Path("/usr/local/lib/allure"),
            Path("/opt/allure"),
        ]
        for dist_dir in possible_dirs:
            if (dist_dir / "lib").exists():
                return dist_dir

    # Check local cache directory for extracted distribution
    cache_dir = Path.home() / ".cache" / "allure"
    dist_path = get_allure_distribution_path(cache_dir)
    if dist_path:
        return dist_path

    return None


def download_allure_distribution(allure_dir: Path) -> bool:
    """Download Allure distribution from GitHub releases"""
    import json
    import tarfile
    import tempfile

    # Get latest version from GitHub API
    try:
        api_url = "https://api.github.com/repos/allure-framework/allure2/releases/latest"
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read())
            version = data["tag_name"].lstrip("v")
            download_url = None
            for asset in data.get("assets", []):
                if asset["name"].endswith(".tgz"):
                    download_url = asset["browser_download_url"]
                    break

            if not download_url:
                print("❌ Could not find Allure distribution download URL")
                return False

            print(f"📥 Downloading Allure distribution (v{version})...")
            print("   This is a one-time download (~50MB)")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".tgz") as tmp_file:
                tmp_path = Path(tmp_file.name)
                urllib.request.urlretrieve(download_url, tmp_path)
                print("📦 Extracting Allure distribution...")

                allure_dir.mkdir(parents=True, exist_ok=True)
                with tarfile.open(tmp_path, "r:gz") as tar:
                    tar.extractall(allure_dir)

                tmp_path.unlink()
                print(f"✅ Extracted to: {allure_dir}")
                return True
    except Exception as e:
        print(f"❌ Failed to download Allure distribution: {e}")
        return False


def get_allure_distribution_path(allure_dir: Path) -> Path | None:
    """Get Allure distribution base path"""
    # Allure distribution structure: allure-{version}/
    for subdir in allure_dir.iterdir():
        if subdir.is_dir() and subdir.name.startswith("allure-"):
            lib_dir = subdir / "lib"
            if lib_dir.exists():
                return subdir
    return None


def generate_allure_report(results_dir: Path, report_dir: Path) -> bool:
    """Generate Allure HTML report from results using Java JAR"""
    if not results_dir.exists() or not any(results_dir.iterdir()):
        print("⚠️  No allure-results directory found or it's empty. Run tests first.")
        return False

    # Check for Java
    java_cmd = get_java_command()
    if not java_cmd:
        print("❌ Java not found. Please install Java (JDK 8+):")
        print("   Using SDKMAN: sdk install java")
        print("   Or install from: https://adoptium.net/")
        return False

    # Get or download Allure distribution
    allure_dist = get_allure_distribution()
    if not allure_dist:
        # Download distribution to cache
        cache_dir = Path.home() / ".cache" / "allure"
        if not download_allure_distribution(cache_dir):
            return False
        allure_dist = get_allure_distribution_path(cache_dir)
        if not allure_dist:
            print("❌ Could not find Allure distribution after download")
            return False

    print("📊 Generating Allure report...")
    try:
        # Use CLASSPATH approach - simple and works!
        lib_dir = allure_dist / "lib"
        classpath = f"{lib_dir}/*:{lib_dir}/config"

        # Generate report using Java with classpath
        cmd = [
            java_cmd,
            "-cp",
            classpath,
            "io.qameta.allure.CommandLine",
            "generate",
            str(results_dir),
            "-o",
            str(report_dir),
            "--clean",
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Allure report generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate Allure report: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return False


def serve_report(port: int = 8080, open_browser: bool = True):
    """Generate and serve Allure HTML report"""
    results_dir = Path("allure-results")
    report_dir = Path("allure-report")

    # Generate the report first
    if not generate_allure_report(results_dir, report_dir):
        return

    # Check if report directory exists and has index.html
    index_file = report_dir / "index.html"
    if not index_file.exists():
        print("❌ Generated report directory does not contain index.html")
        print(f"   Expected: {index_file}")
        return

    # Check if port is in use and find alternative if needed
    if is_port_in_use(port):
        print(f"⚠️  Port {port} is already in use. Trying to find an available port...")
        try:
            port = find_available_port(port)
            print(f"✅ Using port {port} instead")
        except RuntimeError as e:
            print(f"❌ {e}")
            return

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(report_dir.absolute()), **kwargs)

        def log_message(self, format, *args):
            """Suppress default logging"""
            pass

    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            url = f"http://localhost:{port}"
            print(f"📊 Serving Allure report at {url}")
            print(f"📁 Report directory: {report_dir.absolute()}")
            print("Press Ctrl+C to stop")

            if open_browser:
                webbrowser.open(url)

            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Server stopped")
    except OSError as e:
        print(f"❌ Failed to start server: {e}")
        if "Address already in use" in str(e):
            print(f"💡 Try using a different port or stop the process using port {port}")


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    serve_report(port=port)
