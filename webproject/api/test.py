from celery import shared_task

@shared_task(bind=True)
def test_task(self):
    print("Test task started")
    return "Test task completed"