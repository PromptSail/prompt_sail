from transactions.models import Transaction


class TransactionNotFoundException(Exception):
    ...


class TransactionRepository:
    def __init__(self):
        self._transactions = {}

    def add(self, transaction: Transaction):
        self._transactions[transaction.id] = transaction

    def get(self, transaction_id: str) -> Transaction:
        try:
            return self._transactions[transaction_id]
        except KeyError:
            raise TransactionNotFoundException(transaction_id)

    def get_all(self):
        return self._transactions.values()
