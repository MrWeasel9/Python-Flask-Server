import logging
from app import webserver
from flask import request, jsonify
from app.task import *


# Obținem un obiect logger pentru modulele de routare
logger = logging.getLogger(__name__)

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """
    Example POST endpoint.
    """
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        logger.info("Received POST data: %s", data)

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        logger.error("Method not allowed")
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    Endpoint to get the status or result of a specific job.
    """
    job_id = int(job_id)
    # Verificăm dacă task-ul asociat cu job_id-ul este finalizat
    if webserver.tasks_runner.dictionary[job_id]["status"] == "running":
        logger.info("Job %s is still running", job_id)
        return jsonify({'status': 'running'}), 200

    # Dacă task-ul este finalizat, returnăm rezultatul
    logger.info("Job %s is done with result: %s", job_id, webserver.tasks_runner.dictionary[job_id]['result'])
    return jsonify({"status": "done", "data": webserver.tasks_runner.dictionary[job_id]["result"]}), 200

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """
    Endpoint to get the list of all jobs and their statuses.
    """
    # Construim o listă de dicționare pentru fiecare job_id și statusul său
    jobs = []
    for job_id, job_info in webserver.tasks_runner.dictionary.items():
        jobs.append({f"job_id_{job_id}": job_info["status"]})
    logger.info("Retrieving jobs status: %s", jobs)

    # Construim obiectul JSON cu lista de dicționare
    response_data = {"status": "done", "data": jobs}

    # Returnăm răspunsul sub formă de JSON
    return jsonify(response_data)

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    """
    Endpoint to get the number of remaining jobs in the queue.
    """
    # Obținem numărul de joburi rămase de procesat
    num_jobs = webserver.tasks_runner.task_queue.qsize()
    logger.info("Number of jobs remaining: %s", num_jobs)

    # Returnăm numărul de joburi sub formă de JSON
    return jsonify({"status": "done", "num_jobs": num_jobs})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    Endpoint to request the mean values of states.
    """
    # Obține datele din cerere
    data = request.json
    logger.info("Received request for states mean with data: %s" , data)

    # Creăm un obiect Task specific pentru cererea de media statelor
    task = StatesMeanTask(data['question'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    Endpoint to request the mean value of a state.
    """
    # Obținem datele din cerere
    data = request.json
    logger.info("Received request for state mean with data: %s", data)

    # Creăm un obiect Task specific pentru cererea de media statului
    task = StateMeanTask(data['question'], data['state'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    Endpoint to request the best 5 values.
    """
    # Obține datele din cerere
    data = request.json
    logger.info("Received request for best 5 with data: %s", data)

    # Creăm un obiect Task specific pentru cererea de best5
    task = Best5Task(data['question'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    Endpoint to request the worst 5 values.
    """
    # Obține datele din cerere
    data = request.json
    logger.info("Received request for worst 5 with data: %s", data)

    # Creăm un obiect Task specific pentru cererea de worst5
    task = Worst5Task(data['question'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    Endpoint to request the global mean value.
    """
    # Obține datele din cerere
    data = request.json
    logger.info("Received request for global mean with data: %s", data)

    # Creăm un obiect Task specific pentru cererea de global_mean
    task = GlobalMeanTask(data['question'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    Endpoint to request the difference from the mean value.
    """
    # Obține datele din cerere
    data = request.json
    logger.info("Received request for diff from mean with data: %s", data)

    # Creăm un obiect Task specific pentru cererea de diff_from_mean
    task = DiffFromMeanTask(data['question'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    Endpoint to request the difference from the mean value for a specific state.
    """
    # Obține datele din cerere
    data = request.json
    logger.info("Received request for state diff from mean with data: %s", data)

    # Creăm un obiect Task specific pentru cererea de state_diff_from_mean
    task = StateDiffFromMeanTask(data['question'], data['state'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    Endpoint to request the mean value by category.
    """
    # Obține datele din cerere
    data = request.json
    logger.info("Received request for mean by category with data: %s", data)

    # Creăm un obiect Task specific pentru cererea de mean_by_category
    task = MeanByCategoryTask(data['question'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    Endpoint to request the mean value by category for a specific state.
    """
    # Obține datele din cerere
    data = request.json
    logger.info("Received request for state mean by category with data: %s", data)

    # Creăm un obiect Task specific pentru cererea de state_mean_by_category
    task = StateMeanByCategoryTask(data['question'], data['state'], webserver.data_ingestor.data)

    # Adăugăm task-ul în coada de task-uri a thread pool-ului
    job_id = webserver.tasks_runner.add_task(task)

    # Returnăm un răspuns imediat pentru a confirma primirea cererii
    return jsonify({"status": "done", "job_id": job_id}), 202

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    """
    Endpoint to gracefully shutdown the server.
    """
    # Înainte de a începe shutdown-ul, trebuie să notificăm ThreadPool-ul
    webserver.tasks_runner.stop()
    logger.info("Received request for graceful shutdown")

    # Returnăm un răspuns JSON indicând că shutdown-ul a fost inițiat
    return jsonify({"status": "done", "result" : "Shutdown Initiated!"}), 200

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """
    Default endpoint to display available routes.
    """
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """
    Function to retrieve all defined routes.
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
