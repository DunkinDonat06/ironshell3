from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import shutil
import os
import secrets

app = FastAPI()
security = HTTPBasic()

USERNAME = "admin"
PASSWORD = "changeme"
REPORTS_DIR = "reports/"
UPLOADS_DIR = "uploads/"

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/scan/")
async def upload_and_scan(background_tasks: BackgroundTasks, file: UploadFile = File(...), credentials: HTTPBasicCredentials = Depends(check_auth)):
    file_location = os.path.join(UPLOADS_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # Для теста — просто копируем файл, в будущем можно добавить реальный запуск сканера по архиву
    report_path = os.path.join(REPORTS_DIR, f"{file.filename}_report.json")
    with open(report_path, "w") as f:
        f.write("{}")
    return {"detail": "Файл получен, сканирование запущено (заглушка)", "report": report_path}

@app.get("/reports/")
async def list_reports(credentials: HTTPBasicCredentials = Depends(check_auth)):
    files = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".json")]
    return {"reports": files}

@app.get("/reports/{report_name}")
async def get_report(report_name: str, credentials: HTTPBasicCredentials = Depends(check_auth)):
    path = os.path.join(REPORTS_DIR, report_name)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(path, media_type="application/json")

@app.get("/health")
async def health_check():
    return JSONResponse({"status": "ok"})