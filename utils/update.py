import subprocess
import sys

def update_scanners():
    # Пример для pip-based сканеров, можно добавить и другие
    scanners = ["gitleaks", "semgrep", "trivy"]
    for scanner in scanners:
        print(f"Обновление {scanner}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", scanner], check=False)
    print("Все поддерживаемые сканеры обновлены.")