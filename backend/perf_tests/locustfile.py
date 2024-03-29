from locust import HttpUser, task

# project_id = '5fd4b399-7169-4775-b830-06ec41a49ad6'  # True project
project_id = 'project-test'  # Project with fake data


class HelloWorldUser(HttpUser):
    @task
    def transaction_cost_statistics_yearly(self):
        self.client.get(f'/api/statistics/transactions_cost?project_id={project_id}&period=yearly')

    @task
    def transaction_count_statistics_yearly(self):
        self.client.get(f'/api/statistics/transactions_count?project_id={project_id}&period=yearly')

    @task
    def transaction_speed_statistics_yearly(self):
        self.client.get(f'/api/statistics/transactions_speed?project_id={project_id}&period=yearly')

    @task
    def transaction_cost_statistics_monthly(self):
        self.client.get(f'/api/statistics/transactions_cost?project_id={project_id}&period=monthly')

    @task
    def transaction_count_statistics_monthly(self):
        self.client.get(f'/api/statistics/transactions_count?project_id={project_id}&period=monthly')

    @task
    def transaction_speed_statistics_monthly(self):
        self.client.get(f'/api/statistics/transactions_speed?project_id={project_id}&period=monthly')