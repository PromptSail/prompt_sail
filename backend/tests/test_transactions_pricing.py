from utils import read_transactions_from_csv

header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsImN0eSI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0IiwiYXpwIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNDA3NDA4NzE4MTkyLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTEyMTAyODc3OTUzNDg0MzUyNDI3IiwiZW1haWwiOiJ0ZXN0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiYm54OW9WT1o4U3FJOTcyczBHYjd4dyIsIm5hbWUiOiJUZXN0IFVzZXIiLCJwaWN0dXJlIjoiIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIiLCJpYXQiOjE3MTM3MzQ0NjEsImV4cCI6OTk5OTk5OTk5OX0.eZYMQzcSRzkAq4Me8C6SNU3wduS7EIu_o5XGAbsDmU05GtyipQEb5iNJ1QiLg-11RbZFL3dvi8xKd3mpuw8b-5l6u8hwSpZg6wNPLY0zPX-EOwxeHLtev_2X5pUf1_IWAnso9K_knsK8CcmJoVsCyNNjlw3hrkChacJHGNzg0TTT1rh3oe6KCpbLvYlV6tUPfm5k3AMFZIT7Jntr38CZvs6gac6L_DhItJc3TNNUUHie2zgA29_r9YFlaEr_nGoSmBhIi-i0i0h34TL4JAb4qJkVM2YI2eTTv2HjEGtkx4mE5JvNQ0VxzHSJcCNOHh1gCiFD5c6rhvvxVeEqMkGGbCZKHX_vCgnIp0iE_OWyICjVTFPitQJ00fXLhyHyPb7q5J605tuK2iTHp2NCRJEXIAl9e0F_qASBBAfyL0C4FCBtvbnEMwtpoV1VWinkKgkI7JVH0AsyTugjXyAjxxsJxBTJT9qwZLxVBoaxgqNTOFfxvwstyq1VfCl3iBbpt71D"
}


def test_openai_costs(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv("../test_transactions_pricing.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get("/api/transactions?page=1&page_size=100", headers=header)
    data = [item for item in response.json()["items"] if item["provider"] == "OpenAI"]
    case1 = [item for item in data if item["model"] == "babbage-002"][0]
    case2 = [item for item in data if item["model"] == "davinci-002"][0]
    case3 = [item for item in data if item["model"] == "gpt-3.5-turbo-0125"][0]
    case4 = [item for item in data if item["model"] == "gpt-3.5-turbo-0301"][0]
    case5 = [item for item in data if item["model"] == "gpt-3.5-turbo-0613"][1]
    case6 = [item for item in data if item["model"] == "gpt-3.5-turbo-1106"][0]
    case7 = [item for item in data if item["model"] == "gpt-3.5-turbo-16k-0613"][0]
    case8 = [item for item in data if item["model"] == "gpt-3.5-turbo-instruct"][0]
    case9 = [item for item in data if item["model"] == "gpt-3.5-turbo-instruct-0914"][0]
    case10 = [item for item in data if item["model"] == "gpt-4-0125-preview"][0]
    case11 = [item for item in data if item["model"] == "gpt-4-0613"][0]
    case12 = [item for item in data if item["model"] == "gpt-4-1106-preview"][0]
    case13 = [item for item in data if item["model"] == "gpt-4-1106-vision-preview"][0]
    case14 = [item for item in data if item["model"] == "gpt-4-turbo-2024-04-09"][0]
    case15 = [item for item in data if item["model"] == "text-embedding-3-small"][0]
    case16 = [item for item in data if item["model"] == "text-embedding-3-large"][0]
    case17 = [item for item in data if item["model"] == "text-embedding-ada-002"][0]
    case18 = [item for item in data if item["model"] == "gpt-3.5-turbo-0000"][0]
    case19 = [item for item in data if item["model"] == "gpt-3.5-turbo-0100"][0]
    case20 = [item for item in data if item["model"] == "gpt-3.5-turbo-0613"][0]

    # assert
    assert response.status_code == 200
    assert len(data) == 20
    assert case1["total_cost"] - 0.00001 <= 0.000086400 <= case1["total_cost"] + 0.00001
    assert case2["total_cost"] - 0.00001 <= 0.000124000 <= case2["total_cost"] + 0.00001
    assert case3["total_cost"] - 0.00001 <= 0.001165500 <= case3["total_cost"] + 0.00001
    assert case4["total_cost"] - 0.00001 <= 0.000078000 <= case4["total_cost"] + 0.00001
    assert case5["total_cost"] - 0.00001 <= 0.000175000 <= case5["total_cost"] + 0.00001
    assert case6["total_cost"] - 0.00001 <= 0.000082000 <= case6["total_cost"] + 0.00001
    assert case7["total_cost"] - 0.00001 <= 0.000514000 <= case7["total_cost"] + 0.00001
    assert case8["total_cost"] - 0.00001 <= 0.000646500 <= case8["total_cost"] + 0.00001
    assert case9["total_cost"] - 0.00001 <= 0.000908000 <= case9["total_cost"] + 0.00001
    assert (
        case10["total_cost"] - 0.00001 <= 0.002810000 <= case10["total_cost"] + 0.00001
    )
    assert (
        case11["total_cost"] - 0.00001 <= 0.007380000 <= case11["total_cost"] + 0.00001
    )
    assert (
        case12["total_cost"] - 0.00001 <= 0.003230000 <= case12["total_cost"] + 0.00001
    )
    assert (
        case13["total_cost"] - 0.00001 <= 0.003250000 <= case13["total_cost"] + 0.00001
    )
    assert (
        case14["total_cost"] - 0.00001 <= 0.003670000 <= case14["total_cost"] + 0.00001
    )
    assert (
        case15["total_cost"] - 0.00001 <= 0.000010660 <= case15["total_cost"] + 0.00001
    )
    assert (
        case16["total_cost"] - 0.00001 <= 0.000130000 <= case16["total_cost"] + 0.00001
    )
    assert (
        case17["total_cost"] - 0.00001 <= 0.000150000 <= case17["total_cost"] + 0.00001
    )
    assert case18["total_cost"] == 0
    assert case19["total_cost"] is None
    assert case20["total_cost"] == 0


def test_azure_costs(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv("../test_transactions_pricing.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get("/api/transactions?page=1&page_size=100", headers=header)
    data = [
        item for item in response.json()["items"] if item["provider"] == "Azure OpenAI"
    ]
    case1 = [item for item in data if item["model"] == "babbage-002-1"][0]
    case2 = [item for item in data if item["model"] == "davinci-002-1"][0]
    case3 = [item for item in data if item["model"] == "gpt-35-turbo-0125"][0]
    case4 = [item for item in data if item["model"] == "gpt-3.5-turbo-0125"][0]
    case5 = [item for item in data if item["model"] == "gpt-35-turbo-0301"][0]
    case6 = [item for item in data if item["model"] == "gpt-3.5-turbo-0301"][0]
    case7 = [item for item in data if item["model"] == "gpt-35-turbo-0613"][0]
    case8 = [item for item in data if item["model"] == "gpt-3.5-turbo-0613"][0]
    case9 = [item for item in data if item["model"] == "gpt-35-turbo-1106"][0]
    case10 = [item for item in data if item["model"] == "gpt-3.5-turbo-1106"][0]
    case11 = [item for item in data if item["model"] == "gpt-35-turbo-16k-0613"][0]
    case12 = [item for item in data if item["model"] == "gpt-3.5-turbo-16k-0613"][0]
    case13 = [item for item in data if item["model"] == "gpt-35-turbo-instruct-0914"][0]
    case14 = [item for item in data if item["model"] == "gpt-3.5-turbo-instruct-0914"][
        0
    ]
    case15 = [item for item in data if item["model"] == "gpt-4-0125-preview"][0]
    case16 = [item for item in data if item["model"] == "gpt-4-0613"][0]
    case17 = [item for item in data if item["model"] == "gpt-4-1106-preview"][0]
    case18 = [item for item in data if item["model"] == "gpt-4-32k-0613"][0]
    case19 = [item for item in data if item["model"] == "gpt-4-vision-preview"][0]
    case20 = [item for item in data if item["model"] == "text-embedding-3-small-1"][0]
    case21 = [item for item in data if item["model"] == "text-embedding-3-large-1"][0]
    case22 = [item for item in data if item["model"] == "text-embedding-ada-002-1"][0]
    case23 = [item for item in data if item["model"] == "text-embedding-ada-002-2"][0]
    case24 = [item for item in data if item["model"] == "text-embedding-ada-002"][0]
    case25 = [item for item in data if item["model"] == "gpt-35t-ps"][0]

    # assert
    assert response.status_code == 200
    assert len(data) == 25
    assert case1["total_cost"] - 0.00001 <= 0.000142400 <= case1["total_cost"] + 0.00001
    assert case2["total_cost"] - 0.00001 <= 0.000324000 <= case2["total_cost"] + 0.00001
    assert case3["total_cost"] - 0.00001 <= 0.001215500 <= case3["total_cost"] + 0.00001
    assert case4["total_cost"] - 0.00001 <= 0.000879000 <= case4["total_cost"] + 0.00001
    assert case5["total_cost"] - 0.00001 <= 0.000296000 <= case5["total_cost"] + 0.00001
    assert case6["total_cost"] - 0.00001 <= 0.000496000 <= case6["total_cost"] + 0.00001
    assert case7["total_cost"] - 0.00001 <= 0.000407000 <= case7["total_cost"] + 0.00001
    assert case8["total_cost"] - 0.00001 <= 0.000607000 <= case8["total_cost"] + 0.00001
    assert case9["total_cost"] - 0.00001 <= 0.000282000 <= case9["total_cost"] + 0.00001
    assert (
        case10["total_cost"] - 0.00001 <= 0.000382000 <= case10["total_cost"] + 0.00001
    )
    assert (
        case11["total_cost"] - 0.00001 <= 0.000714000 <= case11["total_cost"] + 0.00001
    )
    assert (
        case12["total_cost"] - 0.00001 <= 0.001014000 <= case12["total_cost"] + 0.00001
    )
    assert (
        case13["total_cost"] - 0.00001 <= 0.001058000 <= case13["total_cost"] + 0.00001
    )
    assert (
        case14["total_cost"] - 0.00001 <= 0.001258000 <= case14["total_cost"] + 0.00001
    )
    assert (
        case15["total_cost"] - 0.00001 <= 0.003810000 <= case15["total_cost"] + 0.00001
    )
    assert (
        case16["total_cost"] - 0.00001 <= 0.010080000 <= case16["total_cost"] + 0.00001
    )
    assert (
        case17["total_cost"] - 0.00001 <= 0.006230000 <= case17["total_cost"] + 0.00001
    )
    assert (
        case18["total_cost"] - 0.00001 <= 0.031680000 <= case18["total_cost"] + 0.00001
    )

    assert (
        case19["total_cost"] - 0.00001 <= 0.004250000 <= case19["total_cost"] + 0.00001
    )

    assert (
        case20["total_cost"] - 0.00001 <= 0.000006660 <= case20["total_cost"] + 0.00001
    )
    assert (
        case21["total_cost"] - 0.00001 <= 0.000054730 <= case21["total_cost"] + 0.00001
    )
    assert (
        case22["total_cost"] - 0.00001 <= 0.000120000 <= case22["total_cost"] + 0.00001
    )
    assert (
        case23["total_cost"] - 0.00001 <= 0.000150000 <= case23["total_cost"] + 0.00001
    )
    assert case24["total_cost"] is None
    assert case25["total_cost"] is None


def test_anthropic_costs(client, application):
    # arrange
    with application.transaction_context() as ctx:
        repo = ctx["transaction_repository"]
        repo.delete_cascade(project_id="project-test")
        transactions = read_transactions_from_csv("../test_transactions_pricing.csv")
        for transaction in transactions:
            repo.add(transaction)

    # act
    response = client.get("/api/transactions?page=1&page_size=100", headers=header)
    data = [
        item for item in response.json()["items"] if item["provider"] == "Anthropic"
    ]
    case1 = [item for item in data if item["model"] == "claude-2.0"][0]
    case2 = [item for item in data if item["model"] == "claude-2.1"][0]
    case3 = [item for item in data if item["model"] == "claude-3-haiku-20240307"][0]
    case4 = [item for item in data if item["model"] == "claude-3-opus-20240229"][0]
    case5 = [item for item in data if item["model"] == "claude-3-sonnet-20240229"][0]
    case6 = [item for item in data if item["model"] == "claude-instant-1.2"][0]

    # assert
    assert response.status_code == 200
    assert len(data) == 6
    assert case1["total_cost"] - 0.00001 <= 0.007976000 <= case1["total_cost"] + 0.00001
    assert case2["total_cost"] - 0.00001 <= 0.009408000 <= case2["total_cost"] + 0.00001
    assert case3["total_cost"] - 0.00001 <= 0.000578500 <= case3["total_cost"] + 0.00001
    assert case4["total_cost"] - 0.00001 <= 0.049290000 <= case4["total_cost"] + 0.00001
    assert case5["total_cost"] - 0.00001 <= 0.007581000 <= case5["total_cost"] + 0.00001
    assert case6["total_cost"] - 0.00001 <= 0.000845600 <= case6["total_cost"] + 0.00001
