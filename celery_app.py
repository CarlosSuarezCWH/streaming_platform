from celery import Celery

celery_app = Celery(
    "streaming_platform",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["utils.tasks"]  
)

celery_app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    celery_app.start()
