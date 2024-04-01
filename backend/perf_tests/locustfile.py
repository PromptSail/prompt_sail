from locust import HttpUser, task

# project_id = '5fd4b399-7169-4775-b830-06ec41a49ad6'  # True project
project_id = "project-test"  # Project with fake data


class CountStatisticsUser(HttpUser):


    # def on_start(self):

    #     count=1000
    #     self.client.post(f"/api/only_for_purpose/mock_transactions?count={count}&date_from=2023-09-01&date_to=2024-03-31", json={})

    #  Transation Count Statistics
    @task
    def transaction_count_statistics_yearly(self):
        self.client.get(
            f"/api/statistics/transactions_count?project_id={project_id}&period=year"
        )

    @task
    def transaction_count_statistics_monthly(self):
        self.client.get(
            f"/api/statistics/transactions_count?project_id={project_id}&period=month"
        )

    @task
    def transaction_count_statistics_weekly(self):
        self.client.get(
            f"/api/statistics/transactions_count?project_id={project_id}&period=week"
        )

    @task
    def transaction_count_statistics_daily(self):
        self.client.get(
            f"/api/statistics/transactions_count?project_id={project_id}&period=day"
        )



class CostStatisticsUser(HttpUser):
    # Transaction Cost Statistics
    @task
    def transaction_cost_statistics_yearly(self):
        self.client.get(
            f"/api/statistics/transactions_cost?project_id={project_id}&period=year"
        )

    @task
    def transaction_cost_statistics_monthly(self):
        self.client.get(
            f"/api/statistics/transactions_cost?project_id={project_id}&period=month"
        )

    @task
    def transaction_cost_statistics_weekly(self):
        self.client.get(
            f"/api/statistics/transactions_cost?project_id={project_id}&period=week"
        )

    @task
    def transaction_cost_statistics_daily(self):
        self.client.get(
            f"/api/statistics/transactions_cost?project_id={project_id}&period=day"
        )


class SpeedStatisticsUser(HttpUser):
    # Transaction Speed Statistics
    @task
    def transaction_speed_statistics_yearly(self):
        self.client.get(
            f"/api/statistics/transactions_speed?project_id={project_id}&period=year"
        )

    @task
    def transaction_speed_statistics_monthly(self):
        self.client.get(
            f"/api/statistics/transactions_speed?project_id={project_id}&period=month"
        )
    @task
    def transaction_speed_statistics_weekly(self):
        self.client.get(
            f"/api/statistics/transactions_speed?project_id={project_id}&period=week"
        )

    @task
    def transaction_speed_statistics_daily(self):
        self.client.get(
            f"/api/statistics/transactions_speed?project_id={project_id}&period=day"
        )