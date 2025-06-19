def merge_reports(*report_lists):
    merged = []
    for lst in report_lists:
        merged.extend(lst)
    return merged

def filter_findings(findings, scanner=None, severity=None, after_date=None):
    result = []
    for f in findings:
        if scanner and f.get("scanner") != scanner:
            continue
        if severity and str(f.get("severity", "")).lower() != severity.lower():
            continue
        # Можно добавить фильтр по дате, если в finding есть date
        result.append(f)
    return result