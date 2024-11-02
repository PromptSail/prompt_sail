from test_utils import read_transactions_from_csv

header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
}


def test_5min_duration_with_5min_granularity_returns_correct_status_counts(client, application):
    """
    Tests transaction statistics for a 5-minute interval.

    Given: A set of transactions within 2023-11-01 12:00-12:05
    When: Requesting transaction counts with 5-minute granularity
    Then: Returns one interval with correct HTTP status code counts (200,300,400,500)
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00.000&date_to=2023-11-01T12:04:59.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(3, 1, 2, 0)]


def test_30min_duration_with_5min_granularity_returns_six_5min_intervals(client, application):
    """
    Tests transaction statistics for a 30-minute period with 5-minute granularity.

    Given: Transactions spanning 30 minutes (2023-11-01 12:00-12:30)
    When: Requesting transaction counts with 5-minute granularity
    Then: Returns 6 intervals with correct status counts per interval
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00.000&date_to=2023-11-01T12:29:59.999",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 6
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [
        (3, 1, 2, 0),
        (2, 0, 0, 0),
        (0, 0, 0, 0),
        (1, 0, 1, 0),
        (2, 1, 0, 0),
        (3, 0, 0, 2),
    ]


def test_1hour_duration_with_5min_granularity_returns_twelve_5min_intervals(client, application):
    """
    Tests transaction statistics for a 1-hour duration with 5-minute granularity.

    Given: Transactions spanning one hour (2023-11-01 12:00-13:00)
    When: Requesting transaction counts with 5-minute granularity
    Then: Returns 12 intervals with correct status counts per interval
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00.000&date_to=2023-11-01T12:59:59.999",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 12
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [
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
    ]


def test_1month_duration_with_5min_granularity_returns_empty_list(client, application):
    """
    Tests transaction statistics for a 1-month duration with 5-minute granularity.

    Given: A time period with no recorded transactions
    When: Requesting transaction counts for October 2023
    Then: Returns an empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=5minutes&date_from=2023-10-01T00:00.000&date_to=2023-10-31T00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_30min_duration_with_hourly_granularity_returns_single_interval(client, application):
    """
    Tests counting the transactions in a 30 minute duration with hourly granularity.

    Given: Transactions within 30 minutes (2023-11-01 12:00-12:30)
    When: Requesting transaction counts with hourly granularity
    Then: Returns one interval with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:30:00",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(11, 2, 3, 2)]


def test_1hour_duration_with_hourly_granularity_returns_two_intervals(client, application):
    """
    Tests counting the transactions in a 1-hour duration (from 12:00 to 13:00) with hourly granularity (period=hour).

    Given: Transactions spanning one hour
    When: Requesting hourly transaction counts
    Then: Returns two intervals with correct aggregated counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00.000&date_to=2023-11-01T13:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(23, 3, 7, 2), (0, 0, 0, 0)]


def test_24hour_duration_with_hourly_granularity_returns_24_intervals(client, application):
    """
    Tests counting the transactions in a 24-hour duration (from 12:00 to 12:00 the next day) with hourly granularity (period=hour).

    Given: Transactions spanning 24 hours
    When: Requesting hourly transaction counts
    Then: Returns 24 intervals with correct status counts per hour
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00.000&date_to=2023-11-02T11:59:59.999",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 24
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [
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
    ]


def test_1month_duration_with_hourly_granularity_returns_empty_list(client, application):
    """
    Tests counting the transactions in a 1-month duration (from 2023-10-01 to 2023-10-31) with hourly granularity (period=hour).

    Given: A month period without transactions (October 2023)
    When: Requesting hourly transaction counts
    Then: Returns empty list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=hour&date_from=2023-10-01T00:00.000&date_to=2023-10-31T00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_6hour_duration_with_daily_granularity_returns_single_interval(client, application):
    """
    Tests counting the transactions in a 6-hour duration (from 12:00 to 18:00) with daily granularity (period=day).

    Given: Transactions spanning 6 hours
    When: Requesting daily transaction counts
    Then: Returns one interval with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T12:00:00.000&date_to=2023-11-01T18:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(27, 4, 9, 2)]


def test_1day_duration_with_daily_granularity_returns_single_interval(client, application):
    """
    Tests counting the transactions in a 1-day duration (from 2023-11-01 to 2023-11-02) with daily granularity (period=day).

    Given: Transactions spanning 1 day
    When: Requesting daily transaction counts
    Then: Returns one interval with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T00:00.000&date_to=2023-11-01T00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(29, 4, 9, 2)]


def test_24hour_duration_with_daily_granularity_returns_two_intervals(client, application):
    """
    Tests counting the transactions in a 24-hour duration (from 2023-11-01 to 2023-11-02) with daily granularity (period=day).

    Given: Transactions spanning 2 days
    When: Requesting daily transaction counts
    Then: Returns two intervals with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T13:00:00.000&date_to=2023-11-02T13:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(6, 1, 2, 0), (9, 0, 0, 2)]


def test_7day_duration_with_daily_granularity_returns_seven_intervals(client, application):
    """
    Tests counting the transactions in a 7-day duration (from 2023-11-01 to 2023-11-07) with daily granularity (period=day).

    Given: Transactions spanning 7 days
    When: Requesting daily transaction counts
    Then: Returns 7 intervals with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T12:00:00.000&date_to=2023-11-07T11:59:59.999",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 7
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [
        (29, 4, 9, 2),
        (10, 0, 0, 2),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (1, 1, 1, 0),
        (0, 0, 0, 0),
    ]


def test_30day_duration_with_daily_granularity_returns_thirty_intervals(client, application):
    """
    Tests counting the transactions in a 30-day duration (from 2023-11-01 to 2023-11-30) with daily granularity (period=day).

    Given: Transactions spanning 30 days
    When: Requesting daily transaction counts
    Then: Returns 30 intervals with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T12:00:00.000&date_to=2023-11-30T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 30
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [
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
    ]


def test_3day_duration_with_weekly_granularity_returns_single_interval(client, application):
    """
    Tests counting the transactions in a 3-day duration (from 2023-11-01 to 2023-11-03) with weekly granularity (period=week).

    Given: Transactions spanning 3 days
    When: Requesting weekly transaction counts
    Then: Returns 1 interval with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=week&date_from=2023-11-01T12:00:00.000&date_to=2023-11-03T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(39, 4, 9, 4)]


def test_7day_duration_with_weekly_granularity_returns_two_intervals(client, application):
    """
    Tests counting the transactions in a 7-day duration (from 2023-11-01 to 2023-11-07) with weekly granularity (period=week).

    Given: Transactions spanning 7 days
    When: Requesting weekly transaction counts
    Then: Returns 2 intervals with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=week&date_from=2023-11-01T12:00:00.000&date_to=2023-11-07T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(40, 5, 10, 4), (0, 0, 0, 0)]


def test_2month_duration_with_weekly_granularity_returns_nine_intervals(client, application):
    """
    Tests counting the transactions by status code in a 2-month duration (from 2023-11-01 to 2023-12-31) with weekly granularity (period=week).

    Given: Transactions spanning 2 months
    When: Requesting weekly transaction counts
    Then: Returns 9 intervals with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=week&date_from=2023-11-01T12:00:00.000&date_to=2023-12-31T00:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 9
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [
        (40, 5, 10, 4),
        (4, 0, 0, 0),
        (3, 0, 2, 0),
        (1, 0, 0, 1),
        (5, 1, 0, 0),
        (3, 0, 0, 0),
        (2, 0, 0, 0),
        (0, 3, 0, 0),
        (0, 0, 0, 0),
    ]


def test_1month_duration_with_weekly_granularity_returns_single_interval(client, application):
    """
    Tests counting the transactions by status code in a 1-month duration (from 2024-03-29 to 2024-04-30) with weekly granularity (period=week).

    Given: Transactions spanning a month
    When: Requesting weekly transaction counts
    Then: Returns 1 interval with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=week&date_from=2024-03-29T00:00:00.000&date_to=2024-04-30T00:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_7day_duration_with_monthly_granularity_returns_single_interval(client, application):
    """
    Tests counting the transactions by status code in a 7-day duration (from 2023-11-01 to 2023-11-07) with monthly granularity (period=month).

    Given: Transactions spanning 7 days
    When: Requesting monthly transaction counts
    Then: Returns 1 interval with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=month&date_from=2023-11-01T12:00:00&date_to=2023-11-07T12:00:00",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(40, 5, 10, 4)]


def test_30day_duration_with_monthly_granularity_returns_single_interval(client, application):
    """
    Tests counting the transactions by status code in a 30-day duration (from 2023-11-01 to 2023-11-30) with monthly granularity (period=month).

    Given: Transactions spanning 30 days
    When: Requesting monthly transaction counts
    Then: Returns 1 interval with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=month&date_from=2023-11-01T12:00:00.000&date_to=2023-11-30T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(50, 5, 12, 5)]


def test_6month_duration_with_monthly_granularity_returns_six_intervals(client, application):
    """
    Tests counting the transactions by status code in a 6-month duration (from 2023-10-01 to 2024-03-31) with monthly granularity (period=month).

    Given: Transactions spanning 6 months
    When: Requesting monthly transaction counts
    Then: Returns 6 intervals with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=month&date_from=2023-10-01T12:00:00.000&date_to=2024-03-31T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 6
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [
        (0, 0, 0, 0),
        (50, 5, 12, 5),
        (10, 4, 0, 0),
        (6, 1, 1, 1),
        (0, 0, 0, 0),
        (7, 4, 4, 1),
    ]


def test_1month_duration_with_monthly_granularity_returns_empty_interval(client, application):
    """
    Tests counting the transactions by status code in a 1-month duration (from 2024-05-01 to 2024-06-01) with monthly granularity (period=month).

    Given: Transactions spanning a month
    When: Requesting monthly transaction counts
    Then: Returns empty interval list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=month&date_from=2024-05-01T12:00:00.000&date_to=2024-06-01T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_2month_duration_with_yearly_granularity_returns_single_interval(client, application):
    """
    Tests counting the transactions by status code in a 2-month duration (from 2023-11-01 to 2023-12-31) with yearly granularity (period=year).

    Given: Transactions spanning 2 months
    When: Requesting yearly transaction counts
    Then: Returns 1 interval with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=year&date_from=2023-11-01T12:00:00.000&date_to=2023-12-31T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(59, 9, 12, 5)]


def test_5month_duration_with_yearly_granularity_returns_two_intervals(client, application):
    """
    Tests counting the transactions by status code in a 5-month duration (from 2023-11-01 to 2024-03-31) with yearly granularity (period=year).

    Given: Transactions spanning 5 months
    When: Requesting yearly transaction counts
    Then: Returns 2 intervals with aggregated status counts
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=year&date_from=2023-11-01T12:00:00.000&date_to=2024-03-31T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert [
        (stat["status_200"], stat["status_300"], stat["status_400"], stat["status_500"])
        for stat in response.json()
    ] == [(60, 9, 12, 5), (13, 5, 5, 2)]


def test_9month_duration_with_yearly_granularity_returns_empty_interval(client, application):
    """
    Tests counting the transactions by status code in a 9-month duration (from 2024-03-31 to 2024-12-31) with yearly granularity (period=year).

    Given: Transactions spanning 9 months
    When: Requesting yearly transaction counts
    Then: Returns empty interval list
    """
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv("test_transactions.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=year&date_from=2024-03-31T12:00:00.000&date_to=2024-12-31T12:00:00.000",
        headers=header,
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0

