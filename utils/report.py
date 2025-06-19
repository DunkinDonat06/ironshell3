import os
import json
import csv

class ReportManager:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def save(self, data, fmt, filename):
        path = os.path.join(self.output_dir, filename)
        if fmt == "json":
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif fmt == "markdown":
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.to_markdown(data))
        elif fmt == "csv":
            self.to_csv(data, path)
        elif fmt == "html":
            self.to_html(data, path)
        # xlsx и sarif будут добавлены на отдельном шаге
        else:
            raise NotImplementedError(f"Format {fmt} не поддерживается")
        return path

    def to_markdown(self, data):
        lines = ["# IronShell Report", ""]
        for scanner, findings in data.items():
            lines.append(f"## {scanner}")
            for finding in findings:
                lines.append(f"- **{finding.get('severity', 'N/A')}**: {finding.get('title', '')}")
        return "\n".join(lines)

    def to_csv(self, data, path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Scanner", "Severity", "Title", "Description"])
            for scanner, findings in data.items():
                for finding in findings:
                    writer.writerow([
                        scanner,
                        finding.get("severity", "N/A"),
                        finding.get("title", ""),
                        finding.get("description", "")
                    ])

    def to_html(self, data, path):
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', "templates")))
        template = env.get_template("html_report.j2")
        html = template.render(data=data)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)