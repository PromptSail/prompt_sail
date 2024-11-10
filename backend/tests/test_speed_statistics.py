from test_utils import read_transactions_from_csv, truncate_float

header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
}

# check speed statistics basic functionality, error handling, parameters checks etc.

def test_speed_statistics_for_not_existing_project(client, application):
    """
    Tests transaction speed statistics for a 5-minute time frame with 5-minute granularity for not existing project.

    Given: Transactions spanning 5 minutes (2023-11-01 12:00-12:05)
    When: Requesting transaction speed statistics with 5-minute granularity
    Then: Returns error
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-that-not-exists-xxx&period=5minutes&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:04:59",
        headers=header,
    )
    

    # assert
    response_data = response.json()
    
    assert response.status_code == 404
    assert response_data == {"error": "Project not found"}


def test_speed_statistics_for_not_wrong_period(client, application):
    """
    Tests transaction speed statistics for a not supported period.

    Given: Transactions spanning 5 minutes (2023-11-01 12:00-12:05)
    When: Requesting transaction speed statistics with non-existing period
    Then: Returns error
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=not-existing-period&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:04:59",
        headers=header,
    )
    

    # assert
    response_data = response.json()
    assert response.status_code == 422
    assert response_data['detail'][0]['input'] == 'not-existing-period'



def test_speed_statistics_for_date_from_after_date_to(client, application):
    """
    Tests transaction speed statistics for a time frame when date_from is after date_to.

    Given: Transactions spanning -10 minutes (2023-11-01 12:10-12:00) date_from is after date_to
    When: Requesting transaction speed statistics
    Then: Returns error
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=5minutes&date_from=2023-11-01T12:10:00&date_to=2023-11-01T12:00:00",
        headers=header,
    )
        
    # assert
    response_data = response.json()
    assert response.status_code == 400
    assert response_data['detail'] == "date_from is after date_to"

# check speed statistics for different periods and time frames

def test_5min_duration_with_5min_granularity_returns_single_interval(client, application):
    """
    Tests transaction speed statistics for a 5-minute time frame with 5-minute granularity.

    Given: Transactions spanning 5 minutes (2023-11-01 12:00-12:05)
    When: Requesting transaction speed statistics with 5-minute granularity
    Then: Returns one interval with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:04:59",
        headers=header,
    )
    temp = list(
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
    validation = [tuple([31.77272037])]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert temp == validation
    
    


def test_0min_duration_with_5min_granularity_same_date(client, application):
    """
    Tests transaction speed statistics for a 0-minute time frame with 5-minute granularity with the same date.

    Given: Transactions spanning 0 minutes (2023-11-01 12:00-12:00)
    When: Requesting transaction speed statistics with 5-minute granularity
    Then: Returns empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:00:00",
        headers=header,
    )
    
    response_data = response.json()
    
    # assert
    assert response.status_code == 200
    assert len(response_data) == 0





def test_30min_duration_with_5min_granularity_returns_six_intervals(client, application):
    """
    Tests transaction speed statistics for a 30-minute time frame with 5-minute granularity.

    Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
    When: Requesting transaction speed statistics with 5-minute granularity
    Then: Returns six intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:29:59",
        headers=header,
    )
    temp = list(
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
    validation = [
        tuple([0, 31.77272037, 0, 0]),
        tuple([0, 2.94217308, 7.700000136, 16.00000129]),
        tuple([0, 0, 0, 0]),
        tuple([65.13026753, 0, 0, 0]),
        tuple([0, 0, 82.41802468, 0]),
        tuple([92.09210559, 89.41178679, 0, 20.00000035]),
    ]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 6
    assert temp == validation


def test_1hour_duration_with_5min_granularity_returns_twelve_intervals(client, application):
    """
    Tests transaction speed statistics for a 1-hour time frame with 5-minute granularity.

    Given: Transactions spanning one hour (2023-11-01 12:00-13:00)
    When: Requesting transaction speed statistics with 5-minute granularity
    Then: Returns twelve intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:59:59",
        headers=header,
    )
    temp = list(
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
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 12
    assert temp == validation


def test_1month_duration_with_5min_granularity_returns_empty_list(client, application):
    """
    Tests transaction speed statistics for a period with no data with 5-minute granularity.

    Given: A time period with no recorded transactions (2023-10-01 to 2023-10-31)
    When: Requesting transaction speed statistics with 5-minute granularity
    Then: Returns an empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=5minutes&date_from=2023-10-01T12:00:00&date_to=2023-10-31T12:30:00",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_30min_duration_with_hourly_granularity_returns_single_interval(client, application):
    """
    Tests transaction speed statistics for a 30-minute time frame with hourly granularity.

    Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
    When: Requesting transaction speed statistics with hourly granularity
    Then: Returns one interval with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:30:00",
        headers=header,
    )
    temp = list(
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
    validation = [tuple([78.61118656, 38.97485015, 57.5120165, 18.00000082])]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert temp == validation


def test_1hour_duration_with_hourly_granularity_returns_two_intervals(client, application):
    """
    Tests transaction speed statistics for a 1-hour time frame with hourly granularity.

    Given: Transactions spanning one hour (2023-11-01 12:00-13:00)
    When: Requesting transaction speed statistics with hourly granularity
    Then: Returns two intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00&date_to=2023-11-01T13:00:00",
        headers=header,
    )
    temp = list(
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
    validation = [
        tuple([78.61118656, 48.46159236, 69.08307764, 30.46153202]),
        tuple([0, 0, 0, 0]),
    ]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert temp == validation


def test_24hour_duration_with_hourly_granularity_returns_24_intervals(client, application):
    """
    Tests transaction speed statistics for a 24-hour time frame with hourly granularity.

    Given: Transactions spanning 24 hours (2023-11-01 12:00 to 2023-11-02 12:00)
    When: Requesting transaction speed statistics with hourly granularity
    Then: Returns 24 intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00&date_to=2023-11-02T11:59:59",
        headers=header,
    )
    temp = list(
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
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 24
    assert temp == validation


def test_1month_duration_with_hourly_granularity_returns_empty_list(client, application):
    """
    Tests transaction speed statistics for a period with no data with hourly granularity.

    Given: A time period with no recorded transactions (2023-10-01 to 2023-10-31)
    When: Requesting transaction speed statistics with hourly granularity
    Then: Returns an empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=hour&date_from=2023-10-01T12:00:00&date_to=2023-10-31T18:00:00",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_6hour_duration_with_daily_granularity_returns_single_interval(client, application):
    """
    Tests transaction speed statistics for a 6-hour time frame with daily granularity.

    Given: Transactions spanning 6 hours (2023-11-01 12:00-18:00)
    When: Requesting transaction speed statistics with daily granularity
    Then: Returns one interval with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=day&date_from=2023-11-01T12:00:00&date_to=2023-11-01T18:00:00",
        headers=header,
    )
    temp = list(
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
    validation = [tuple([76.74774645, 44.80929007, 69.08307764, 30.46153202])]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert temp == validation


def test_24hour_duration_with_daily_granularity_returns_single_interval(client, application):
    """
    Tests transaction speed statistics for a 24-hour time frame with daily granularity.

    Given: Transactions spanning 24 hours (2023-11-01 00:00-23:59)
    When: Requesting transaction speed statistics with daily granularity
    Then: Returns one interval with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=day&date_from=2023-11-01&date_to=2023-11-01",
        headers=header,
    )
    temp = list(
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
    validation = [tuple([72.04359746, 43.355338, 69.08307764, 30.46153202])]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert temp == validation


def test_1day_duration_with_daily_granularity_returns_two_intervals(client, application):
    """
    Tests transaction speed statistics for a 1-day time frame with daily granularity.

    Given: Transactions spanning one day (2023-11-01 13:00 to 2023-11-02 13:00)
    When: Requesting transaction speed statistics with daily granularity
    Then: Returns two intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=day&date_from=2023-11-01T13:00:00&date_to=2023-11-02T13:00:00",
        headers=header,
    )
    temp = list(
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
    validation = [
        tuple([67.66520472, 22.93032058, 0, 0]),
        tuple([54.33745498, 0, 36.11515931, 44.1666656]),
    ]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert temp == validation


def test_7day_duration_with_daily_granularity_returns_seven_intervals(client, application):
    """
    Tests transaction speed statistics for a 7-day time frame with daily granularity.

    Given: Transactions spanning 7 days (2023-11-01 12:00 to 2023-11-07 12:00)
    When: Requesting transaction speed statistics with daily granularity
    Then: Returns seven intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=day&date_from=2023-11-01T12:00:00&date_to=2023-11-07T11:59:59",
        headers=header,
    )
    temp = list(
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
    validation = [
        tuple([72.04359746, 43.355338, 69.08307764, 30.46153202]),
        tuple([49.37809126, 0, 36.11515931, 44.1666656]),
        tuple([0, 0, 0, 0]),
        tuple([0, 0, 0, 0]),
        tuple([0, 0, 0, 0]),
        tuple([23.46938859, 0, 0, 0]),
        tuple([0, 0, 0, 0]),
    ]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 7
    assert temp == validation


def test_1month_duration_with_daily_granularity_returns_30_intervals(client, application):
    """
    Tests transaction speed statistics for a 1-month time frame with daily granularity.

    Given: Transactions spanning one month (2023-11-01 12:00 to 2023-11-30 12:00)
    When: Requesting transaction speed statistics with daily granularity
    Then: Returns 30 intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=day&date_from=2023-11-01T12:00:00&date_to=2023-11-30T12:00:00",
        headers=header,
    )
    temp = list(
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
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 30
    assert temp == validation


def test_1day_duration_with_daily_granularity_returns_empty_list(client, application):
    """
    Tests transaction speed statistics for a period with no data with daily granularity.

    Given: A time period with no recorded transactions (2023-11-03 12:00 to 2023-11-04 12:00)
    When: Requesting transaction speed statistics with daily granularity
    Then: Returns an empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=day&date_from=2023-11-03T12:00:00&date_to=2023-11-04T12:00:00",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_3day_duration_with_weekly_granularity_returns_single_interval(client, application):
    """
    Tests transaction speed statistics for a 3-day time frame with weekly granularity.

    Given: Transactions spanning 3 days (2023-11-01 12:00 to 2023-11-03 12:00)
    When: Requesting transaction speed statistics with weekly granularity
    Then: Returns one interval with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=week&date_from=2023-11-01T12:00:00&date_to=2023-11-03T12:00:00",
        headers=header,
    )
    temp = list(
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
    validation = [tuple([61.97003915, 43.355338, 54.09766022, 33.88781541])]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert temp == validation


def test_7day_duration_with_weekly_granularity_returns_two_intervals(client, application):
    """
    Tests transaction speed statistics for a 7-day time frame with weekly granularity.

    Given: Transactions spanning 7 days (2023-11-01 12:00 to 2023-11-07 12:00)
    When: Requesting transaction speed statistics with weekly granularity
    Then: Returns two intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=week&date_from=2023-11-01T12:00:00&date_to=2023-11-07T12:00:00",
        headers=header,
    )
    temp = list(
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
    validation = [
        tuple([58.11997409, 43.355338, 54.09766022, 33.88781541]),
        tuple([0, 0, 0, 0]),
    ]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert temp == validation


def test_2month_duration_with_weekly_granularity_returns_nine_intervals(client, application):
    """
    Tests transaction speed statistics for a 2-month time frame with weekly granularity.

    Given: Transactions spanning 2 months (2023-11-01 12:00 to 2023-12-31 00:00)
    When: Requesting transaction speed statistics with weekly granularity
    Then: Returns nine intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=week&date_from=2023-11-01T12:00:00&date_to=2023-12-31T00:00:00",
        headers=header,
    )
    temp = list(
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
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 9
    assert temp == validation


def test_2week_duration_with_weekly_granularity_returns_empty_list(client, application):
    """
    Tests transaction speed statistics for a period with no data with weekly granularity.

    Given: A time period with no recorded transactions (2024-03-29 00:00 to 2024-04-12 00:00)
    When: Requesting transaction speed statistics with weekly granularity
    Then: Returns an empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=week&date_from=2024-03-29T00:00:00&date_to=2024-04-12T00:00:00",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_7day_duration_with_monthly_granularity_returns_single_interval(client, application):
    """
    Tests transaction speed statistics for a 7-day time frame with monthly granularity.

    Given: Transactions spanning 7 days (2023-11-01 12:00 to 2023-11-07 12:00)
    When: Requesting transaction speed statistics with monthly granularity
    Then: Returns one interval with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=month&date_from=2023-11-01T12:00:00&date_to=2023-11-07T12:00:00",
        headers=header,
    )
    temp = list(
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
    validation = [tuple([58.119971, 43.355338, 54.09766022, 33.88781541])]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert temp == validation


def test_1month_duration_with_monthly_granularity_returns_single_interval(client, application):
    """
    Tests transaction speed statistics for a 1-month time frame with monthly granularity.

    Given: Transactions spanning one month (2023-11-01 to 2023-11-30)
    When: Requesting transaction speed statistics with monthly granularity
    Then: Returns one interval with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=month&date_from=2023-11-01&date_to=2023-11-30",
        headers=header,
    )
    temp = list(
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
    validation = [tuple([58.11997409, 44.75901239, 56.11741906, 42.85312452])]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert temp == validation


def test_6month_duration_with_monthly_granularity_returns_six_intervals(client, application):
    """
    Tests transaction speed statistics for a 6-month time frame with monthly granularity.

    Given: Transactions spanning 6 months (2023-10-01 to 2024-03-31)
    When: Requesting transaction speed statistics with monthly granularity
    Then: Returns six intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=month&date_from=2023-10-01&date_to=2024-03-31",
        headers=header,
    )
    temp = list(
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
    validation = [
        tuple([0, 0, 0, 0]),
        tuple([58.11997409, 44.75901239, 56.11741906, 42.85312452]),
        tuple([32.9118353, 55.815765, 26.00000482, 44.53264224]),
        tuple([38.85257592, 11.75, 17.26086978, 69.94543473]),
        tuple([0, 0, 0, 0]),
        tuple([55.78817778, 0, 0, 60.88811508]),
    ]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 6
    assert temp == validation


def test_1month_duration_with_monthly_granularity_returns_empty_list(client, application):
    """
    Tests transaction speed statistics for a period with no data with monthly granularity.

    Given: A time period with no recorded transactions (2024-05-01 to 2024-06-01)
    When: Requesting transaction speed statistics with monthly granularity
    Then: Returns an empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=month&date_from=2024-05-01&date_to=2024-06-01",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_2month_duration_with_yearly_granularity_returns_single_interval(client, application):
    """
    Tests transaction speed statistics for a 2-month time frame with yearly granularity.

    Given: Transactions spanning 2 months (2023-11-01 to 2023-12-31)
    When: Requesting transaction speed statistics with yearly granularity
    Then: Returns one interval with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=year&date_from=2023-11-01&date_to=2023-12-31",
        headers=header,
    )
    temp = list(
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
    validation = [tuple([53.91861763, 44.82339021, 54.10959145, 43.15849138])]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert temp == validation


def test_2year_duration_with_yearly_granularity_returns_two_intervals(client, application):
    """
    Tests transaction speed statistics for a 2-year time frame with yearly granularity.

    Given: Transactions spanning from 2023 to 2024 (2023-11-01 to 2024-03-31)
    When: Requesting transaction speed statistics with yearly granularity
    Then: Returns two intervals with tokens per second for each model
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=year&date_from=2023-11-01&date_to=2024-03-31",
        headers=header,
    )
    temp = list(
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
    validation = [
        tuple([53.91861763, 47.27191158, 54.10959145, 43.15849138]),
        tuple([48.5300627, 11.75, 17.26086978, 63.15244499]),
    ]
    validation = list(
        [tuple(map(lambda x: truncate_float(x, 3), list(val))) for val in validation]
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert temp == validation


def test_6month_duration_with_yearly_granularity_returns_empty_list(client, application):
    """
    Tests transaction speed statistics for a period with no data with yearly granularity.

    Given: A time period with no recorded transactions (2024-05-31 to 2024-12-31)
    When: Requesting transaction speed statistics with yearly granularity
    Then: Returns an empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv(
            "test_transactions_tokens_cost_speed.csv"
        )
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_speed?project_id=project-test&period=year&date_from=2024-05-31&date_to=2024-12-31",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0
