import threading

class ProgressStore:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def set(self, jobid, value):
        with self.lock:
            self.data[jobid] = value

    def get(self, jobid):
        with self.lock:
            return self.data.get(jobid, {})

progress_store = ProgressStore()