from utils import read_transactions_from_csv


def test_transaction_count_min_5min(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:04:59"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_transaction_count_min_30min(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:29:59"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_transaction_count_min_1h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=5minutes&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:59:59"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 12


def test_transaction_count_min_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=5minutes&date_from=2023-10-01&date_to=2023-10-31"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_transaction_count_hour_30min(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00&date_to=2023-11-01T12:30:00"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_transaction_count_hour_1h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00&date_to=2023-11-01T13:00:00"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_transaction_count_hour_24h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=hour&date_from=2023-11-01T12:00:00&date_to=2023-11-02T11:59:59"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 24


def test_transaction_count_hour_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=hour&date_from=2023-10-01&date_to=2023-10-31"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_transaction_count_day_6h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T12:00:00&date_to=2023-11-01T18:00:00"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_transaction_count_day_1d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01&date_to=2023-11-01"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_transaction_count_day_24h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T13:00:00&date_to=2023-11-02T13:00:00"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_transaction_count_day_7d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T12:00:00&date_to=2023-11-07T11:59:59"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 7


def test_transaction_count_day_1mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=day&date_from=2023-11-01T12:00:00&date_to=2023-11-30T12:00:00"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 30


def test_transaction_count_week_3d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=week&date_from=2023-11-01T12:00:00&date_to=2023-11-03T12:00:00"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_transaction_count_week_7d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=week&date_from=2023-11-01T12:00:00&date_to=2023-11-07T12:00:00"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_transaction_count_week_2mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=week&date_from=2023-11-01T12:00:00&date_to=2023-12-31"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 9


def test_transaction_count_week_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=week&date_from=2024-03-29&date_to=2024-04-30"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_transaction_count_month_7d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=month&date_from=2023-11-01T12:00:00&date_to=2023-11-07T12:00:00"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_transaction_count_month_1mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=month&date_from=2023-11-01&date_to=2023-11-30"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_transaction_count_month_6mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=month&date_from=2023-10-01&date_to=2024-03-31"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_transaction_count_month_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=month&date_from=2024-05-01&date_to=2024-06-01"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_transaction_count_year_2mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=year&date_from=2023-11-01&date_to=2023-12-31"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_transaction_count_year_2y(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=year&date_from=2023-11-01&date_to=2024-03-31"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_transaction_count_year_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get(
        "/api/statistics/transactions_count?project_id=project-test&period=year&date_from=2024-03-31&date_to=2024-12-31"
    )

    # assert
    assert response.status_code == 200
    assert len(response.json()) == 0
