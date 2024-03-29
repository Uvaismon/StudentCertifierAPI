from web3 import Web3
import json
import os
from django.conf import settings
from decouple import config
import requests
from web3.gas_strategies.rpc import rpc_gas_price_strategy
import time


class ContractHelper:

    def __init__(self, network_url, contract_address):

        self.w3 = Web3(Web3.HTTPProvider(network_url))
        abi_path = os.path.join(settings.BASE_DIR, r'certification/static/certification/abi.json')
        with open(abi_path) as abi_file:
            self.abi = json.load(abi_file)
        self.address = self.w3.toChecksumAddress(contract_address)
        self.contract = self.w3.eth.contract(address=contract_address, abi=self.abi)

    def add_hash(self, certificate_id, certificate_hash):
        # try:
        transaction = self.contract.functions.add_hash(certificate_id, certificate_hash).buildTransaction({
            'nonce': self.w3.eth.getTransactionCount(config('ETHEREUM_ACCOUNT_ADDRESS'), 'pending'),
            'from': config('ETHEREUM_ACCOUNT_ADDRESS')
        })
        
        signed_transaction = self.w3.eth.account.signTransaction(
            transaction, config('ETHEREUM_ACCOUNT_PRIVATE_KEY'))
        transaction_hash = self.w3.eth.sendRawTransaction(
            signed_transaction.rawTransaction)
            # self.w3.eth.wait_for_transaction_receipt(transaction_hash)
        # except:
        #     time.sleep(1)
        #     return self.add_hash(certificate_id, certificate_hash)
        return transaction_hash

    def get_hash(self, certificate_id):
        return self.contract.functions.get_hash(certificate_id).call()

    def compare_hash(self, certificate_id, file_hash):
        return file_hash == self.get_hash(certificate_id)

    def estimate_fee(self):
        ETHER_PRICE_API = 'https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD'

        ether_price = requests.get(ETHER_PRICE_API).json()['USD']

        ether_required = self.estimate_fee_wei() / (10 ** 18)
        transaction_fee = ether_required * ether_price
        return transaction_fee

    def estimate_fee_wei(self):
        dummy_certificate_id = 115792089237316195423570985008687907853269984665640564039457584007913129639935
        dummy_certificate_hash = 'd2607ab3cd54242c1ad78fa35052ba7c8aafd4f4781503f2274c31063a85f560'
        transaction = self.contract.functions.add_hash(dummy_certificate_id, dummy_certificate_hash).buildTransaction({
            'nonce': self.w3.eth.getTransactionCount(config('ETHEREUM_ACCOUNT_ADDRESS')),
            'from': config('ETHEREUM_ACCOUNT_ADDRESS')
        })
        gas_price = self.estimate_cost()
        gas_required = self.w3.eth.estimateGas(transaction)
        return gas_required * gas_price

    def estimate_cost(self):
        self.w3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
        return self.w3.eth.generate_gas_price()

    def get_transaction_details(self, transaction_hash):
        return self.w3.eth.get_transaction(transaction_hash)
        