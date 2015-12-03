def safe(lock, f):
    lock.acquire()
    f()
    lock.release()
