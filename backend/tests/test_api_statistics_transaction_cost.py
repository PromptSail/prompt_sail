import pytest
from test_utils import read_transactions_with_prices_from_csv




class TestBaseTransactionCosts:
    @pytest.fixture(autouse=True)
    def setup(self, client, application):
        self.client = client
        self.application = application
        
        self.header = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
        }
        
        
        with self.application.transaction_context() as ctx:
            repo = ctx["transaction_repository"]
            repo.delete_cascade(project_id="project-test")
            
            config = self.application['config']
            
            transactions = read_transactions_with_prices_from_csv(
                "test_transactions_tokens_cost_speed.csv",
                config.PRICE_LIST_PATH
            )
            for transaction in transactions:
                repo.add(transaction)
        
        yield
        
        # Clean up test data
        with self.application.transaction_context() as ctx:
            repo = ctx["transaction_repository"]
            repo.delete_cascade(project_id="project-test")
    
    def make_request(self, period, date_from, date_to, project_id="project-test"):
        """Helper method to make API request for speed statistics."""
        
        if date_from is None:
            date_from = ""
        if date_to is None:
            date_to = ""    
        
        api_url = f"/api/statistics/transactions_cost?"
        #create api url add parameters if they are not empty
        
        if project_id != "":
            api_url += f"project_id={project_id}"
        
        if period != "":
            api_url += f"&period={period}"
        if date_from != "":
            api_url += f"&date_from={date_from}"
        if date_to != "":
            api_url += f"&date_to={date_to}"
        

        return self.client.get(
            api_url,
            headers=self.header,
        )
        


    def extract_tokens_and_costs(self, response):
        tokens = list(
            [
                tuple(
                    [
                        record["input_cumulative_total"] + record["output_cumulative_total"]
                        for record in date["records"]
                    ]
                )
                for date in response.json()
            ]
        )

        costs = list(
            [
                tuple(
                    [record["total_cost"] for record in date["records"]]
                )
                for date in response.json()
            ]
        )
        
        # costs = list(
        #     [
        #         tuple(map(lambda x: round(x * 1000000, 1), list(val)))
        #         for val in costs
        #     ]
        # )

        return tokens, costs

    def assert_response(self, response, expected_count, expected_tokens, expected_costs):
        assert response.status_code == 200
        assert len(response.json()) == expected_count
        
        actual_tokens, actual_costs = self.extract_tokens_and_costs(response)
        assert actual_tokens == expected_tokens , \
            f"Tokens are not equal: {actual_tokens} != {expected_tokens}"
        assert len(actual_costs) == len(expected_costs) , \
            f"Costs has different length: {len(actual_costs)} != {len(expected_costs)}"
        
        for actual, expected in zip(actual_costs, expected_costs):
            assert actual == pytest.approx(expected, rel=1e-4), \
                f"Costs are not equal: {actual} != {expected}"



class TestTransactionCostErrors(TestBaseTransactionCosts):
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
        
        #current implementation returns 200 and empty list
        assert response.status_code == 200
        assert len(response.json()) == 0
        
        # TODO: this should be changed in the future
        # assert response.status_code == 404
        # assert response.json() == {"error": "Project not found"}
        

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
        assert response_data['detail'] == "date_from cannot be after date_to"
        


class TestMinutesGranularity(TestBaseTransactionCosts):
    def test_5min_duration_with_5min_granularity_returns_single_interval_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 5-minute time frame with 5-minute granularity.

        Given: A set of transactions within 2023-11-01 12:00-12:05
        When: Requesting token and cost statistics with 5-minute granularity
        Then: Returns one interval with correct token counts and costs for each model
        """
        response = self.make_request(
            "5minutes", 
            "2023-11-01T12:00:00", 
            "2023-11-01T12:04:59"
        )
        
        tokens_validation = [tuple([174])]
        costs_validation = [tuple([0.0003155])]
        
        self.assert_response(response, 1, tokens_validation, costs_validation)

    def test_30min_duration_with_5min_granularity_returns_six_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 30-minute time frame with 5-minute granularity.

        Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
        When: Requesting token and cost statistics with 5-minute granularity
        Then: Returns 6 intervals with correct token counts and costs per model per interval
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:29:59"
        )

        tokens_validation = [
            tuple([0, 174, 0, 0]),
            tuple([0, 730, 142, 332]),
            tuple([0, 730, 142, 332]),
            tuple([107, 730, 142, 332]),
            tuple([107, 730, 1816, 332]),
            tuple([419, 835, 1816, 497]),
        ]

        costs_validation = [
            tuple([0, 0.0003155, 0, 0]),
            tuple([0, 0.0013275, 0.0000568, 0.01092]),
            tuple([0, 0.0013275, 0.0000568, 0.01092]),
            tuple([0.001896, 0.0013275, 0.0000568, 0.01092]),
            tuple([0.001896, 0.0013275, 0.0007264, 0.01092]),
            tuple([0.008808, 0.001523, 0.0007264, 0.01887]),
        ]

        self.assert_response(response, 6, tokens_validation, costs_validation)

    def test_1hour_duration_with_5min_granularity_returns_twelve_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 1-hour time frame with 5-minute granularity (period=5minutes).

        Given: Transactions spanning one hour (2023-11-01 12:00-13:00)
        When: Requesting token and cost statistics with 5-minute granularity
        Then: Returns 12 intervals with correct token counts and costs per model per interval
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:59:59"
        )

        tokens_validation = [
            tuple([0, 174, 0, 0]),
            tuple([0, 730, 142, 332]),
            tuple([0, 730, 142, 332]),
            tuple([107, 730, 142, 332]),
            tuple([107, 730, 1816, 332]),
            tuple([419, 835, 1816, 497]),
            tuple([419, 835, 1816, 497]),
            tuple([419, 2847, 1816, 497]),
            tuple([419, 3713, 1816, 497]),
            tuple([419, 3713, 1816, 497]),
            tuple([419, 7904, 1816, 497]),
            tuple([419, 7904, 2778, 578]),
        ]

        costs_validation = [
            tuple([0, 0.0003155, 0, 0]),
            tuple([0, 0.0013275, 0.0000568, 0.01092]),
            tuple([0, 0.0013275, 0.0000568, 0.01092]),
            tuple([0.001896, 0.0013275, 0.0000568, 0.01092]),
            tuple([0.001896, 0.0013275, 0.0007264, 0.01092]),
            tuple([0.008808, 0.001523, 0.0007264, 0.01887]),
            tuple([0.008808, 0.001523, 0.0007264, 0.01887]),
            tuple([0.008808, 0.005541, 0.0007264, 0.01887]),
            tuple([0.008808, 0.007212, 0.0007264, 0.01887]),
            tuple([0.008808, 0.007212, 0.0007264, 0.01887]),
            tuple([0.008808, 0.0151335, 0.0007264, 0.01887]),
            tuple([0.008808, 0.0151335, 0.0011112, 0.02292]),
        ]

        self.assert_response(response, 12, tokens_validation, costs_validation)

    def test_1month_duration_with_5min_granularity_returns_empty_list(self):
        """
        Tests token usage and cost statistics for a 1 month time frame with 5-minute granularity (period=5minutes).

        Given: A time period with no recorded transactions (October 2023)
        When: Requesting token and cost statistics with 5-minute granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "5minutes",
            "2023-10-01T12:00:00",
            "2023-10-31T12:30:00"
        )
        
        self.assert_response(response, 0, [], [])


class TestHourlyGranularity(TestBaseTransactionCosts):
    def test_30min_duration_with_hourly_granularity_returns_single_interval_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 30-minute time frame with hourly granularity (period=hour).

        Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
        When: Requesting token and cost statistics with hourly granularity
        Then: Returns one interval with aggregated token counts and costs per model
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00",
            "2023-11-01T12:30:00"
        )

        tokens_validation = [tuple([419, 835, 1816, 497])]
        costs_validation = [tuple([0.008808, 0.001523, 0.0007264, 0.01887])]

        self.assert_response(response, 1, tokens_validation, costs_validation)

    def test_1hour_duration_with_hourly_granularity_returns_two_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 1-hour time frame with hourly granularity (period=hour).

        Given: Transactions spanning one hour (2023-11-01 12:00-13:00)
        When: Requesting token and cost statistics with hourly granularity
        Then: Returns two intervals with aggregated token counts and costs per model
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00",
            "2023-11-01T13:00:00"
        )

        tokens_validation = [tuple([419, 7904, 2778, 578]), tuple([419, 7904, 2778, 578])]
        costs_validation = [
            tuple([0.008808, 0.0151335, 0.0011112, 0.02292]),
            tuple([0.008808, 0.0151335, 0.0011112, 0.02292]),
        ]

        self.assert_response(response, 2, tokens_validation, costs_validation)

    def test_24hour_duration_with_hourly_granularity_returns_24_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 24-hour time frame with hourly granularity (period=hour).

        Given: Transactions spanning 24 hours (2023-11-01 12:00 to 2023-11-02 12:00)
        When: Requesting token and cost statistics with hourly granularity
        Then: Returns 24 intervals with aggregated token counts and costs per model per hour
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00",
            "2023-11-02T11:59:59"
        )

        tokens_validation = [
            tuple([419, 7904, 2778, 578]),
            tuple([419, 7953, 2778, 578]),
            tuple([419, 8045, 2778, 578]),
            tuple([1231, 8045, 2778, 578]),
            tuple([1231, 8045, 2778, 578]),
            tuple([1468, 8045, 2778, 578]),
            tuple([1468, 8045, 2778, 578]),
            tuple([1468, 8045, 2778, 578]),
            tuple([1781, 8079, 2778, 578]),
            tuple([1781, 8079, 2778, 578]),
            tuple([1781, 8079, 2778, 578]),
            tuple([1781, 8079, 2778, 578]),
            tuple([1781, 8079, 2778, 578]),
            tuple([1781, 8079, 2778, 578]),
            tuple([1781, 8079, 2778, 578]),
            tuple([1781, 8079, 2778, 578]),
            tuple([1781, 8079, 2787, 941]),
            tuple([1781, 8079, 2787, 941]),
            tuple([1781, 8079, 2787, 941]),
            tuple([1781, 8079, 2787, 941]),
            tuple([1871, 8079, 4429, 941]),
            tuple([1871, 8079, 4429, 941]),
            tuple([2253, 8079, 4429, 941]),
            tuple([2253, 8079, 5337, 941]),
        ]

        costs_validation = [
            tuple([0.008808, 0.0151335, 0.0011112, 0.02292]),
            tuple([0.008808, 0.0152295, 0.0011112, 0.02292]),
            tuple([0.008808, 0.01538, 0.0011112, 0.02292]),
            tuple([0.02788, 0.01538, 0.0011112, 0.02292]),
            tuple([0.02788, 0.01538, 0.0011112, 0.02292]),
            tuple([0.03312, 0.01538, 0.0011112, 0.02292]),
            tuple([0.03312, 0.01538, 0.0011112, 0.02292]),
            tuple([0.03312, 0.01538, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.040216, 0.0154425, 0.0011148, 0.04176]),
            tuple([0.040216, 0.0154425, 0.0011148, 0.04176]),
            tuple([0.040216, 0.0154425, 0.0011148, 0.04176]),
            tuple([0.040216, 0.0154425, 0.0011148, 0.04176]),
            tuple([0.041304, 0.0154425, 0.0017716, 0.04176]),
            tuple([0.041304, 0.0154425, 0.0017716, 0.04176]),
            tuple([0.04988, 0.0154425, 0.0017716, 0.04176]),
            tuple([0.04988, 0.0154425, 0.0021348, 0.04176]),
        ]

        self.assert_response(response, 24, tokens_validation, costs_validation)

    def test_1month_duration_with_hourly_granularity_returns_empty_list(self):
        """
        Tests token usage and cost statistics for a 1 month time frame with no transactions with hourly granularity (period=hour).

        Given: A time period with no recorded transactions (2023-10-01 to 2023-10-31)
        When: Requesting token and cost statistics with hourly granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "hour",
            "2023-10-01T12:00:00",
            "2023-10-31T18:00:00"
        )

        self.assert_response(response, 0, [], [])


class TestDailyGranularity(TestBaseTransactionCosts):
    def test_6hour_duration_with_daily_granularity_returns_single_interval_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 6-hour time frame with daily granularity (period=day).

        Given: Transactions spanning 6 hours (2023-11-01 12:00-18:00)
        When: Requesting token and cost statistics with daily granularity
        Then: Returns one interval with aggregated token counts and costs per model
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00",
            "2023-11-01T18:00:00"
        )

        tokens_validation = [tuple([1468, 8045, 2778, 578])]
        costs_validation = [tuple([0.03312, 0.01538, 0.0011112, 0.02292])]

        self.assert_response(response, 1, tokens_validation, costs_validation)

    def test_24hour_duration_with_daily_granularity_returns_single_interval_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 24-hour time frame with daily granularity (period=day).

        Given: Transactions spanning 24 hours (2023-11-01 00:00-23:59), dates without time
        When: Requesting token and cost statistics with daily granularity
        Then: Returns one interval with aggregated token counts and costs per model
        """
        response = self.make_request(
            "day",
            "2023-11-01",
            "2023-11-01"
        )

        tokens_validation = [tuple([1781, 8079, 2778, 578])]
        costs_validation = [tuple([0.040216, 0.0154425, 0.0011112, 0.02292])]

        self.assert_response(response, 1, tokens_validation, costs_validation)

    def test_1day_duration_with_daily_granularity_returns_two_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 1-day time frame with daily granularity (period=day).

        Given: Transactions spanning one day (2023-11-01 13:00 to 2023-11-02 13:00)
        When: Requesting token and cost statistics with daily granularity
        Then: Returns two intervals with aggregated token counts and costs per model
        """
        response = self.make_request(
            "day",
            "2023-11-01T13:00:00",
            "2023-11-02T13:00:00"
        )

        tokens_validation = [tuple([1362, 175, 0, 0]), tuple([2085, 175, 2559, 363])]
        costs_validation = [
            tuple([0.031408, 0.000309, 0.0, 0.0]),
            tuple([0.046632, 0.000309, 0.0010236, 0.01884]),
        ]

        self.assert_response(response, 2, tokens_validation, costs_validation)

    def test_7day_duration_with_daily_granularity_returns_seven_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 7-day time frame with daily granularity (period=day).

        Given: Transactions spanning 7 days (2023-11-01 to 2023-11-07)
        When: Requesting token and cost statistics with daily granularity
        Then: Returns 7 intervals with aggregated token counts and costs per model per day
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00",
            "2023-11-07T11:59:59"
        )

        tokens_validation = [
            tuple([1781, 8079, 2778, 578]),
            tuple([2805, 8079, 5337, 941]),
            tuple([2805, 8079, 5337, 941]),
            tuple([2805, 8079, 5337, 941]),
            tuple([2805, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 941]),
        ]

        costs_validation = [
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.062264, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.062264, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.062264, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.062264, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
        ]

        self.assert_response(response, 7, tokens_validation, costs_validation)

    def test_1month_duration_with_daily_granularity_returns_30_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 1-month time frame with daily granularity (period=day).

        Given: Transactions spanning one month (2023-11-01 to 2023-11-30)
        When: Requesting token and cost statistics with daily granularity
        Then: Returns 30 intervals with aggregated token counts and costs per model per day
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00.000",
            "2023-11-30T12:00:00.000"
        )

        tokens_validation = [
            tuple([1781, 8079, 2778, 578]),
            tuple([2805, 8079, 5337, 941]),
            tuple([2805, 8079, 5337, 941]),
            tuple([2805, 8079, 5337, 941]),
            tuple([2805, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 941]),
            tuple([2902, 8079, 5337, 1390]),
            tuple([2902, 8079, 6348, 2090]),
            tuple([2902, 8079, 6348, 2090]),
            tuple([2902, 8079, 6348, 2090]),
            tuple([2902, 8079, 6348, 2090]),
            tuple([2902, 8079, 6631, 2090]),
            tuple([2902, 8079, 6631, 2090]),
            tuple([2902, 8498, 6631, 2090]),
            tuple([2902, 8643, 6631, 2090]),
            tuple([2902, 8643, 6631, 2090]),
            tuple([2902, 8643, 6631, 2090]),
            tuple([2902, 8643, 6631, 2090]),
            tuple([2902, 8643, 6631, 2090]),
            tuple([2902, 8643, 6631, 2152]),
            tuple([2902, 8643, 6631, 2152]),
            tuple([2902, 8643, 6631, 2152]),
            tuple([2902, 8643, 6631, 32357]),
            tuple([2902, 8643, 6631, 32357]),
            tuple([2902, 8643, 13616, 32357]),
        ]

        costs_validation = [
            tuple([0.040216, 0.0154425, 0.0011112, 0.02292]),
            tuple([0.062264, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.062264, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.062264, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.062264, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.06414]),
            tuple([0.063408, 0.0154425, 0.0025392, 0.10527]),
            tuple([0.063408, 0.0154425, 0.0025392, 0.10527]),
            tuple([0.063408, 0.0154425, 0.0025392, 0.10527]),
            tuple([0.063408, 0.0154425, 0.0025392, 0.10527]),
            tuple([0.063408, 0.0154425, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0154425, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0162695, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.108]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.108]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.108]),
            tuple([0.063408, 0.0165265, 0.0026524, 1.9143]),
            tuple([0.063408, 0.0165265, 0.0026524, 1.9143]),
            tuple([0.063408, 0.0165265, 0.0054464, 1.9143]),
        ]

        self.assert_response(response, 30, tokens_validation, costs_validation)

    def test_1day_duration_with_daily_granularity_returns_empty_list(self):
        """
        Tests token usage and cost statistics for a 1 day time frame with no transactions with daily granularity (period=day).

        Given: A time period with no recorded transactions (2023-11-03 to 2023-11-04)
        When: Requesting token and cost statistics with daily granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "day",
            "2023-11-03T12:00:00",
            "2023-11-04T12:00:00"
        )

        self.assert_response(response, 0, [], [])


class TestWeeklyGranularity(TestBaseTransactionCosts):
    def test_3day_duration_with_weekly_granularity_returns_single_interval_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 3-day time frame with weekly granularity (period=week).

        Given: Transactions spanning 3 days (2023-11-01 to 2023-11-03)
        When: Requesting token and cost statistics with weekly granularity
        Then: Returns one interval with aggregated token counts and costs per model
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00",
            "2023-11-03T12:00:00"
        )

        tokens_validation = [tuple([2805, 8079, 5337, 941])]
        costs_validation = [tuple([0.062264, 0.0154425, 0.0021348, 0.04176])]

        self.assert_response(response, 1, tokens_validation, costs_validation)

    def test_7day_duration_with_weekly_granularity_returns_two_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 7-day time frame with weekly granularity (period=week).

        Given: Transactions spanning 7 days (2023-11-01 to 2023-11-07)
        When: Requesting token and cost statistics with weekly granularity
        Then: Returns two intervals with aggregated token counts and costs per model
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00",
            "2023-11-07T12:00:00"
        )

        tokens_validation = [tuple([2902, 8079, 5337, 941]), tuple([2902, 8079, 5337, 941])]
        costs_validation = [
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
        ]

        self.assert_response(response, 2, tokens_validation, costs_validation)

    def test_2month_duration_with_weekly_granularity_returns_nine_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 2-month time frame with weekly granularity (period=week).

        Given: Transactions spanning 2 months (2023-11-01 to 2023-12-31)
        When: Requesting token and cost statistics with weekly granularity
        Then: Returns 9 intervals with aggregated token counts and costs per model per week
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00",
            "2023-12-31T00:00:00"
        )

        tokens_validation = [
            tuple([2902, 8079, 5337, 941]),
            tuple([2902, 8079, 6348, 2090]),
            tuple([2902, 8643, 6631, 2090]),
            tuple([2902, 8643, 6631, 2152]),
            tuple([2902, 8643, 13730, 33279]),
            tuple([3877, 8859, 13730, 33279]),
            tuple([4682, 9159, 13730, 33279]),
            tuple([4682, 9159, 13730, 33279]),
            tuple([4682, 9159, 13730, 33279]),
        ]

        costs_validation = [
            tuple([0.063408, 0.0154425, 0.0021348, 0.04176]),
            tuple([0.063408, 0.0154425, 0.0025392, 0.10527]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.10527]),
            tuple([0.063408, 0.0165265, 0.0026524, 0.108]),
            tuple([0.063408, 0.0165265, 0.005492, 1.96632]),
            tuple([0.085768, 0.016896, 0.005492, 1.96632]),
            tuple([0.104496, 0.0174505, 0.005492, 1.96632]),
            tuple([0.104496, 0.0174505, 0.005492, 1.96632]),
            tuple([0.104496, 0.0174505, 0.005492, 1.96632]),
        ]

        self.assert_response(response, 9, tokens_validation, costs_validation)

    def test_2week_duration_with_weekly_granularity_returns_empty_list(self):
        """
        Tests token usage and cost statistics for a 2-week time frame with no transactions with weekly granularity (period=week).

        Given: A time period with no recorded transactions (2024-03-29 to 2024-04-12)
        When: Requesting token and cost statistics with weekly granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "week",
            "2024-03-29T00:00:00",
            "2024-04-12T00:00:00"
        )

        self.assert_response(response, 0, [], [])


class TestMonthlyGranularity(TestBaseTransactionCosts):
    def test_7day_duration_with_monthly_granularity_returns_single_interval_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 7-day time frame with monthly granularity (period=month).

        Given: Transactions spanning 7 days (2023-11-01 to 2023-11-07)
        When: Requesting token and cost statistics with monthly granularity
        Then: Returns one interval with aggregated token counts and costs per model
        """
        response = self.make_request(
            "month",
            "2023-11-01T12:00:00",
            "2023-11-07T12:00:00"
        )

        tokens_validation = [tuple([2902, 8079, 5337, 941])]
        costs_validation = [tuple([0.063408, 0.0154425, 0.0021348, 0.04176])]

        self.assert_response(response, 1, tokens_validation, costs_validation)

    def test_1month_duration_with_monthly_granularity_returns_single_interval_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 1-month time frame with monthly granularity (period=month).

        Given: Transactions spanning one month (2023-11-01 to 2023-11-30)
        When: Requesting token and cost statistics with monthly granularity
        Then: Returns one interval with aggregated token counts and costs per model
        """
        response = self.make_request(
            "month",
            "2023-11-01",
            "2023-11-30"
        )

        tokens_validation = [tuple([2902, 8643, 13616, 32357])]
        costs_validation = [tuple([0.063408, 0.0165265, 0.0054464, 1.9143])]

        self.assert_response(response, 1, tokens_validation, costs_validation)

    def test_6month_duration_with_monthly_granularity_returns_six_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 6-month time frame with monthly granularity (period=month).

        Given: Transactions spanning 6 months (2023-10-01 to 2024-03-31)
        When: Requesting token and cost statistics with monthly granularity
        Then: Returns 6 intervals with aggregated token counts and costs per model per month
        """
        response = self.make_request(
            "month",
            "2023-10-01",
            "2024-03-31"
        )

        tokens_validation = [
            tuple([0, 0, 0, 0]),
            tuple([2902, 8643, 13616, 32357]),
            tuple([4682, 9384, 13730, 33279]),
            tuple([4975, 9804, 14278, 34344]),
            tuple([4975, 9804, 14278, 34344]),
            tuple([5586, 9804, 14278, 61424]),
        ]

        costs_validation = [
            tuple([0.0, 0.0, 0.0, 0.0]),
            tuple([0.063408, 0.0165265, 0.0054464, 1.9143]),
            tuple([0.104496, 0.0178535, 0.005492, 1.96632]),
            tuple([0.11116, 0.0186715, 0.0057112, 2.02788]),
            tuple([0.11116, 0.0186715, 0.0057112, 2.02788]),
            tuple([0.123792, 0.0186715, 0.0057112, 3.5808]),
        ]

        self.assert_response(response, 6, tokens_validation, costs_validation)

    def test_1month_duration_with_monthly_granularity_returns_empty_list(self):
        """
        Tests token usage and cost statistics for a 1 month time frame with no transactions with monthly granularity (period=month).

        Given: A time period with no recorded transactions (2024-05-01 to 2024-06-01)
        When: Requesting token and cost statistics with monthly granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "month",
            "2024-05-01",
            "2024-06-01"
        )

        self.assert_response(response, 0, [], [])


class TestYearlyGranularity(TestBaseTransactionCosts):
    def test_2month_duration_with_yearly_granularity_returns_single_interval_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 2-month time frame with yearly granularity (period=year).

        Given: Transactions spanning 2 months (2023-11-01 to 2023-12-31)
        When: Requesting token and cost statistics with yearly granularity
        Then: Returns one interval with aggregated token counts and costs per model
        """
        response = self.make_request(
            "year",
            "2023-11-01",
            "2023-12-31"
        )

        tokens_validation = [tuple([4682, 9245, 13730, 33279])]
        costs_validation = [tuple([0.104496, 0.017596, 0.005492, 1.96632])]

        self.assert_response(response, 1, tokens_validation, costs_validation)

    def test_5month_duration_with_yearly_granularity_returns_two_intervals_with_tokens_and_costs(self):
        """
        Tests token usage and cost statistics for a 5-month time frame with yearly granularity (period=year).

        Given: Transactions spanning from 2023 to 2024 (2023-11-01 to 2024-03-31)
        When: Requesting token and cost statistics with yearly granularity
        Then: Returns two intervals with aggregated token counts and costs per model per year
        """
        response = self.make_request(
            "year",
            "2023-11-01",
            "2024-03-31"
        )

        tokens_validation = [
            tuple([4682, 9384, 13730, 33279]),
            tuple([5586, 9804, 14278, 61424]),
        ]

        costs_validation = [
            tuple([0.104496, 0.0178535, 0.005492, 1.96632]),
            tuple([0.123792, 0.0186715, 0.0057112, 3.5808]),
        ]

        self.assert_response(response, 2, tokens_validation, costs_validation)

    def test_6month_duration_with_yearly_granularity_returns_empty_list(self):
        """
        Tests token usage and cost statistics for a 6-month time frame with no transactions with yearly granularity (period=year).

        Given: A time period with no recorded transactions (2024-05-31 to 2024-12-31)
        When: Requesting token and cost statistics with yearly granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "year",
            "2024-05-31",
            "2024-12-31"
        )

        self.assert_response(response, 0, [], [])