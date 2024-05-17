from utils import read_transactions_from_csv

header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
}


def test_transaction_count_min_5min(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_min_30min(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_min_1h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_min_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_hour_30min(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_hour_1h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_hour_24h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_hour_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_day_6h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_day_1d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_day_24h(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_day_7d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_day_1mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_week_3d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_week_7d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_week_2mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_week_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_month_7d(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_month_1mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_month_6mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_month_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_year_2mo(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_year_2y(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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


def test_transaction_count_year_empty(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        transactions = read_transactions_from_csv()
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
