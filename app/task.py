from app import webserver

class Task:
    """
    Base class for tasks.
    """
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for tasks.
        """
        raise NotImplementedError("Method 'execute' must be implemented in subclasses")

class StateMeanTask:
    """
    Task for calculating the mean value of a specific state.
    """
    def __init__(self, question, state, data_frame):
        self.question = question
        self.state = state
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for StateMeanTask.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        if self.state is None:
            return {"status": "error", "message": "State not specified"}, 400

        # Filter data to keep only records corresponding to the specified question and state
        relevant_data = self.data_frame[(self.data_frame['Question'] == self.question) &
                                        (self.data_frame['LocationDesc'] == self.state)]
        state_mean = relevant_data['Data_Value'].mean()

        return {self.state: state_mean}

class StatesMeanTask:
    """
    Task for calculating the mean value of all states.
    """
    def __init__(self, question, data_frame):
        self.question = question
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for StatesMeanTask.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        # Filter data to keep only records corresponding to the specified question
        relevant_data = self.data_frame[(self.data_frame['Question'] == self.question)]
        state_means = {}
        for state in relevant_data['LocationDesc'].unique():
            state_data = relevant_data[relevant_data['LocationDesc'] == state]
            state_means[state] = state_data['Data_Value'].mean()

        sorted_results = sorted(state_means.items(), key=lambda x: x[1])

        result = {state: mean for state, mean in sorted_results}

        return result

class Best5Task:
    """
    Task for finding the best 5 states based on a specific question.
    """
    def __init__(self, question, data_frame):
        self.question = question
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for Best5Task.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        # Filter data to keep only records corresponding to the specified question
        relevant_data = self.data_frame[(self.data_frame['Question'] == self.question)]
        state_means = {}
        for state in relevant_data['LocationDesc'].unique():
            state_data = relevant_data[relevant_data['LocationDesc'] == state]
            state_means[state] = state_data['Data_Value'].mean()

        if self.question in webserver.data_ingestor.questions_best_is_min:
            sorted_results = sorted(state_means.items(), key=lambda x: x[1])[:5]
        else:
            sorted_results = sorted(state_means.items(), key=lambda x: x[1], reverse=True)[:5]

        result = {state: mean for state, mean in sorted_results}

        return result



class Worst5Task:
    """
    Task for finding the worst 5 states based on a specific question.
    """
    def __init__(self, question, data_frame):
        self.question = question
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for Worst5Task.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        # Filter data to keep only records corresponding to the specified question
        relevant_data = self.data_frame[(self.data_frame['Question'] == self.question)]

        # Calculate the mean values for each state
        state_means = {}
        for state in relevant_data['LocationDesc'].unique():
            state_data = relevant_data[relevant_data['LocationDesc'] == state]
            state_means[state] = state_data['Data_Value'].mean()

        # Sort the results based on mean
        if self.question in webserver.data_ingestor.questions_best_is_max:
            sorted_results = sorted(state_means.items(), key=lambda x: x[1])[:5]
        else:
            sorted_results = sorted(state_means.items(), key=lambda x: x[1], reverse=True)[:5]

        # Construct a JSON object with the results
        result = {state: mean for state, mean in sorted_results}

        return result

class GlobalMeanTask:
    """
    Task for calculating the global mean value of a specific question.
    """
    def __init__(self, question, data_frame):
        self.question = question
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for GlobalMeanTask.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        # Filter data to keep only records corresponding to the specified question
        relevant_data = self.data_frame[(self.data_frame['Question'] == self.question)]

        # Calculate the mean value
        global_mean = relevant_data['Data_Value'].mean()

        return {"global_mean": global_mean}

class DiffFromMeanTask:
    """
    Task for calculating the difference between the global mean and state means.
    """
    def __init__(self, question, data_frame):
        self.question = question
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for DiffFromMeanTask.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        # Filter data to keep only records corresponding to the specified question
        relevant_data = self.data_frame[self.data_frame['Question'] == self.question]

        # Calculate the mean values for each state
        state_means = {}
        for state in relevant_data['LocationDesc'].unique():
            state_data = relevant_data[relevant_data['LocationDesc'] == state]
            state_means[state] = state_data['Data_Value'].mean()

        # Calculate the global mean of the recorded values
        global_mean = relevant_data['Data_Value'].mean()

        # Calculate the difference between the global mean and the state mean for each state
        diff_from_mean = {state: global_mean - mean for state, mean in state_means.items()}

        # Sort the differences in descending order
        sorted_diff_from_mean = sorted(diff_from_mean.items(), key=lambda x: x[1], reverse=True)

        # Construct a JSON object with the results
        result = {state: mean for state, mean in sorted_diff_from_mean}

        return result


class StateDiffFromMeanTask:
    """
    Task for calculating the difference from the global mean for a specific state.
    """
    def __init__(self, question, state, data_frame):
        self.question = question
        self.state = state
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for StateDiffFromMeanTask.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        # Read data from the CSV file using DataIngestor
        data_frame = webserver.data_ingestor.data

        # Filter data to keep only records corresponding to the specified question and state
        relevant_data = data_frame[(data_frame['Question'] == self.question) & \
                                    (data_frame['LocationDesc'] == self.state)]
        global_data = data_frame[data_frame['Question'] == self.question]
        # Check if there are no records for the specified state
        if relevant_data.empty:
            return {"status": "error", "message": f"No data available for {self.state}"}, 400

        # Calculate the mean value for the specified state
        state_mean = relevant_data['Data_Value'].mean()

        # Calculate the global mean of the recorded values
        global_mean = global_data['Data_Value'].mean()

        # Calculate the difference between the global mean and the mean for the specified state
        diff_from_mean = global_mean - state_mean

        return {self.state: diff_from_mean}

class MeanByCategoryTask:
    """
    Task for calculating the mean value by category for a specific question.
    """
    def __init__(self, question, data_frame):
        self.question = question
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for MeanByCategoryTask.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        # Filter data to keep only records corresponding to the specified question
        relevant_data = self.data_frame[(self.data_frame['Question'] == self.question)]

        # Calculate the mean value for each segment within the categories of each state
        mean_by_category = relevant_data.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value'].mean()

        # Transform the results into an easy-to-use format
        results = {f"('{state}', '{category}', '{segment}')": mean_value for (state, category, segment), mean_value in mean_by_category.items()}

        return results

class StateMeanByCategoryTask:
    """
    Task for calculating the mean value by category for a specific state and question.
    """
    def __init__(self, question, state, data_frame):
        self.question = question
        self.state = state
        self.data_frame = data_frame

    def execute(self):
        """
        Execute method for StateMeanByCategoryTask.
        """
        # Check if the question is valid
        if self.question not in webserver.data_ingestor.questions_best_is_min and \
           self.question not in webserver.data_ingestor.questions_best_is_max:
            return {"status": "error", "message": "Invalid question"}, 400

        # Filter data to keep only records corresponding to the specified question and state
        relevant_data = self.data_frame[(self.data_frame['Question'] == self.question) & \
            (self.data_frame['LocationDesc'] == self.state)]

        # Calculate the mean value for each segment within the respective categories
        mean_by_category = relevant_data.groupby(['StratificationCategory1', 'Stratification1'])['Data_Value'].mean()

        # Transform the results into an easy-to-use format
        results = {f"('{category}', '{segment}')": mean_value for (category, segment), mean_value in mean_by_category.items()}

        return {self.state: results}
