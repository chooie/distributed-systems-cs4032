def safe(lock, f):
    lock.acquire()
    output = f()
    lock.release()
    return output
