from web3 import Web3
from django.conf import settings
from .models import Vote, CatsedVote
import hashlib
from core import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64


# Setup web3 connection and contract instance
infura_project_id = secrets.INFURA_API_KEY  # replace with your actual project ID
infura_url = f'https://sepolia.infura.io/v3/{infura_project_id}'
web3 = Web3(Web3.HTTPProvider(infura_url))
contract_address = secrets.ETHEREUM_WALLET_ADDRESS
contract_abi = [
  {
    "constant": True,
    "inputs": [{"name": "_candidateId", "type": "uint256"}],
    "name": "getVotes",
    "outputs": [{"name": "votes", "type": "uint256"}],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": True,
    "inputs": [{"name": "_voterId", "type": "string"}, {"name": "_candidateName", "type": "string"}],
    "name": "recordVote",
    "outputs": [],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
def encrypt_vote(vote_id: int, secret_key: str) -> str:
    key = secret_key.encode('utf-8')[:32]  # Ensure 32-byte key length for AES-256
    
    # Generate a random initialization vector (IV) for encryption
    iv = os.urandom(16)
    
    # Encrypt the vote ID with AES (CBC mode)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Prepare the vote ID for encryption (padding to ensure block size)
    padded_vote_id = str(vote_id).ljust(16)  # Example padding to make the length multiple of block size
    encrypted_vote_id = encryptor.update(padded_vote_id.encode('utf-8')) + encryptor.finalize()
    
    # Combine the IV and the encrypted vote ID
    encrypted_data = iv + encrypted_vote_id
    
    # Return the base64 encoded encrypted data
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_vote(encrypted_transaction_id: str) -> int:
    key = secrets.SECRET_KEY.encode('utf-8')[:32]
    encrypted_data = base64.b64decode(encrypted_transaction_id)
    
    # Extract the IV and the encrypted vote ID
    iv = encrypted_data[:16]
    encrypted_vote_id = encrypted_data[16:]
    
    # Decrypt the vote ID
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_vote_id) + decryptor.finalize()
    
    # Return the decrypted vote ID (convert from bytes to int)
    return int(decrypted_data.strip())

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Cast vote and save transaction ID
def cast_vote(voter, candidate, council, polling_station, polling_booth, gender):
    # Create a new Vote instance in the database
    vote = Vote.objects.create(
        voter=voter,
        candidate=candidate,
        council=council,
        polling_station=polling_station,
        polling_booth=polling_booth,
        gender=gender
    )
    
    # Fetch the current nonce for the Ethereum wallet
    nonce = web3.eth.get_transaction_count(secrets.ETHEREUM_WALLET_ADDRESS)

    # Build the transaction for the recordVote function on the contract
    txn_id = encrypt_vote(vote_id=vote.id, secret_key=secrets.SECRET_KEY)
    
    # Create a CatsedVote instance to store the transaction ID
    CatsedVote.objects.create(transaction_id=txn_id)

    vote.save()
    
    return txn_id

def get_vote_count(candidate_id):
    # Fetch the vote count for a candidate from the contract
    vote_count = contract.functions.getVoteCount(candidate_id).call()
    return vote_count
