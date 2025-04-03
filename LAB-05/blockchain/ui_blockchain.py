import tkinter as tk
from tkinter import messagebox, scrolledtext
from blockchain import Blockchain

class BlockchainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Simulator")
        self.blockchain = Blockchain()

        # Blockchain display
        tk.Label(root, text="Blockchain:").grid(row=0, column=0, padx=10, pady=5)
        self.text_blockchain = scrolledtext.ScrolledText(root, width=80, height=20, state=tk.DISABLED)
        self.text_blockchain.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Transaction inputs
        tk.Label(root, text="Sender:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_sender = tk.Entry(root, width=20)
        self.entry_sender.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Receiver:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entry_receiver = tk.Entry(root, width=20)
        self.entry_receiver.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Amount:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entry_amount = tk.Entry(root, width=20)
        self.entry_amount.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        self.btn_add_transaction = tk.Button(root, text="Add Transaction", command=self.add_transaction)
        self.btn_add_transaction.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_mine_block = tk.Button(root, text="Mine Block", command=self.mine_block)
        self.btn_mine_block.grid(row=5, column=2, pady=10)

        self.btn_validate_chain = tk.Button(root, text="Validate Blockchain", command=self.validate_blockchain)
        self.btn_validate_chain.grid(row=6, column=0, columnspan=3, pady=10)

        # Initialize blockchain display
        self.update_blockchain_display()

    def update_blockchain_display(self):
        self.text_blockchain.config(state=tk.NORMAL)
        self.text_blockchain.delete(1.0, tk.END)
        for block in self.blockchain.chain:
            self.text_blockchain.insert(tk.END, f"Block #{block.index}\n")
            self.text_blockchain.insert(tk.END, f"Timestamp: {block.timestamp}\n")
            self.text_blockchain.insert(tk.END, f"Transactions: {block.transactions}\n")
            self.text_blockchain.insert(tk.END, f"Proof: {block.proof}\n")
            self.text_blockchain.insert(tk.END, f"Previous Hash: {block.previous_hash}\n")
            self.text_blockchain.insert(tk.END, f"Hash: {block.hash}\n")
            self.text_blockchain.insert(tk.END, "-" * 50 + "\n")
        self.text_blockchain.config(state=tk.DISABLED)

    def add_transaction(self):
        sender = self.entry_sender.get()
        receiver = self.entry_receiver.get()
        amount = self.entry_amount.get()

        if not sender or not receiver or not amount:
            messagebox.showwarning("Warning", "All fields must be filled!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        self.blockchain.add_transaction(sender, receiver, amount)
        messagebox.showinfo("Success", "Transaction added!")
        self.entry_sender.delete(0, tk.END)
        self.entry_receiver.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)

    def mine_block(self):
        previous_block = self.blockchain.get_previous_block()
        previous_proof = previous_block.proof
        proof = self.blockchain.proof_of_work(previous_proof)
        previous_hash = previous_block.hash
        self.blockchain.create_block(proof, previous_hash)
        messagebox.showinfo("Success", "Block mined successfully!")
        self.update_blockchain_display()

    def validate_blockchain(self):
        is_valid = self.blockchain.is_chain_valid(self.blockchain.chain)
        validation_message = f"Is Blockchain Valid: {is_valid}"
        self.text_blockchain.config(state=tk.NORMAL)
        self.text_blockchain.insert(tk.END, validation_message + "\n")
        self.text_blockchain.config(state=tk.DISABLED)
        if is_valid:
            messagebox.showinfo("Validation", validation_message)
        else:
            messagebox.showerror("Validation", validation_message)
        # Thêm dòng này để cập nhật giao diện blockchain sau khi kiểm tra
        self.update_blockchain_display()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()
