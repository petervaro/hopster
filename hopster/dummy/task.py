from pathlib import Path
from threading import Thread

from hopster.constants import LOCKS_DIRECTORY


#------------------------------------------------------------------------------#
class Task:
    """
    `Task` is a dummy implementation for an asynchronous task manager, such as
    Celery.  To keep the dependencies down and make the assignment as portable
    as possible, `Task` uses simple threads to simulate parallelism and the
    file-system to achieve _atomicity_ (i.e. as a message-broker)
    """

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def __init__(self, task):
        Path(LOCKS_DIRECTORY).mkdir(exist_ok=True)
        self._task = task

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def fork(self, reference, args=(), kwargs={}):
        # If we already started processing this task
        lock = self._lock(reference)
        if lock.exists():
            return

        # Indicate we started processing this task
        lock.touch()

        # Create the job we need to run
        def target(*args, **kwargs):
            self._task(*args, **kwargs)
            lock.unlink()

        # Create the thread and start it immediately
        Thread(name=reference,
               target=target,
               args=args,
               kwargs=kwargs,
               daemon=True).start()

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    @staticmethod
    def _lock(reference):
        return Path(f'{LOCKS_DIRECTORY}/{reference}.lock')

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    def is_finished(self, reference):
        return not self._lock(reference).exists()
