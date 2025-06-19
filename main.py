import sys
import os
import yaml
import argparse
import subprocess
import logging
from ironshell.utils import sbom, remediation, license_audit

# --- PRESETS ---
PRESETS = {
    "fast": ["gitleaks", "semgrep"],
    "full": [
        "gitleaks", "semgrep", "bandit", "brakeman", "eslint",
        "trufflehog", "checkov", "tfsec", "kubesec", "trivy",
        "dockle", "syft", "osv-scanner"
    ],
}

# --- CLI UX: инициализация профиля и blacklist ---
def cli_init():
    if not os.path.exists(".ironprofile.yaml"):
        with open(".ironprofile.yaml", "w") as f:
            yaml.dump({"scanners": PRESETS["fast"]}, f)
    if not os.path.exists(".ironignore"):
        with open(".ironignore", "w") as f:
            f.write("*.log\n*.tmp\n")
    if not os.path.exists("ironshell/blacklist.yaml"):
        os.makedirs("ironshell", exist_ok=True)
        with open("ironshell/blacklist.yaml", "w") as f:
            yaml.dump({"paths": ["/etc/", "*.pem", "*.key"]}, f)
    print("Инициализация завершена. Профили и blacklist созданы.")

# --- EXPLAIN/REMEDIATION ---
def explain_finding(finding):
    return remediation.remediation_hint(finding)

# --- Загрузка профиля ---
def load_profile(profile_path=".ironprofile.yaml"):
    if os.path.exists(profile_path):
        with open(profile_path) as f:
            return yaml.safe_load(f)
    return {}

# --- Фильтрация по .ironignore ---
def filter_files(target_dir, ignore_path=".ironignore"):
    import fnmatch
    patterns = []
    if os.path.exists(ignore_path):
        with open(ignore_path) as f:
            patterns = [line.strip() for line in f if line.strip()]
    for root, dirs, files in os.walk(target_dir):
        for fname in files:
            path = os.path.relpath(os.path.join(root, fname), target_dir)
            if any(fnmatch.fnmatch(path, pat) for pat in patterns):
                continue
            yield os.path.join(root, fname)

# --- Запуск сканера ---
def run_scanner(scanner, target_dir, args=None):
    args = args or []
    if scanner == "gitleaks":
        cmd = ["gitleaks", "detect", "--source", target_dir, "--report-format", "json"]
    elif scanner == "semgrep":
        cmd = ["semgrep", "--config", "auto", "--json", target_dir]
    elif scanner == "bandit":
        cmd = ["bandit", "-r", target_dir, "-f", "json"]
    elif scanner == "syft":
        cmd = ["syft", target_dir, "-o", "json"]
    elif scanner == "trivy":
        cmd = ["trivy", "fs", "--scanners", "vuln,secret,config,license", "--format", "json", target_dir]
    # ...добавь остальные сканеры по аналогии
    else:
        print(f"Сканер {scanner} не поддерживается.")
        return []
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        return json.loads(result.stdout)
    except Exception as ex:
        print(f"[!] Ошибка запуска {scanner}: {ex}")
        return []

# --- Агрегация результатов (очень базово) ---
def aggregate_results(result_lists):
    findings = []
    for result in result_lists:
        if isinstance(result, list):
            findings.extend(result)
        elif isinstance(result, dict) and "results" in result:
            findings.extend(result["results"])
        elif isinstance(result, dict) and "findings" in result:
            findings.extend(result["findings"])
    return findings

# --- Генерация отчётов ---
def save_report(findings, fmt="json", output="report.json"):
    import json
    if fmt == "json":
        with open(output, "w") as f:
            json.dump(findings, f, indent=2)
        print(f"JSON отчёт сохранён: {output}")
    elif fmt == "sarif":
        from ironshell.utils.report_sarif import to_sarif
        with open(output, "w") as f:
            f.write(to_sarif(findings))
        print(f"SARIF отчёт сохранён: {output}")
    elif fmt == "xlsx":
        from ironshell.utils.report_xlsx import to_xlsx
        to_xlsx(findings, output)
        print(f"XLSX отчёт сохранён: {output}")
    # ... аналогично для markdown, html и т.д.

# --- License audit ---
def run_license_audit(target_dir):
    licenses = license_audit.get_licenses(target_dir)
    print("Обнаружены лицензии:", ", ".join(licenses))
    return licenses

# --- SBOM CycloneDX ---
def run_sbom_cyclonedx(target_dir):
    path = sbom.generate_cyclonedx_sbom(target_dir)
    print(f"CycloneDX SBOM сохранён в {path}")
    return path

# --- Аргументы командной строки: основной парсер ---
def parse_args():
    parser = argparse.ArgumentParser(description="IronShell: DevSecOps CLI")
    parser.add_argument("--init", action="store_true", help="Инициализировать профиль и blacklist")
    parser.add_argument("--preset", type=str, help="Preset набора сканеров (fast, full, ...)")
    parser.add_argument("--explain", type=str, help="Объяснить finding по заголовку")
    parser.add_argument("--only", nargs="+", help="Только указанные сканеры")
    parser.add_argument("--skip", nargs="+", help="Пропустить сканеры")
    parser.add_argument("--format", type=str, default="json", help="Формат отчёта")
    parser.add_argument("--output-dir", type=str, default="results", help="Куда сохранять отчёты")
    parser.add_argument("--target", type=str, default=".", help="Что сканировать")
    parser.add_argument("--license-audit", action="store_true", help="Аудит лицензий")
    parser.add_argument("--sbom-cyclonedx", action="store_true", help="Сделать CycloneDX SBOM")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.init:
        cli_init()
        return
    if args.explain:
        print(explain_finding({"title": args.explain}))
        return

    # 1. Определение набора сканеров
    profile = load_profile()
    if args.preset:
        scanners = PRESETS.get(args.preset, PRESETS["fast"])
    elif args.only:
        scanners = args.only
    elif profile and "scanners" in profile:
        scanners = profile["scanners"]
    else:
        scanners = PRESETS["fast"]
    if args.skip:
        scanners = [s for s in scanners if s not in args.skip]

    # 2. Сканирование
    os.makedirs(args.output_dir, exist_ok=True)
    all_results = []
    for scanner in scanners:
        print(f"▶ Запуск сканера: {scanner}")
        findings = run_scanner(scanner, args.target)
        out_path = os.path.join(args.output_dir, f"{scanner}_report.json")
        with open(out_path, "w") as f:
            import json
            json.dump(findings, f, indent=2)
        all_results.append(findings)

    # 3. Агрегация и итоговый отчёт
    findings = aggregate_results(all_results)
    final_report = os.path.join(args.output_dir, f"ironshell_report.{args.format}")
    save_report(findings, args.format, final_report)

    # 4. License audit и SBOM
    if args.license_audit:
        run_license_audit(args.target)
    if args.sbom_cyclonedx:
        run_sbom_cyclonedx(args.target)

    print("IronShell завершён.")

if __name__ == "__main__":
    main()