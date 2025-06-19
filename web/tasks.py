from .celery_worker import celery

@celery.task
def run_scan_task(archive_path, scanners, user):
    # распаковка, запуск, сохранение отчёта, запись в историю...
    # (логика выносится из FastAPI endpoint в этот таск)
    return {"status": "ok"}