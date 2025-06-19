import os
import importlib

def list_scanners():
    scanners_dir = os.path.dirname(__file__)
    scanners = [f[:-3] for f in os.listdir(scanners_dir)
                if f.endswith(".py") and f != "__init__.py"]
    print("Доступные сканеры:")
    for s in sorted(scanners):
        print(f"- {s}")

def run_scanners(only=None, skip=None, output_dir="reports/", report_format="json",
                 dry_run=False, profile=None, logger=None):
    scanners_dir = os.path.dirname(__file__)
    scanner_files = [f for f in os.listdir(scanners_dir)
                     if f.endswith(".py") and f != "__init__.py"]
    scanner_names = [f[:-3] for f in scanner_files]
    if only:
        selected = [s for s in scanner_names if s in only]
    elif skip:
        selected = [s for s in scanner_names if s not in skip]
    else:
        selected = scanner_names
    if dry_run:
        print("Следующие сканеры будут запущены:", ", ".join(selected))
        return
    results = {}
    for s in selected:
        module = importlib.import_module(f"scanners.{s}")
        scanner_class = getattr(module, "Scanner", None)
        if scanner_class:
            scanner = scanner_class(profile=profile, logger=logger)
            findings = scanner.run()
            results[s] = findings
            if logger:
                logger.info(f"{s}: найдено {len(findings)} проблем")
    from utils.report import ReportManager
    reporter = ReportManager(output_dir)
    out_path = reporter.save(results, report_format, f"report.{report_format}")
    print(f"Отчёт сохранён: {out_path}")