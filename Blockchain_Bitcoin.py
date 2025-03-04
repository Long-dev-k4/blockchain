import hashlib
import time
import json
import random

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty):
        """ Proof of Work: Tìm nonce sao cho hash có số lượng số 0 nhất định ở đầu """
        start_time = time.time()
        while not self.hash.startswith('0' * difficulty):
            self.nonce += 1
            self.hash = self.compute_hash()
        end_time = time.time()
        self.mining_time = end_time - start_time  # Thời gian đào block

class Blockchain:
    REWARD = 50  # Phần thưởng cho miner khi đào thành công

    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """ Tạo khối đầu tiên (Genesis Block) """
        genesis_block = Block(0, "0", [], time.time())
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_transaction(self, sender, receiver, amount):
        """ Thêm giao dịch vào danh sách chờ """
        transaction = {"sender": sender, "receiver": receiver, "amount": amount}
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        """ Đào khối mới với các giao dịch đang chờ và trả thưởng """
        if not self.pending_transactions:
            return False

        # Thêm giao dịch thưởng cho miner
        reward_transaction = {"sender": "System", "receiver": miner_address, "amount": self.REWARD}
        self.pending_transactions.append(reward_transaction)

        new_block = Block(len(self.chain), self.chain[-1].hash, self.pending_transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []  # Xóa giao dịch sau khi thêm vào blockchain
        return new_block

    def get_balance(self, address):
        """ Kiểm tra số dư của một người trong blockchain """
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["receiver"] == address:
                    balance += transaction["amount"]
                if transaction["sender"] == address:
                    balance -= transaction["amount"]
        return balance

    def is_valid_chain(self):
        """ Kiểm tra chuỗi có hợp lệ không """
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            current_block = self.chain[i]

            if current_block.hash != current_block.compute_hash():
                return False
            if current_block.previous_hash != prev_block.hash:
                return False
        return True

    def print_chain(self):
        """ Hiển thị toàn bộ chuỗi khối """
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Transactions: {block.transactions}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print(f"Mining Time: {getattr(block, 'mining_time', 'N/A')} seconds")
            print("-" * 50)

# ---- Chạy thử Blockchain ----
if __name__ == "__main__":
    bitcoin = Blockchain(difficulty=4)
    
    # Thêm giao dịch
    bitcoin.add_transaction("Long", "Huy", 50000)
    bitcoin.add_transaction("Minh", "Long", 22000)
    
    # Chọn một miner ngẫu nhiên để đào block
    miner = random.choice(["Long", "Huy", "Minh", "Dat"])
    print(f"Miner được chọn: {miner}")

    # Đào khối mới
    bitcoin.mine_pending_transactions(miner)

    # Thêm giao dịch khác
    bitcoin.add_transaction("Dat", "Huy", 30000)
    miner = random.choice(["Long", "Huy", "Minh", "Dat"])
    print(f"Miner được chọn: {miner}")

    bitcoin.mine_pending_transactions(miner)

    # In toàn bộ chuỗi khối
    bitcoin.print_chain()
    
    # Kiểm tra số dư tài khoản
    print(f"Số dư của Long: {bitcoin.get_balance('Long')}")
    print(f"Số dư của Huy: {bitcoin.get_balance('Huy')}")
    print(f"Số dư của Minh: {bitcoin.get_balance('Minh')}")
    print(f"Số dư của Dat: {bitcoin.get_balance('Dat')}")
    
    # Kiểm tra tính hợp lệ của chuỗi khối
    print("Blockchain hợp lệ:", bitcoin.is_valid_chain())
