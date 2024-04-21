import json
from queue import Queue
from threading import Thread, Event
import os
import multiprocessing

class ThreadPool:
    """
    A class representing a thread pool for executing tasks asynchronously.
    """
    def __init__(self):
        """
        Initialize the ThreadPool instance.
        """
        self.dictionary = {}
        # Determine the number of threads allowed by hardware
        self.num_threads = int(os.environ.get('TP_NUM_OF_THREADS', multiprocessing.cpu_count()))

        # Initialize a task queue
        self.task_queue = Queue()
        self.job_id = 0
        # Initialize threads within the pool
        self.threads = [TaskRunner(self.task_queue, self.dictionary) for _ in range(self.num_threads)]

    def add_task(self, task):
        """
        Add a task to the task queue.
        """
        self.job_id += 1
        # Add a task to the queue
        self.task_queue.put((task, self.job_id))
        return self.job_id

    def start(self):
        """
        Start each thread in the pool.
        """
        # Start each thread
        for thread in self.threads:
            thread.start()

    def stop(self):
        """
        Notify each thread to stop gracefully.
        """
        # Notify each thread to stop
        for thread in self.threads:
            thread.stop()

class TaskRunner(Thread):
    """
    A class representing a thread responsible for executing tasks.
    """
    def __init__(self, task_queue, dictionary):
        """
        Initialize the TaskRunner instance.
        """
        super().__init__()
        self.task_queue = task_queue
        self.graceful_shutdown = Event()
        self.dictionary = dictionary

    def run(self):
        """
        Execute tasks from the task queue.
        """
        
        while not self.graceful_shutdown.is_set():
            try:
                # Wait for a task from the queue or timeout after 1 second
                task, job_id = self.task_queue.get()

                # Execute the task and save the result to disk
                self.execute_task(task, job_id)

            except Exception:
                # If an exception occurs, continue execution
                continue


    def execute_task(self, task, job_id):
        """
        Execute a task and save the result.
        """
        self.dictionary[job_id] = {"status": "running", "result": None}
        value = task.execute()
        self.dictionary[job_id] = {"status": "done", "result": value}
        # Process the data or perform necessary operations
        self.save_result(job_id, value)

    def save_result(self, job_id, result):
        """
        Save the result to a JSON file.
        """
        # Define the path to the file where the results will be saved
        file_path = f"./results/{job_id}.json"

        # Create a JSON file and write the results to it
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(result, file)

    def stop(self):
        """
        Stop the thread gracefully.
        """
        # Method to stop the thread gracefully
        self.graceful_shutdown.set()
