import hashlib
import time

class Transaction:
    def __init__(self, voter_id, candidate_id):
        self.voter_id = voter_id
        self.candidate_id = candidate_id
        self.timestamp = time.time()

    def to_dict(self):
        return {
            'voter_id': self.voter_id,
            'candidate_id': self.candidate_id,
            'timestamp': self.timestamp
        }


class Block:
    def __init__(self, index, previous_hash, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.transactions}{self.timestamp}".encode()
        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(previous_hash='0')  # Genesis block

    def create_block(self, previous_hash):
        block = Block(index=len(self.chain) + 1, previous_hash=previous_hash, transactions=self.current_transactions)
        self.current_transactions = []  # Reset the current transaction list
        self.chain.append(block)
        return block

    def add_transaction(self, voter_id, candidate_id):
        transaction = Transaction(voter_id, candidate_id)
        self.current_transactions.append(transaction.to_dict())
        return self.last_block.index + 1  # Return the index of the block that will hold this transaction

    @property
    def last_block(self):
        return self.chain[-1]

    def mine_block(self):
        previous_hash = self.last_block.hash
        block = self.create_block(previous_hash)
        return block


# Example usage:
if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Simulate adding a transaction
    transaction_index = blockchain.add_transaction(voter_id=1, candidate_id=2)
    print(f"Transaction will be added to block {transaction_index}")

    # Mine the block
    mined_block = blockchain.mine_block()
    print(f"New block mined: {mined_block.index} with hash: {mined_block.hash}")
