import pytest
from datetime import datetime
from test_utils import read_transactions_from_csv, truncate_float

class TestBaseTransactionSpeed:
    """Base test class for transaction speed statistics tests."""
    
    @pytest.fixture(autouse=True)
    def setup(self, client, application):
        """Setup test data and common test fixtures."""
        self.client = client
        self.application = application
        self.header = {
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
        }
        
        # Load and add test transactions
        with self.application.transaction_context() as ctx:
            repo = ctx["transaction_repository"]
            repo.delete_cascade(project_id="project-test")
            transactions = read_transactions_from_csv(
                "test_transactions_tokens_cost_speed.csv"
            )
            for transaction in transactions:
                repo.add(transaction)
                
        yield
        
        # Cleanup test data
        with self.application.transaction_context() as ctx:
            repo = ctx["transaction_repository"]
            repo.delete_cascade(project_id="project-test")

    def make_request(self, period, date_from, date_to, project_id="project-test"):
        """Helper method to make API request for speed statistics."""
        
        if date_from is None:
            date_from = ""
        if date_to is None:
            date_to = ""    
        
        api_url = f"/api/statistics/transactions_speed?"
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

    def extract_tokens_per_second(self, response):
        """Helper method to extract tokens per second from response."""
        return list(
            [
                tuple(
                    [
                        truncate_float(record["tokens_per_second"], 3)
                        for record in date["records"]
                    ]
                )
                for date in response.json()
            ]
        )

    def assert_response(self, response, expected_count, expected_speeds):
        """Helper method to verify response status, length and speed values."""
        assert response.status_code == 200
        assert len(response.json()) == expected_count
        
        actual_speeds = self.extract_tokens_per_second(response)
        expected_speeds = [
            tuple(map(lambda x: truncate_float(x, 3), list(val))) 
            for val in expected_speeds
        ]
        
        assert actual_speeds == expected_speeds


class TestTransactionSpeedAPIContract(TestBaseTransactionSpeed):
    """Tests for API contract in transaction speed statistics. Check for errors and invalid parameters and contract for returned data."""

    def test_speed_statistics_for_not_existing_project(self):
        """
        Tests transaction speed statistics for a not existing project.

        Given: A set of transactions for a different project
        When: Requesting speed statistics for non-existent project
        Then: Returns 404 error with "Project not found" message
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
        
    def test_speed_statistics_without_project_id(self):
        """
        Tests transaction speed statistics without project_id.

        Given: A set of transactions
        When: Requesting speed statistics without project_id
        Then: Returns 422 error with "project_id is required" message
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:04:59",
            ""
        )
        
        resp_data = response.json()
        
        assert response.status_code == 422
        assert resp_data['detail'][0]['msg'] == 'Field required'

    def test_speed_statistics_wrong_period(self):
        """
        Tests transaction speed statistics for an invalid period parameter.

        Given: A set of valid transactions
        When: Requesting speed statistics with invalid period
        Then: Returns 422 error with validation details
        """
        response = self.make_request(
            "not-existing-period",
            "2023-11-01T12:00:00",
            "2023-11-01T12:29:59"
        )
        
        assert response.status_code == 422
        assert response.json()['detail'][0]['input'] == 'not-existing-period'

    def test_speed_statistics_for_date_from_after_date_to(self):
        """
        Tests transaction speed statistics with invalid date range.

        Given: A set of valid transactions
        When: Requesting speed statistics with date_from after date_to
        Then: Returns 400 error with invalid date range message
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:10:00",
            "2023-11-01T12:00:00"
        )
        
        assert response.status_code == 400
        assert response.json()['detail'] == "date_from cannot be after date_to"
        
    def test_speed_statistics_date_from_required(self):
        """
        Tests transaction speed statistics without date_from.

        Given: A set of valid transactions
        When: Requesting speed statistics without date_from
        Then: Returns 422 error with "date_from is required" message
        """
        response = self.make_request(
            "5minutes",
            None,
            "2023-11-01T12:00:00"
        )
        
        resp_data = response.json()
        
        assert response.status_code == 422
        assert resp_data['detail'][0]['msg'] == "Field required"
    
    def test_speed_statistics_not_valid_dates_from(self):
        """
        Tests transaction speed statistics with not valid date_from.

        Given: A set of valid transactions
        When: Requesting speed statistics with not valid date_from
        Then: Returns 422 error with validation details
        """
        response = self.make_request(
            "5minutes",
            "2023-11-31T12:00:00",
            "2023-11-31T12:10:00"
        )
        
        resp_data = response.json()
        
        assert response.status_code == 400
        assert resp_data['detail'] == "Invalid date format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS: day is out of range for month"
        
    def test_speed_statistics_date_to_required(self):
        """
        Tests transaction speed statistics without date_to.

        Given: A set of valid transactions
        When: Requesting speed statistics without date_to
        Then: Returns 422 error with "date_to is required" message
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            None
        )
        
        resp_data = response.json()
        
        assert response.status_code == 422
        assert resp_data['detail'][0]['msg'] == "Field required"
        
    def test_speed_statistics_dates_not_iso_format(self):
        """
        Tests transaction speed statistics with dates not in ISO format.

        Given: A set of valid transactions
        When: Requesting speed statistics with dates not in ISO format
        Then: Returns 400 error with invalid date format message
        """
        response_datetime = self.make_request(
            "5minutes",
            datetime(2023, 11, 1, 12, 0, 0), # not ISO format 2023-11-02 12:00:00 (without "T" between date and time)
            datetime(2023, 11, 2, 12, 0, 0)  # not ISO format 2023-11-02 12:00:00 (without "T" between date and time)
        )
        
        assert response_datetime.status_code == 400
        assert response_datetime.json()['detail'] == "Invalid date format. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS: Invalid date format"

        
    def test_speed_statistics_date_without_time_is_same_as_with_time(self):
        """
        Tests transaction speed statistics with date_from without time is same as with time.

        Given: A set of valid transactions
        When: Requesting speed statistics with date_from without time and with time
        Then: Time shoud be added automatically as 00:00:00 and returns same data
        """
        response_without_time = self.make_request(
            "5minutes",
            "2023-11-01",
            "2023-11-02"
        )
        
        response_with_time = self.make_request(
            "5minutes",
            "2023-11-01T00:00:00",
            "2023-11-02T00:00:00"
        )
               
        assert response_without_time.status_code == 200
        assert response_with_time.status_code == 200
        
        
        data_without_time = response_without_time.json()
        data_with_time = response_with_time.json()
        
        assert len(data_without_time) == 289
        assert len(data_without_time) == len(data_with_time)
                
        assert data_without_time == data_with_time
        
    def test_speed_statistics_5min_granularity_2_data_keypoints(self):
        """
        Tests transaction speed statistics returned data contract for 5-minute granularity in 9:59 minutes period.
        
        Given: Transactions for 9:59 minutes period
        When: Requesting speed statistics with 5-minute granularity
        Then: Returns 2 intervals with proper data keys and records with all the fields according to the contract
        """
        
        
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:09:59"
        )
        resp_data = response.json()
        
        expected_dates = [ datetime.fromisoformat("2023-11-01T12:00:00"), 
                           datetime.fromisoformat("2023-11-01T12:05:00"),
        ]
        
        response_dates = [ datetime.fromisoformat(resp_data[0]['date']), 
                           datetime.fromisoformat(resp_data[1]['date'])
        ]
        
        assert len(resp_data) == 2
        assert response_dates == expected_dates
        assert len(resp_data[0]['records']) == 3
        assert len(resp_data[1]['records']) == 3
        
        records_0 = resp_data[0]['records']
        records_1 = resp_data[1]['records']
        
          
        #provider Azure OpenAI gpt-35-turbo-0613
        assert records_0[0]['provider'] == 'Azure OpenAI'
        assert records_0[0]['model'] == 'gpt-35-turbo-0613'
        assert records_0[0]['mean_latency'] == pytest.approx(6.0, rel=1e-3)
        assert records_0[0]['tokens_per_second'] == pytest.approx(31.77272727, rel=1e-3)
        assert records_0[0]['total_transactions'] == 2
        
        #provider OpenAI babbage-002
        assert records_0[1]['provider'] == 'OpenAI'
        assert records_0[1]['model'] == 'babbage-002'
        assert records_0[1]['mean_latency'] == pytest.approx(0.0, rel=1e-3)
        assert records_0[1]['tokens_per_second'] == pytest.approx(0.0, rel=1e-3)
        assert records_0[1]['total_transactions'] == 0
        
        #provider OpenAI gpt-4-0613
        assert records_0[2]['provider'] == 'OpenAI'
        assert records_0[2]['model'] == 'gpt-4-0613'
        assert records_0[2]['mean_latency'] == pytest.approx(0.0, rel=1e-3)
        assert records_0[2]['tokens_per_second'] == pytest.approx(0.0, rel=1e-3)
        assert records_0[2]['total_transactions'] == 0
        
        #provider Azure OpenAI gpt-35-turbo-0613
        assert records_1[0]['provider'] == 'Azure OpenAI'
        assert records_1[0]['model'] == 'gpt-35-turbo-0613'
        assert records_1[0]['mean_latency'] == pytest.approx(120.999, rel=1e-3)
        assert records_1[0]['tokens_per_second'] == pytest.approx(2.9421730, rel=1e-3)
        assert records_1[0]['total_transactions'] == 1
        
        #provider OpenAI babbage-002
        assert records_1[1]['provider'] == 'OpenAI'
        assert records_1[1]['model'] == 'babbage-002'
        assert records_1[1]['mean_latency'] == pytest.approx(10.0, rel=1e-3)
        assert records_1[1]['tokens_per_second'] == pytest.approx(7.7, rel=1e-3)
        assert records_1[1]['total_transactions'] == 1
        
        #provider OpenAI gpt-4-0613
        assert records_1[2]['provider'] == 'OpenAI'
        assert records_1[2]['model'] == 'gpt-4-0613'
        assert records_1[2]['mean_latency'] == pytest.approx(2.0, rel=1e-3)
        assert records_1[2]['tokens_per_second'] == pytest.approx(16.0, rel=1e-3)
        assert records_1[2]['total_transactions'] == 1
        
    def test_speed_statistics_5min_granularity_3_data_keypoints(self):
        """
        Tests transaction speed statistics returned data contract for 5-minute granularity in 10 minutes period.
        
        Given: Transactions for 10 minutes period
        When: Requesting speed statistics with 5-minute granularity
        Then: Returns proper number of intervals with proper data keys and records with all the fields according to the contract
        """
        
        
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:10:00"
        )
        resp_data = response.json()
        
        expected_dates = [ datetime.fromisoformat("2023-11-01T12:00:00"), 
                           datetime.fromisoformat("2023-11-01T12:05:00"),
                           datetime.fromisoformat("2023-11-01T12:10:00"),
        ]
        
        response_dates = [ datetime.fromisoformat(resp_data[0]['date']), 
                           datetime.fromisoformat(resp_data[1]['date']),
                           datetime.fromisoformat(resp_data[2]['date'])
        ]
        
        assert len(resp_data) == 3
        assert response_dates == expected_dates
               
        assert len(resp_data[0]['records']) == 3
        assert len(resp_data[1]['records']) == 3
        assert len(resp_data[2]['records']) == 3
        
        records_0 = resp_data[0]['records']
        records_1 = resp_data[1]['records']
        records_2 = resp_data[2]['records']
        
        #goes for all records in 3 data points, 
        for i in range(3):
            # check if records contain the keys as expected
            assert all(key in records_0[i] for key in ['provider', 'model', 'mean_latency', 'tokens_per_second', 'total_transactions'])
            assert all(key in records_1[i] for key in ['provider', 'model', 'mean_latency', 'tokens_per_second', 'total_transactions'])
            assert all(key in records_2[i] for key in ['provider', 'model', 'mean_latency', 'tokens_per_second', 'total_transactions'])
            
            # checks if all the providers and models are the same in all 3 data points    
            assert records_0[i]['provider'] == records_1[i]['provider'] == records_2[i]['provider']
            assert records_0[i]['model'] == records_1[i]['model'] == records_2[i]['model']
               
        
    @pytest.mark.parametrize("period,date_from,date_to,expected_dates", [
        # 5 minutes granularity
        (
            "5minutes",
            "2023-11-01T12:00:00", 
            "2023-11-01T12:10:00",
            [
                "2023-11-01T12:00:00",
                "2023-11-01T12:05:00",
                "2023-11-01T12:10:00"
            ]
        ),
        (
            "5minutes",
            "2023-11-01T12:00:00", 
            "2023-11-01T12:09:59",
            [
                "2023-11-01T12:00:00",
                "2023-11-01T12:05:00",
            ]
        ),
        ( # period starts in the middle of the interval
            "5minutes",
            "2023-11-01T12:02:00", 
            "2023-11-01T12:09:59",
            [
                "2023-11-01T12:00:00",
                "2023-11-01T12:05:00",
            ]
        ),
        (
            "5minutes",
            "2023-11-01T23:55:00", 
            "2023-11-02T00:00:00",
            [
                # empty data in this period
            ]
        ),
        # hourly granularity
        (
            "hour",
            "2023-11-01T12:00:00", 
            "2023-11-01T13:00:00",
            [
                "2023-11-01T12:00:00",
                "2023-11-01T13:00:00"
            ]
        ),
        (
            "hour",
            "2023-11-01T12:00:00", 
            "2023-11-01T14:00:00",
            [
                "2023-11-01T12:00:00", 
                "2023-11-01T13:00:00",
                "2023-11-01T14:00:00"
            ]
        ),
        (
            "hour",
            "2023-11-01T12:00:00", 
            "2023-11-01T13:59:59",
            [
                "2023-11-01T12:00:00", 
                "2023-11-01T13:00:00",
            ]
        ),
        ( # period starts in the middle of the interval
            "hour",
            "2023-11-01T12:30:00", 
            "2023-11-01T13:30:00",
            [
                "2023-11-01T12:00:00", 
                "2023-11-01T13:00:00",
            ]
        ),
               ( # period starts in the middle of the interval
            "hour",
            "2023-11-01T11:59:59", 
            "2023-11-01T13:30:00",
            [
                "2023-11-01T11:00:00",
                "2023-11-01T12:00:00", 
                "2023-11-01T13:00:00",
            ]
        ),
        
        (
            "hour",
            "2023-11-01T23:00:00", 
            "2023-11-02T00:00:00",
            [
                #empty data in this period
            ]
        ),
        # daily granularity
        (
            "day",
            "2023-11-01T00:00:00", 
            "2023-11-03T00:00:00",
            [
                "2023-11-01T00:00:00",
                "2023-11-02T00:00:00",
                "2023-11-03T00:00:00"
            ]
        ),
        (
            "day",
            "2023-11-01T12:00:00", 
            "2023-11-02T12:00:00",
            [
                "2023-11-01T00:00:00",
                "2023-11-02T00:00:00",
            ]
        ),
        (
            "day",
            "2023-11-01", 
            "2023-11-01",
            [
                "2023-11-01T00:00:00",
            ]
        ),
        ( # period starts in the middle of the interval
            "day",
            "2023-11-30T23:59:59", 
            "2023-12-02T12:00:00",
            [
                "2023-11-30T00:00:00",
                "2023-12-01T00:00:00",
                "2023-12-02T00:00:00",
            ]
        ),
        # weekly granularity
        ( # each week starts on a monday, we should return as a data point the end of the week (Monday 00:00:00)
            "week",
            "2023-11-01T00:00:00", 
            "2023-11-15T00:00:00",
            [
                "2023-11-06T00:00:00",
                "2023-11-13T00:00:00",
                "2023-11-20T00:00:00"
            ]
        ),
        ( # each week starts on a monday, we should return as a data point the end of the week (Monday 00:00:00)
            "week",
            "2023-11-06T00:00:00", 
            "2023-11-15T00:00:00",
            [
                "2023-11-06T00:00:00",
                "2023-11-13T00:00:00",
                "2023-11-20T00:00:00"
            ]
        ),
        ( # each week starts on a monday, we should return as a data point the end of the week (Monday 00:00:00)
            "week",
            "2023-11-06T00:00:01", 
            "2023-11-15T00:00:00",
            [
                "2023-11-06T00:00:00",
                "2023-11-13T00:00:00",
                "2023-11-20T00:00:00"
            ]
        ),
        ( # each week starts on a 
            "week",
            "2023-11-06T15:00:00", 
            "2023-11-13T23:59:59",
            [
                "2023-11-06T00:00:00",
                "2023-11-13T00:00:00",
            ]
        ),
        ( 
            "week",
            "2023-11-07T00:00:00", 
            "2023-11-15T00:00:00",
            [
                "2023-11-13T00:00:00",
                "2023-11-20T00:00:00"
            ]
        ),
        # monthly granularity
        (
            "month",
            "2023-11-01T00:00:00", 
            "2024-01-01T00:00:00",
            [
                "2023-11-30T00:00:00",
                "2023-12-31T00:00:00",
                "2024-01-31T00:00:00"
            ]
        ),
        (
            "month",
            "2023-11-01T00:00:00", 
            "2024-01-02T00:00:00",
            [
                "2023-11-30T00:00:00",
                "2023-12-31T00:00:00",
                "2024-01-31T00:00:00"
            ]
        ),
        (
            "month",
            "2023-10-31T00:00:00", 
            "2023-12-02T00:00:00",
            [
                "2023-10-31T00:00:00",
                "2023-11-30T00:00:00",
                "2023-12-31T00:00:00"
            ]
        ),
        (
            "month",
            "2023-11-30T00:00:00", 
            "2023-11-30T23:59:59",
            [
                "2023-11-30T00:00:00",
            ]
        ),
        (
            "month",
            "2023-02-15T00:00:00", 
            "2023-04-30T23:59:59",
            [
                # empty data in this period
            ]
        ),
        # yearly granularity
        (
            "year",
            "2023-01-01T00:00:00", 
            "2025-01-01T00:00:00",
            [
                "2023-12-31T00:00:00",
                "2024-12-31T00:00:00",
                "2025-12-31T00:00:00"
            ]
        ),
        (
            "year",
            "2023-12-31T23:59:59", 
            "2024-01-01T00:00:00",
            [
                "2023-12-31T00:00:00",
                "2024-12-31T00:00:00",
            ]
        ),
    ])
    def test_speed_statistics_data_points_arrangement(self, period, date_from, date_to, expected_dates):
        """
        Tests transaction speed statistics returned data contract for different time granularities.
        
        Given: Transactions for different time periods
        When: Requesting speed statistics with different granularities (5min, hourly, daily, weekly, monthly, yearly)
        Then: Returns correct number of intervals with proper data keys and records with all the fields according to the contract
        """
        response = self.make_request(
            period,
            date_from,
            date_to
        )
        resp_data = response.json()
        
        expected_dates = [datetime.fromisoformat(date) for date in expected_dates]
        response_dates = [datetime.fromisoformat(date_keypoint['date']) for date_keypoint in resp_data]
        
        assert len(resp_data) == len(expected_dates)
        assert response_dates == expected_dates
        
        number_of_data_points = len(resp_data)
        
        # returns the number of models in the first data point or 0 if the data is empty
        number_of_models = len(resp_data[0]['records']) if resp_data else 0
                
        #goes for all records in all data points, 
        for i in range(number_of_models):
            for j in range(number_of_data_points):
                # check if records contain the keys as expected
                assert all(key in resp_data[j]['records'][i] for key in ['provider', 'model', 'mean_latency', 'tokens_per_second', 'total_transactions'])


        # cross checks if all the providers and models are the same in all data points, use transition property if data_point_0 == data_point_1 and data_point_1 == data_point_2 then data_point_0 == data_point_2
        for j in range(1, number_of_data_points):
            for i in range(number_of_models):
                assert resp_data[j-1]['records'][i]['provider'] == resp_data[j]['records'][i]['provider']
                assert resp_data[j-1]['records'][i]['model'] == resp_data[j]['records'][i]['model']


class TestMinutesGranularity(TestBaseTransactionSpeed):
    """Tests for 5-minute granularity transaction speed statistics.""" 
    
    def test_0min_duration_with_5min_granularity_same_date(self):
        """
        Tests transaction speed statistics for a 0-minute time frame.

        Given: A time period with zero duration (2023-11-01 12:00-12:00)
        When: Requesting speed statistics with 5-minute granularity
        Then: Returns empty list
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:00:00"
        )
        
        self.assert_response(response, 0, [])

    def test_5min_duration_with_5min_granularity_returns_single_interval(self):
        """
        Tests transaction speed statistics for a 5-minute time frame.

        Given: Transactions spanning 5 minutes (2023-11-01 12:00-12:05)
        When: Requesting speed statistics with 5-minute granularity
        Then: Returns one interval with tokens per second for each model
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:04:59"
        )
        
        resp_data = response.json()
        
        
        
        validation = [tuple([31.77272037])]
        self.assert_response(response, 1, validation)

    def test_5min_duration_with_5min_granularity_plus_one_hour_time_zone_returns_same_result(self):
        """
        Tests transaction speed statistics for a 5-minute time frame check if we get the same result if the dates are in different time zones. UTC is the default time zone.

        Given: Transactions spanning 5 minutes (2023-11-01 12:00-12:05)
        When: Requesting speed statistics with 5-minute granularity in UTC and CET
        Then: Returns the same interval with tokens per second for each model in both time zones
        """
        response_utc_0 = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00+00:00",
            "2023-11-01T12:04:59+00:00"
        )
        
        response_utc_1 = self.make_request(
            "5minutes",
            "2023-11-01T13:00:00+01:00",
            "2023-11-01T13:04:59+01:00"
        )
        
        resp_data_utc_0 = response_utc_0.json()
        resp_data_utc_1 = response_utc_1.json()
        
        assert resp_data_utc_0 == resp_data_utc_1
        
        validation = [tuple([31.77272037])]
        self.assert_response(response_utc_0, 1, validation)   
    
    def test_5min_duration_with_5min_granularity_plus_one_minushour_time_zone_returns_same_result(self):
        """
        Tests transaction speed statistics for a 5-minute time frame check if we get the same result if the dates are in different time zones. UTC is the default time zone.

        Given: Transactions spanning 5 minutes (2023-11-01 12:00-12:05)
        When: Requesting speed statistics with 5-minute granularity in UTC and CET
        Then: Returns the same interval with tokens per second for each model in both time zones
        """
        response_utc_0 = self.make_request(
            "5minutes",
            "2023-11-01T11:00:00-01:00",
            "2023-11-01T11:04:59-01:00"
        )
        
        response_utc_1 = self.make_request(
            "5minutes",
            "2023-11-01T13:00:00+01:00",
            "2023-11-01T13:04:59+01:00"
        )
        
        resp_data_utc_0 = response_utc_0.json()
        resp_data_utc_1 = response_utc_1.json()
        
        assert resp_data_utc_0 == resp_data_utc_1
        
        validation = [tuple([31.77272037])]
        self.assert_response(response_utc_0, 1, validation)           


    def test_30min_duration_with_5min_granularity_returns_six_intervals(self):
        """
        Tests transaction speed statistics for a 30-minute time frame.

        Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
        When: Requesting speed statistics with 5-minute granularity
        Then: Returns six intervals with tokens per second for each model
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:29:59"
        )
        
        validation = [
            tuple([0, 31.77272037, 0, 0]),
            tuple([0, 2.94217308, 7.700000136, 16.00000129]),
            tuple([0, 0, 0, 0]),
            tuple([65.13026753, 0, 0, 0]),
            tuple([0, 0, 82.41802468, 0]),
            tuple([92.09210559, 89.41178679, 0, 20.00000035]),
        ]
        self.assert_response(response, 6, validation)

    def test_1hour_duration_with_5min_granularity_returns_twelve_intervals(self):
        """
        Tests transaction speed statistics for a 1-hour time frame.

        Given: Transactions spanning one hour (2023-11-01 12:00-13:00)
        When: Requesting speed statistics with 5-minute granularity
        Then: Returns twelve intervals with tokens per second for each model
        """
        response = self.make_request(
            "5minutes",
            "2023-11-01T12:00:00",
            "2023-11-01T12:59:59"
        )
        
        validation = [
            tuple([0, 31.77272037, 0, 0]),
            tuple([0, 2.94217308, 7.700000136, 16.00000129]),
            tuple([0, 0, 0, 0]),
            tuple([65.13026753, 0, 0, 0]),
            tuple([0, 0, 82.41802468, 0]),
            tuple([92.09210559, 89.41178679, 0, 20.00000035]),
            tuple([0, 0, 0, 0]),
            tuple([0, 98.46880746, 0, 0]),
            tuple([0, 67.43749926, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 38.45918092, 0, 0]),
            tuple([0, 0, 80.65413879, 55.3845944]),
        ]
        self.assert_response(response, 12, validation)

    def test_1month_duration_with_5min_granularity_returns_empty_list(self):
        """
        Tests transaction speed statistics for a period with no data.

        Given: A time period with no recorded transactions (October 2023)
        When: Requesting speed statistics with 5-minute granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "5minutes",
            "2023-10-01T12:00:00",
            "2023-10-31T12:30:00"
        )
        
        self.assert_response(response, 0, [])


class TestHourlyGranularity(TestBaseTransactionSpeed):
    """Tests for hourly granularity transaction speed statistics."""

    def test_30min_duration_with_hourly_granularity_returns_single_interval(self):
        """
        Tests transaction speed statistics for a 30-minute time frame.

        Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
        When: Requesting speed statistics with hourly granularity
        Then: Returns one interval with tokens per second for each model
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00",
            "2023-11-01T12:30:00"
        )
        
        validation = [tuple([78.61118656, 38.97485015, 57.5120165, 18.00000082])]
        self.assert_response(response, 1, validation)

    def test_1hour_duration_with_hourly_granularity_returns_two_intervals(self):
        """
        Tests transaction speed statistics for a 1-hour time frame.

        Given: Transactions spanning one hour (2023-11-01 12:00-13:00)
        When: Requesting speed statistics with hourly granularity
        Then: Returns two intervals with tokens per second for each model
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00",
            "2023-11-01T13:00:00"
        )
        
        validation = [
            tuple([78.61118656, 48.46159236, 69.08307764, 30.46153202]),
            tuple([0, 0, 0, 0]),
        ]
        self.assert_response(response, 2, validation)

    def test_24hour_duration_with_hourly_granularity_returns_24_intervals(self):
        """
        Tests transaction speed statistics for a 24-hour time frame.

        Given: Transactions spanning 24 hours (2023-11-01 12:00 to 2023-11-02 12:00)
        When: Requesting speed statistics with hourly granularity
        Then: Returns 24 intervals with tokens per second for each model
        """
        response = self.make_request(
            "hour",
            "2023-11-01T12:00:00",
            "2023-11-02T11:59:59"
        )
        
        validation = [
            tuple([78.61118656, 48.46159236, 69.08307764, 30.46153202]),
            tuple([0, 4.124278, 0, 0]),
            tuple([0, 41.66667439, 0, 0]),
            tuple([97.51860847, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([52.25000421, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([53.2270015, 23.00000908, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 5.988021267, 44.1666656]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([31.50684656, 0, 47.52925421, 0]),
            tuple([0, 0, 0, 0]),
            tuple([57.48084108, 0, 0, 0]),
            tuple([0, 0, 32.00001264, 0]),
        ]
        self.assert_response(response, 24, validation)

    def test_1month_duration_with_hourly_granularity_returns_empty_list(self):
        """
        Tests transaction speed statistics for a period with no data.

        Given: A time period with no recorded transactions (October 2023)
        When: Requesting speed statistics with hourly granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "hour",
            "2023-10-01T12:00:00",
            "2023-10-31T18:00:00"
        )
        
        self.assert_response(response, 0, [])
        
    def test_1day_duration_with_daily_granularity_returns_two_intervals(self):
        """
        Tests transaction speed statistics for a 1-day time frame.

        Given: Transactions spanning one day (2023-11-01 13:00 to 2023-11-02 13:00)
        When: Requesting speed statistics with daily granularity
        Then: Returns two intervals with tokens per second for each model
        """
        response = self.make_request(
            "day",
            "2023-11-01T13:00:00",
            "2023-11-02T13:00:00"
        )
        
        validation = [
            tuple([67.66520472, 22.93032058, 0, 0]),
            tuple([54.33745498, 0, 36.11515931, 44.1666656]),
        ]
        self.assert_response(response, 2, validation)

    def test_1month_duration_with_daily_granularity_returns_30_intervals(self):
        """
        Tests transaction speed statistics for a 1-month time frame.

        Given: Transactions spanning one month (2023-11-01 12:00 to 2023-11-30 12:00)
        When: Requesting speed statistics with daily granularity
        Then: Returns 30 intervals with tokens per second for each model
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00",
            "2023-11-30T12:00:00"
        )
        
        validation = [
            tuple([72.04359746, 43.355338, 69.08307764, 30.46153202]),
            tuple([49.37809126, 0, 36.11515931, 44.1666656]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([23.46938859, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 73.48172621]),
            tuple([0, 0, 86.68341626, 5.546371285]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 30.14705791, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 30.77519425, 0, 0]),
            tuple([0, 79.79794645, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 14.50000117]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 83.11703415]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 73.73913033, 0]),
        ]
        self.assert_response(response, 30, validation)

    def test_1day_duration_with_daily_granularity_returns_empty_list(self):
        """
        Tests transaction speed statistics for a period with no data.

        Given: A time period with no recorded transactions (2023-11-03 12:00 to 2023-11-04 12:00)
        When: Requesting speed statistics with daily granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "day",
            "2023-11-03T12:00:00",
            "2023-11-04T12:00:00"
        )
        
        self.assert_response(response, 0, [])

class TestDailyGranularity(TestBaseTransactionSpeed):
    """Tests for daily granularity transaction speed statistics."""

    def test_6hour_duration_with_daily_granularity_returns_single_interval(self):
        """
        Tests transaction speed statistics for a 6-hour time frame.

        Given: Transactions spanning 6 hours (2023-11-01 12:00-18:00)
        When: Requesting speed statistics with daily granularity
        Then: Returns one interval with tokens per second for each model
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00",
            "2023-11-01T18:00:00"
        )
        
        validation = [tuple([76.74774645, 44.80929007, 69.08307764, 30.46153202])]
        self.assert_response(response, 1, validation)

    def test_24hour_duration_with_daily_granularity_returns_single_interval(self):
        """
        Tests transaction speed statistics for a 24-hour time frame.

        Given: Transactions spanning 24 hours (2023-11-01 00:00-23:59)
        When: Requesting speed statistics with daily granularity
        Then: Returns one interval with tokens per second for each model
        """
        response = self.make_request(
            "day",
            "2023-11-01T00:00:00",
            "2023-11-01T23:59:59"
        )
        
        resp_data = response.json()
        
        response_date = datetime.fromisoformat(resp_data[0]['date'])
        expected_date = datetime.fromisoformat("2023-11-01T00:00:00")
        assert response_date == expected_date
        
        validation = [tuple([72.04359746, 43.355338, 69.08307764, 30.46153202])]
        self.assert_response(response, 1, validation)

    def test_7day_duration_with_daily_granularity_returns_seven_intervals(self):
        """
        Tests transaction speed statistics for a 7-day time frame.

        Given: Transactions spanning 7 days (2023-11-01 to 2023-11-07)
        When: Requesting speed statistics with daily granularity
        Then: Returns seven intervals with tokens per second for each model
        """
        response = self.make_request(
            "day",
            "2023-11-01T12:00:00",
            "2023-11-07T11:59:59"
        )
        
        validation = [
            tuple([72.04359746, 43.355338, 69.08307764, 30.46153202]),
            tuple([49.37809126, 0, 36.11515931, 44.1666656]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([23.46938859, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
        ]
        self.assert_response(response, 7, validation)
        
    def test_1month_duration_with_daily_granularity_returns_empty_list(self):
        """
        Tests transaction speed statistics for a period with no data.

        Given: A time period with no recorded transactions (2024-05-01 to 2024-06-01)
        When: Requesting speed statistics with daily granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "day",
            "2024-05-01",
            "2024-06-01"
        )
        
        self.assert_response(response, 0, [])


class TestWeeklyGranularity(TestBaseTransactionSpeed):
    """Tests for weekly granularity transaction speed statistics."""

    def test_3day_duration_with_weekly_granularity_returns_single_interval(self):
        """
        Tests transaction speed statistics for a 3-day time frame.

        Given: Transactions spanning 3 days (2023-11-01 to 2023-11-03)
        When: Requesting speed statistics with weekly granularity
        Then: Returns one interval with tokens per second for each model
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00",
            "2023-11-03T12:00:00"
        )
        
        validation = [tuple([61.97003915, 43.355338, 54.09766022, 33.88781541])]
        self.assert_response(response, 1, validation)

    def test_7day_duration_with_weekly_granularity_returns_two_intervals(self):
        """
        Tests transaction speed statistics for a 7-day time frame.

        Given: Transactions spanning 7 days (2023-11-01 to 2023-11-07)
        When: Requesting speed statistics with weekly granularity
        Then: Returns two intervals with tokens per second for each model
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00",
            "2023-11-07T12:00:00"
        )
        
        validation = [
            tuple([58.11997409, 43.355338, 54.09766022, 33.88781541]),
            tuple([0, 0, 0, 0]),
        ]
        self.assert_response(response, 2, validation)

    def test_2month_duration_with_weekly_granularity_returns_nine_intervals(self):
        """
        Tests transaction speed statistics for a 2-month time frame.

        Given: Transactions spanning 2 months (2023-11-01 to 2023-12-31)
        When: Requesting speed statistics with weekly granularity
        Then: Returns nine intervals with tokens per second for each model
        """
        response = self.make_request(
            "week",
            "2023-11-01T12:00:00",
            "2023-12-31T00:00:00"
        )
        
        validation = [
            tuple([58.11997409, 43.355338, 54.09766022, 33.88781541]),
            tuple([0, 0, 86.68341626, 50.8366079]),
            tuple([0, 55.28657035, 30.14705791, 0]),
            tuple([0, 0, 0, 14.50000117]),
            tuple([0, 0, 49.86956757, 57.39410621]),
            tuple([54.36081291, 45.90951084, 0, 0]),
            tuple([11.46285769, 72.06896586, 0, 0]),
            tuple([0, 0, 0, 0]),
            tuple([0, 0, 0, 0]),
        ]
        self.assert_response(response, 9, validation)
        
    def test_2week_duration_with_weekly_granularity_returns_empty_list(self):
        """
        Tests transaction speed statistics for a period with no data.

        Given: A time period with no recorded transactions (2024-03-29 to 2024-04-12)
        When: Requesting speed statistics with weekly granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "week",
            "2024-03-29T00:00:00",
            "2024-04-12T00:00:00"
        )
        
        self.assert_response(response, 0, [])


class TestMonthlyGranularity(TestBaseTransactionSpeed):
    """Tests for monthly granularity transaction speed statistics."""

    def test_7day_duration_with_monthly_granularity_returns_single_interval(self):
        """
        Tests transaction speed statistics for a 7-day time frame.

        Given: Transactions spanning 7 days (2023-11-01 to 2023-11-07)
        When: Requesting speed statistics with monthly granularity
        Then: Returns one interval with tokens per second for each model
        """
        response = self.make_request(
            "month",
            "2023-11-01T12:00:00",
            "2023-11-07T12:00:00"
        )
        
        validation = [tuple([58.119971, 43.355338, 54.09766022, 33.88781541])]
        self.assert_response(response, 1, validation)
  

    def test_1month_duration_with_monthly_granularity_returns_single_interval(self):
        """
        Tests transaction speed statistics for a 1-month time frame.

        Given: Transactions spanning one month (2023-11-01 to 2023-11-30)
        When: Requesting speed statistics with monthly granularity
        Then: Returns one interval with tokens per second for each model
        """
        response = self.make_request(
            "month",
            "2023-11-01",
            "2023-11-30T23:59:59"
        )
        
        validation = [tuple([58.11997409, 44.75901239, 56.11741906, 42.85312452])]
        self.assert_response(response, 1, validation)

    def test_1month_duration_with_monthly_granularity_returns_empty_list(self):
        """
        Tests transaction speed statistics for a period with no data.

        Given: A time period with no recorded transactions (2024-05-01 to 2024-06-01)
        When: Requesting speed statistics with monthly granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "month",
            "2024-05-01",
            "2024-06-01"
        )
        
        self.assert_response(response, 0, [])


    
    def test_6month_duration_with_monthly_granularity_returns_six_intervals(self):
        """
        Tests transaction speed statistics for a 6-month time frame.

        Given: Transactions spanning 6 months (2023-10-01 to 2024-03-31)
        When: Requesting speed statistics with monthly granularity
        Then: Returns six intervals with tokens per second for each model
        """
        response = self.make_request(
            "month",
            "2023-10-01",
            "2024-03-31"
        )
        validation = [
            tuple([0, 0, 0, 0]),
            tuple([58.11997409, 44.75901239, 56.11741906, 42.85312452]),
            tuple([32.9118353, 55.815765, 26.00000482, 44.53264224]),
            tuple([38.85257592, 11.75, 17.26086978, 69.94543473]),
            tuple([0, 0, 0, 0]),
            tuple([55.78817778, 0, 0, 60.88811508]),
        ]
        self.assert_response(response, 6, validation)


class TestYearlyGranularity(TestBaseTransactionSpeed):
    """Tests for yearly granularity transaction speed statistics."""

    def test_2month_duration_with_yearly_granularity_returns_single_interval(self):
        """
        Tests transaction speed statistics for a 2-month time frame.

        Given: Transactions spanning 2 months (2023-11-01 to 2023-12-31)
        When: Requesting speed statistics with yearly granularity
        Then: Returns one interval with tokens per second for each model
        """
        response = self.make_request(
            "year",
            "2023-11-01",
            "2023-12-31T23:59:59"
        )
        
        resp_data = response.json()
        
        expected_date = datetime.fromisoformat("2023-12-31T00:00:00")
        response_date = datetime.fromisoformat(resp_data[0]['date'])
        
        assert len(resp_data) == 1
        assert response_date == expected_date
        assert len(resp_data[0]['records']) == 4
        
        records = resp_data[0]['records']
        
        #provider Anthropic claude-2.0
        assert records[0]['provider'] == 'Anthropic'
        assert records[0]['model'] == 'claude-2.0'
        assert records[0]['mean_latency'] == pytest.approx(10.32475, rel=1e-3)
        assert records[0]['tokens_per_second'] == pytest.approx(53.91861763, rel=1e-3)
        assert records[0]['total_transactions'] == 12
        
        #provider Azure OpenAI gpt-35-turbo-0613
        assert records[1]['provider'] == 'Azure OpenAI'
        assert records[1]['model'] == 'gpt-35-turbo-0613'
        assert records[1]['mean_latency'] == pytest.approx(14.68428, rel=1e-3)
        assert records[1]['tokens_per_second'] == pytest.approx(44.82339021, rel=1e-3)
        assert records[1]['total_transactions'] == 21
        
        #provider OpenAI babbage-002
        assert records[2]['provider'] == 'OpenAI'
        assert records[2]['model'] == 'babbage-002'
        assert records[2]['mean_latency'] == pytest.approx(10.8833333, rel=1e-3)
        assert records[2]['tokens_per_second'] == pytest.approx(54.10959145, rel=1e-3)
        assert records[2]['total_transactions'] == 15
        
        #provider OpenAI gpt-4-0613
        assert records[3]['provider'] == 'OpenAI'
        assert records[3]['model'] == 'gpt-4-0613'
        assert records[3]['mean_latency'] == pytest.approx(47.21509, rel=1e-3)
        assert records[3]['tokens_per_second'] == pytest.approx(43.15849138, rel=1e-3)
        assert records[3]['total_transactions'] == 11
                

    def test_5month_duration_with_yearly_granularity_returns_two_intervals(self):
        """
        Tests transaction speed statistics for a 5-month time frame.

        Given: Transactions spanning from 2023 to 2024 (2023-11-01 to 2024-03-31)
        When: Requesting speed statistics with yearly granularity
        Then: Returns two intervals with tokens per second for each model
        """
        response = self.make_request(
            "year",
            "2023-11-01",
            "2024-03-31"
        )
        
        validation = [
            tuple([53.91861763, 47.27191158, 54.10959145, 43.15849138]),
            tuple([48.5300627, 11.75, 17.26086978, 63.15244499]),
        ]
        self.assert_response(response, 2, validation)

    def test_6month_duration_with_yearly_granularity_returns_empty_list(self):
        """
        Tests transaction speed statistics for a period with no data.

        Given: A time period with no recorded transactions (2024-05-31 to 2024-12-31)
        When: Requesting speed statistics with yearly granularity
        Then: Returns an empty list
        """
        response = self.make_request(
            "year",
            "2024-05-31",
            "2024-12-31"
        )
        
        self.assert_response(response, 0, [])
        
    def test_5month_duration_with_yearly_granularity_returns_two_intervals(self):
        """
        Tests transaction speed statistics for a 5-month time frame with yearly granularity.

        Given: Transactions spanning from 2023 to 2024 (2023-11-01 to 2024-03-31)
        When: Requesting transaction speed statistics with yearly granularity
        Then: Returns two intervals with tokens per second for each model
        """
        response = self.make_request(
            "year",
            "2023-11-01",
            "2024-03-31"
        )  
        
        validation = [
            tuple([53.91861763, 47.27191158, 54.10959145, 43.15849138]),
            tuple([48.5300627, 11.75, 17.26086978, 63.15244499]),
        ]
        self.assert_response(response, 2, validation)
        
    

    