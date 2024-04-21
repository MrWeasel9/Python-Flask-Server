# Health Metrics Analysis Server

This project is a Python-based web application developed using the Flask micro-framework. It serves as a platform for analyzing nutrition, physical activity, and obesity data collected by the U.S. Department of Health & Human Services from 2011 to 2022. The server offers a RESTful API with endpoints designed to provide users with valuable statistical insights and state-specific health metrics.

## Features

- **Multi-threaded Server**: Utilizes multi-threading techniques to efficiently handle concurrent client requests.
  
- **RESTful API**: Provides a user-friendly API with intuitive endpoints for querying health-related statistics and insights.
  
- **Statistical Analysis**: Offers functionalities such as retrieving mean values, top/bottom states, and category-wise mean values for health metrics.

## Usage

### API Endpoints

- `/api/states_mean`: Retrieve mean values of health metrics for all states.
  
- `/api/state_mean`: Retrieve mean values of health metrics for a specific state.
  
- `/api/best5`: Retrieve the top 5 states with the best health metrics.
  
- `/api/worst5`: Retrieve the bottom 5 states with the worst health metrics.
  
- `/api/global_mean`: Retrieve global mean values of health metrics.
  
- `/api/diff_from_mean`: Calculate differences between global mean values and state-specific mean values for all states.
  
- `/api/state_diff_from_mean`: Calculate differences between global mean values and state-specific mean values for a specific state.
  
- `/api/mean_by_category`: Calculate average values for each category segment for all states.
  
- `/api/state_mean_by_category`: Calculate average values for each category segment for a specific state.
  
- `/api/graceful_shutdown`: Initiate a graceful shutdown process for the server.

## Implementation [README](app/README)

## Tests

For the purposes of testing I was provided with a checker from the university which sends a large amount of requests to check the correct functionality of the multithreaded component and make sure the return values are all in order.

### Setup and Run

1. Prepare the environment:

```bash
  make create_venv
  source venv/bin/activate
  make install
```

2. Install dependencies:

```bash
  pip install -r requirements.txt
```
3. Run the server and tests:

```bash
  make run_server
  make run_tests
```


