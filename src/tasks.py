from models import Transaction


def persist_transaction(transaction: Transaction):
    print("persisting", transaction)
