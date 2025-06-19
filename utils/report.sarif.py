import json
import datetime

def to_sarif(findings, tool_name="IronShell"):
    # findings — общий список из всех сканеров, приводить к структуре SARIF
    sarif = {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0-rtm.5.json",
        "runs": [{
            "tool": {"driver": {"name": tool_name}},
            "results": []
        }]
    }
    for f in findings:
        sarif["runs"][0]["results"].append({
            "ruleId": f.get("title", "NO_RULE"),
            "level": str(f.get("severity", "warning")).lower(),
            "message": {"text": f.get("description", "")},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {"uri": f.get("file", "N/A")}
                }
            }]
        })
    return json.dumps(sarif, indent=2)