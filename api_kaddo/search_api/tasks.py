from threading import Lock

from celery import shared_task
from django.core.management import call_command

task_lock = Lock()

@shared_task(bind=True)
def run_pre_cadastro_rotina(self):

    if not task_lock.locked():
        task_lock.acquire()
        try:
            call_command('pre_cadastro_rotina', '0')
        except Exception as exc:
            pass
        finally:
            # Release the lock
            task_lock.release()
        
    # Schedule the next run after 'x' seconds
    self.apply_async(countdown=60)
