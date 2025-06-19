def remediation_hint(finding):
    if "SQL Injection" in finding["title"]:
        return "Используйте параметризованные запросы и ORM. Не формируйте SQL через конкатенацию строк."
    if "XSS" in finding["title"]:
        return "Проверяйте и экранируйте пользовательский ввод. Включите Content Security Policy (CSP)."
    if "Insecure Deserialization" in finding["title"]:
        return "Избегайте небезопасной десериализации и валидации входных данных."
    return "Обратитесь к best-practices для этого типа уязвимости."