import pytest
from test_utils import read_transactions_from_csv

class TestBaseTransactionCounts:
    """Base test class for transaction count statistics tests."""
    
    @pytest.fixture(autouse=True)
    def setup(self, client, application):
        """Setup test data and common test fixtures."""
        self.client = client
        self.application = application
        self.header = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
        }
        
        
        
        # Load test data
        transactions = read_transactions_from_csv("test_transactions.csv")
        
        # Add transactions to the database
        with self.application.transaction_context() as ctx:
            repo = ctx["transaction_repository"]
            for transaction in transactions:
                repo.add(transaction)
                
        yield
        
        # Delete transactions from the database
        with self.application.transaction_context() as ctx:
            repo = ctx["transaction_repository"]
            repo.delete_cascade("project-test")



    def _assert_response_status_and_length(self, response, expected_status, expected_length):
        """Helper method to check response status and length."""
        assert response.status_code == expected_status
        assert len(response.json()) == expected_length

    def _assert_status_counts(self, response, expected_counts):
        """Helper method to verify status counts in response."""
        actual_counts = [
            (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
            for stat in response.json()
        ]
        assert actual_counts == expected_counts

    def make_request(self, period, date_from, date_to):
        """Helper method to make API request for statistics."""
        return self.client.get(
            f"/api/statistics/transactions_count?project_id=project-test&period={period}&date_from={date_from}&date_to={date_to}",
            headers=self.header,
        )



class TestTransactionCountsErrors(TestBaseTransactionCounts):
    def test_cost_statistics_for_not_existing_project(self):
        """
        Tests token usage and cost statistics for not existing project.

        Given: A set of transactions within 2023-11-01 12:00-12:05
        When: Requesting token and cost statistics with 5-minute granularity
        Then: Returns one interval with correct token counts and costs for each model
        """
        response = self.make_request(
            "5minutes", 
            "2023-11-01T12:00:00", 
            "2023-11-01T12:04:59",
            "project-that-not-exists-xxx"
        )
        
        response_data = response.json()
        
        assert response.status_code == 404
        assert response_data == {"error": "Project not found"}
        

    def test_cost_statistics_for_not_wrong_period(self):
        """
        Tests token usage and cost statistics for a not supported period.

        Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
        When: Requesting token and cost statistics with not supported period
        Then: Returns error
        """
        response = self.make_request(
            "not-existing-period",
            "2023-11-01T12:00:00",
            "2023-11-01T12:29:59"
        )

        response_data = response.json()
        
        # assert
        response_data = response.json()
        assert response.status_code == 422
        assert response_data['detail'][0]['input'] == 'not-existing-period'


    def test_cost_statistics_for_date_from_after_date_to(self):
        """
        Tests transaction cost statistics for a time frame when date_from is after date_to.

        Given: Transactions spanning -10 minutes (2023-11-01 12:10-12:00) date_from is after date_to
        When: Requesting transaction cost statistics
        Then: Returns error
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:10:00",
            "2023-11-01T12:00:00"
        )
            
        # assert
        response_data = response.json()
        assert response.status_code == 400
        assert response_data['detail'] == "date_from is after date_to"

class Test5MinuteTransactionCounts(TestBaseTransactionCounts):
    """Tests for 5-minute granularity transaction counts."""

    def test_5min_duration_with_5min_granularity_returns_correct_status_counts(self):
        """
        Tests transaction statistics for a 5-minute interval.

        Given: A set of transactions within 2023-11-01 12:00-12:05
        When: Requesting transaction counts with 5-minute granularity
        Then: Returns one interval with correct HTTP status code counts (200,300,400,500)
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00.000",
            "2023-11-01T12:04:59.000"
        )
        
        self._assert_response_status_and_length(response, 200, 1)
        self._assert_status_counts(response, [(3, 1, 2, 0)])

    def test_30min_duration_with_5min_granularity_returns_six_5min_intervals(self):
        """
        Tests transaction statistics for a 30-minute period with 5-minute granularity.

        Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
        When: Requesting transaction counts with 5-minute granularity
        Then: Returns 6 intervals with correct status counts per interval
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00.000",
            "2023-11-01T12:29:59.999"
        )
        
        self._assert_response_status_and_length(response, 200, 6)
        self._assert_status_counts(response, [
            (3, 1, 2, 0),
            (2, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 1, 0),
            (2, 1, 0, 0),
            (3, 0, 0, 2),
        ])

    def test_1hour_duration_with_5min_granularity_returns_twelve_5min_intervals(self):
        """
        Tests transaction statistics for a 1-hour duration with 5-minute granularity.

        Given: Transactions spanning one hour (2023-11-01 12:00-13:00)
        When: Requesting transaction counts with 5-minute granularity
        Then: Returns 12 intervals with correct status counts per interval
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00.000",
            "2023-11-01T12:59:59.999"
        )
        
        self._assert_response_status_and_length(response, 200, 12)
        self._assert_status_counts(response, [
            (3, 1, 2, 0),
            (2, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 1, 0),
            (2, 1, 0, 0),
            (3, 0, 0, 2),
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (2, 0, 0, 0),
            (0, 0, 0, 0),
            (5, 0, 2, 0),
            (4, 1, 2, 0),
        ])

    def test_1month_duration_with_5min_granularity_returns_empty_list(self):
        """
        Tests transaction statistics for a 1-month duration with 5-minute granularity.

        Given: A time period with no recorded transactions
        When: Requesting transaction counts for October 2023
        Then: Returns an empty list
        """
        response = self.make_request(
            "5minutes",
            "2023-10-01T00:00.000",
            "2023-10-31T00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 0)


class TestHourlyTransactionCounts(TestBaseTransactionCounts):
    """Tests for hourly granularity transaction counts."""

    def test_30min_duration_with_hourly_granularity_returns_single_interval(self):
        """
        Tests counting the transactions in a 30 minute duration with hourly granularity.

        Given: Transactions within 30 minutes (2023-11-01 12:00-12:30)
        When: Requesting transaction counts with hourly granularity
        Then: Returns one interval with aggregated status counts
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00",
            "2023-11-01T12:30:00"
        )
        
        self._assert_response_status_and_length(response, 200, 1)
        self._assert_status_counts(response, [(11, 2, 3, 2)])

    def test_1hour_duration_with_hourly_granularity_returns_two_intervals(self):
        """
        Tests counting the transactions in a 1-hour duration (from 12:00 to 13:00) with hourly granularity (period=hour).

        Given: Transactions spanning one hour
        When: Requesting hourly transaction counts
        Then: Returns two intervals with correct aggregated counts
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00.000",
            "2023-11-01T13:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 2)
        self._assert_status_counts(response, [(23, 3, 7, 2), (0, 0, 0, 0)])

    def test_24hour_duration_with_hourly_granularity_returns_24_intervals(self):
        """
        Tests counting the transactions in a 24-hour duration (from 12:00 to 12:00 the next day) with hourly granularity (period=hour).

        Given: Transactions spanning 24 hours
        When: Requesting hourly transaction counts
        Then: Returns 24 intervals with correct status counts per hour
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00.000",
            "2023-11-02T11:59:59.999"
        )
        
        self._assert_response_status_and_length(response, 200, 24)
        self._assert_status_counts(response, [
            (23, 3, 7, 2),
            (1, 0, 0, 0),
            (1, 0, 2, 0),
            (1, 1, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (2, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (2, 0, 0, 2),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (4, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (1, 0, 0, 0),
        ])

    def test_1month_duration_with_hourly_granularity_returns_empty_list(self):
        """
        Tests counting the transactions in a 1-month duration (from 2023-10-01 to 2023-10-31) with hourly granularity (period=hour).

        Given: A month period without transactions (October 2023)
        When: Requesting hourly transaction counts
        Then: Returns empty list
        """
        response = self.make_request(
            "hour",
            "2023-10-01T00:00.000",
            "2023-10-31T00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 0)


class TestDailyTransactionCounts(TestBaseTransactionCounts):
    """Tests for daily granularity transaction counts."""

    def test_6hour_duration_with_daily_granularity_returns_single_interval(self):
        """
        Tests counting the transactions in a 6-hour duration (from 12:00 to 18:00) with daily granularity (period=day).

        Given: Transactions spanning 6 hours
        When: Requesting daily transaction counts
        Then: Returns one interval with aggregated status counts
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00.000",
            "2023-11-01T18:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 1)
        self._assert_status_counts(response, [(27, 4, 9, 2)])

    def test_1day_duration_with_daily_granularity_returns_single_interval(self):
        """
        Tests counting the transactions in a 1-day duration (from 2023-11-01 to 2023-11-02) with daily granularity (period=day).

        Given: Transactions spanning 1 day
        When: Requesting daily transaction counts
        Then: Returns one interval with aggregated status counts
        """
        response = self.make_request(
            "day",
            "2023-11-01T00:00.000",
            "2023-11-01T00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 1)
        self._assert_status_counts(response, [(29, 4, 9, 2)])

    def test_24hour_duration_with_daily_granularity_returns_two_intervals(self):
        """
        Tests counting the transactions in a 24-hour duration (from 2023-11-01 to 2023-11-02) with daily granularity (period=day).

        Given: Transactions spanning 2 days
        When: Requesting daily transaction counts
        Then: Returns two intervals with aggregated status counts
        """
        response = self.make_request(
            "day",
            "2023-11-01T13:00:00.000",
            "2023-11-02T13:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 2)
        self._assert_status_counts(response, [(6, 1, 2, 0), (9, 0, 0, 2)])

    def test_7day_duration_with_daily_granularity_returns_seven_intervals(self):
        """
        Tests counting the transactions in a 7-day duration (from 2023-11-01 to 2023-11-07) with daily granularity (period=day).

        Given: Transactions spanning 7 days
        When: Requesting daily transaction counts
        Then: Returns 7 intervals with aggregated status counts
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00.000",
            "2023-11-07T11:59:59.999"
        )
        
        self._assert_response_status_and_length(response, 200, 7)
        self._assert_status_counts(response, [
            (29, 4, 9, 2),
            (10, 0, 0, 2),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 1, 1, 0),
            (0, 0, 0, 0),
        ])

    def test_30day_duration_with_daily_granularity_returns_thirty_intervals(self):
        """
        Tests counting the transactions in a 30-day duration (from 2023-11-01 to 2023-11-30) with daily granularity (period=day).

        Given: Transactions spanning 30 days
        When: Requesting daily transaction counts
        Then: Returns 30 intervals with aggregated status counts
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00.000",
            "2023-11-30T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 30)
        self._assert_status_counts(response, [
            (29, 4, 9, 2),
            (10, 0, 0, 2),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 1, 1, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (3, 0, 0, 0),
            (1, 0, 0, 0),
            (0, 0, 2, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (1, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 0, 1),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 0, 0),
        ])


class TestWeeklyTransactionCounts(TestBaseTransactionCounts):
    """Tests for weekly granularity transaction counts."""

    def test_2month_duration_with_weekly_granularity_returns_nine_intervals(self):
        """
        Tests counting the transactions by status code in a 2-month duration (from 2023-11-01 to 2023-12-31) with weekly granularity (period=week).

        Given: Transactions spanning 2 months
        When: Requesting weekly transaction counts
        Then: Returns 9 intervals with aggregated status counts
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00.000",
            "2023-12-31T00:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 9)
        self._assert_status_counts(response, [
            (40, 5, 10, 4),
            (4, 0, 0, 0),
            (3, 0, 2, 0),
            (1, 0, 0, 1),
            (5, 1, 0, 0),
            (3, 0, 0, 0),
            (2, 0, 0, 0),
            (0, 3, 0, 0),
            (0, 0, 0, 0),
        ])

    def test_3day_duration_with_weekly_granularity_returns_single_interval(self):
        """
        Tests counting the transactions by status code in a 3-day duration (from 2023-11-01 to 2023-11-03) with weekly granularity (period=week).

        Given: Transactions spanning 3 days
        When: Requesting weekly transaction counts
        Then: Returns 1 interval with aggregated status counts
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00.000",
            "2023-11-03T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 1)
        self._assert_status_counts(response, [(39, 4, 9, 4)])

    def test_7day_duration_with_weekly_granularity_returns_two_intervals(self):
        """
        Tests counting the transactions by status code in a 7-day duration (from 2023-11-01 to 2023-11-07) with weekly granularity (period=week).

        Given: Transactions spanning 7 days
        When: Requesting weekly transaction counts
        Then: Returns 2 intervals with aggregated status counts
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00.000",
            "2023-11-07T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 2)
        self._assert_status_counts(response, [(40, 5, 10, 4), (0, 0, 0, 0)])

    def test_1month_duration_with_weekly_granularity_returns_single_interval(self):
        """
        Tests counting the transactions by status code in a 1-month duration (from 2024-03-29 to 2024-04-30) with weekly granularity (period=week).

        Given: A future time period without transactions
        When: Requesting weekly transaction counts
        Then: Returns empty list
        """
        response = self.make_request(
            "week",
            "2024-03-29T00:00:00.000",
            "2024-04-30T00:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 0)


class TestMonthlyTransactionCounts(TestBaseTransactionCounts):
    """Tests for monthly granularity transaction counts."""

    def test_7day_duration_with_monthly_granularity_returns_single_interval(self):
        """
        Tests counting the transactions by status code in a 7-day duration (from 2023-11-01 to 2023-11-07) with monthly granularity (period=month).

        Given: Transactions spanning 7 days
        When: Requesting monthly transaction counts
        Then: Returns 1 interval with aggregated status counts
        """
        response = self.make_request(
            "month",
            "2023-11-01T12:00:00.000",
            "2023-11-07T12:00:00"
        )
    
        # assert
        self._assert_response_status_and_length(response, 200, 1)
        self._assert_status_counts(response, [(40, 5, 10, 4)])

    def test_30day_duration_with_monthly_granularity_returns_single_interval(self):
        """
        Tests counting the transactions by status code in a 30-day duration (from 2023-11-01 to 2023-11-30) with monthly granularity (period=month).

        Given: Transactions spanning 30 days
        When: Requesting monthly transaction counts
        Then: Returns 1 interval with aggregated status counts
        """
        response = self.make_request(
            "month",
            "2023-11-01T12:00:00.000",
            "2023-11-30T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 1)
        self._assert_status_counts(response, [(50, 5, 12, 5)])

    def test_6month_duration_with_monthly_granularity_returns_six_intervals(self):
        """
        Tests counting the transactions by status code in a 6-month duration (from 2023-10-01 to 2024-03-31) with monthly granularity (period=month).

        Given: Transactions spanning 6 months
        When: Requesting monthly transaction counts
        Then: Returns 6 intervals with aggregated status counts
        """
        response = self.make_request(
            "month",
            "2023-10-01T12:00:00.000",
            "2024-03-31T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 6)
        self._assert_status_counts(response, [
            (0, 0, 0, 0),
            (50, 5, 12, 5),
            (10, 4, 0, 0),
            (6, 1, 1, 1),
            (0, 0, 0, 0),
            (7, 4, 4, 1),
        ])

    def test_1month_duration_with_monthly_granularity_returns_empty_list(self):
        """
        Tests counting the transactions by status code in a 1-month duration (from 2024-05-01 to 2024-05-31) with monthly granularity (period=month).

        Given: A month period without transactions (May 2024)
        When: Requesting monthly transaction counts
        Then: Returns empty list
        """
        response = self.make_request(
            "month",
            "2024-05-01T12:00:00.000",
            "2024-05-31T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 0)


class TestYearlyTransactionCounts(TestBaseTransactionCounts):
    """Tests for yearly granularity transaction counts."""

    def test_2month_duration_with_yearly_granularity_returns_single_interval(self):
        """
        Tests counting the transactions by status code in a 2-month duration (from 2023-11-01 to 2023-12-31) with yearly granularity (period=year).

        Given: Transactions spanning 2 months in 2023
        When: Requesting yearly transaction counts
        Then: Returns one interval with aggregated status counts
        """
        response = self.make_request(
            "year",
            "2023-11-01T12:00:00.000",
            "2023-12-31T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 1)
        self._assert_status_counts(response, [(59, 9, 12, 5)])

    def test_5month_duration_with_yearly_granularity_returns_two_intervals(self):
        """
        Tests counting the transactions by status code in a 5-month duration (from 2023-11-01 to 2024-03-31) with yearly granularity (period=year).

        Given: Transactions spanning 5 months across 2023-2024
        When: Requesting yearly transaction counts
        Then: Returns two intervals with aggregated status counts
        """
        response = self.make_request(
            "year",
            "2023-11-01T12:00:00.000",
            "2024-03-31T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 2)
        self._assert_status_counts(response, [(60, 9, 12, 5), (13, 5, 5, 2)])

    def test_9month_duration_with_yearly_granularity_returns_empty_interval(self):
        """
        Tests counting the transactions by status code in a 9-month duration (from 2024-03-31 to 2024-12-31) with yearly granularity (period=year).

        Given: A future time period without transactions
        When: Requesting yearly transaction counts
        Then: Returns empty list
        """
        response = self.make_request(
            "year", 
            "2024-03-31T12:00:00.000",
            "2024-12-31T12:00:00.000"
        )
        
        self._assert_response_status_and_length(response, 200, 0)

