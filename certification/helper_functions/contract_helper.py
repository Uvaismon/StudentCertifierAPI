from web3 import Web3
import json
import os
from django.conf import settings
from decouple import config


class ContractHelper:

    def __init__(self, network_url, contract_address):

        self.w3 = Web3(Web3.HTTPProvider(network_url))
        abi_path = os.path.join(settings.BASE_DIR, r'certification/static/certification/abi.json')
        with open(abi_path) as abi_file:
            self.abi = json.load(abi_file)
        self.address = self.w3.toChecksumAddress(contract_address)
        self.contract = self.w3.eth.contract(address=contract_address, abi=self.abi)

    def add_hash(self, certificate_id, certificate_hash):
        transaction = self.contract.functions.add_hash(certificate_id, certificate_hash).buildTransaction({
            'nonce': self.w3.eth.getTransactionCount(config('ETHEREUM_ACCOUNT_ADDRESS')),
            'from': config('ETHEREUM_ACCOUNT_ADDRESS')
        })
        signed_transaction = self.w3.eth.account.signTransaction(
            transaction, config('ETHEREUM_ACCOUNT_PRIVATE_KEY'))
        transaction_hash = self.w3.eth.sendRawTransaction(
            signed_transaction.rawTransaction)
        self.w3.eth.wait_for_transaction_receipt(transaction_hash)
        return transaction_hash

    def get_hash(self, certificate_id):
        return self.contract.functions.get_hash(certificate_id).call()

    def compare_hash(self, certificate_id, file_hash):
        return file_hash == self.get_hash(certificate_id)
