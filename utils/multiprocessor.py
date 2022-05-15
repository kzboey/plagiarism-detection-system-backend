import multiprocessing

def add_tasks(fileObj, queue):
    queue.put(fileObj)

def run():
    try:
        print("running multiproccesor")
        if not task_queue.empty():
            fileobj = task_queue.get()
        print("printing fileobject " + fileobj)
    except Exception as e:
        print("queue error: {}".format(e))

task_queue = multiprocessing.Queue()
upload_process = multiprocessing.Process(target=run, args=[task_queue])
upload_process.daemon = True
upload_process.start()

class BackgroundUpload:

    def __init__(self, filename):
        self.filename = filename

    def add_tasks(self, fileObj):
        task_queue.put(fileObj)


