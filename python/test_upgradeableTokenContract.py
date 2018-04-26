#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
how to use:
1. start ganache
2. from your terminal cd in this project
3. use truffle to compile the solidity code (i.e. smart contracts). $ truffle compile
4. in this script update the 'userName' variable with your OS userName
5. run this python script
6. if you experience errors try restarting ganache and deleting the build folder (and recompile then)
"""

from web3 import Web3, HTTPProvider
import json
import time

# ganache URL
URL = 'http://localhost:7545'

w3 = Web3(HTTPProvider(URL))

def checkReceiptStatus(_txHash):
    while(1):
        time.sleep(0.1)
        try:
            receipts = w3.eth.getTransactionReceipt(_txHash)
            if(receipts != None):
                if(receipts['status'] == 1):
                    break
                else:
                    raise('transaction failed')  
        except:
            raise('failed to read receipt')       

        
# define actors
coinbase = w3.eth.coinbase
sender = w3.eth.accounts[1]
receiver = w3.eth.accounts[2]

userName = 'yourUserName'
dirPath = '/home/' + userName + '/github/ethereum_contract_upgradeablitiy_simple_example/'

# create contract objects
proxy = w3.eth.contract(abi=json.load(open(dirPath + 'build/contracts/Proxy.json'))['abi'],
                        bytecode=json.load(open(dirPath + 'build/contracts/Proxy.json'))['bytecode'])
tokenV1 = w3.eth.contract(abi=json.load(open(dirPath + 'build/contracts/TokenVersion1.json'))['abi'],
                          bytecode=json.load(open(dirPath + 'build/contracts/TokenVersion1.json'))['bytecode'])
tokenV2 = w3.eth.contract(abi=json.load(open(dirPath + 'build/contracts/TokenVersion2.json'))['abi'],
                          bytecode=json.load(open(dirPath + 'build/contracts/TokenVersion2.json'))['bytecode'])

# deploy contracts
txHash = proxy.constructor().transact({'from':coinbase})
checkReceiptStatus(txHash)
proxy = w3.eth.contract(address=w3.eth.getTransactionReceipt(txHash)['contractAddress'],
                        abi=proxy.abi)
print('proxy contract deploy at {}'.format(proxy.address))

txHash = tokenV1.constructor().transact({'from':coinbase})
checkReceiptStatus(txHash)
tokenV1 = w3.eth.contract(address=w3.eth.getTransactionReceipt(txHash)['contractAddress'],
                          abi=tokenV1.abi)
print('tokenV1 contract deploy at {}'.format(tokenV1.address))

txHash = tokenV2.constructor().transact({'from':coinbase})
checkReceiptStatus(txHash)
tokenV2 = w3.eth.contract(address=w3.eth.getTransactionReceipt(txHash)['contractAddress'],
                          abi=tokenV2.abi)
print('tokenV2 contract deploy at {}'.format(tokenV2.address))

# abstract objects for sending transactions through the proxy (via its fallback function)
tokenV1Proxy = w3.eth.contract(address=proxy.address, abi=tokenV1.abi)
tokenV2Proxy = w3.eth.contract(address=proxy.address, abi=tokenV2.abi)

# tell the proxy to point to the address of tokenV1
txHash = proxy.functions.upgradeTo(tokenV1.address).transact({'from':coinbase})
checkReceiptStatus(txHash)
print('proxy contract upgraded to token contract version 1 (its address)')

# mint 100 on contract tokenV1 (through the proxy)
txHash = tokenV1Proxy.functions.mint(sender, 100).transact({'from':coinbase})
checkReceiptStatus(txHash)
print('mint 100 to sender - through proxy fallback function')

# tell the proxy to point to the address of tokenV2
txHash = proxy.functions.upgradeTo(tokenV2.address).transact({'from':coinbase})
checkReceiptStatus(txHash)
print('proxy contract upgraded to token contract version 2 (its address)')

# mint 100 on contract tokenV2 (through the proxy)
txHash = tokenV2Proxy.functions.mint(sender, 100).transact({'from':coinbase})
checkReceiptStatus(txHash)
print('mint 100 to sender - through proxy fallback function')

# get balance of sender
senderBalance = tokenV2Proxy.functions.balanceOf(sender).call()
print('sender balance is {}'.format(senderBalance))
print('balance should be 300: 100*2 + 100 = 300')
print('receiver not used yet. Lets try to do a transfer ?')

# transfer 50 from sender to receiver
txHash = tokenV2Proxy.functions.transfer(receiver, 50).transact({'from':sender}) # make sure sender address has ether to pay for the gas
checkReceiptStatus(txHash)
senderBalance = tokenV2Proxy.functions.balanceOf(sender).call()
receiverBalance = tokenV2Proxy.functions.balanceOf(receiver).call()
print('transfering 50 rainbowCoins from sender to receiver')
print('sender balancer after transfer: {}'.format(senderBalance))
print('receiver balancer after transfer: {}'.format(receiverBalance))

# the tokenV2 contract does not storage any data. The state of tokenV2
#  is stored in the proxy contract
print('does tokenV2 contract store any data ?')
senderBalance = tokenV2.functions.balanceOf(sender).call()
print('balance of the sender by calling tokenV2 directly : {}'.format(senderBalance))
print('tokenV2 state is stored on the proxy contract memory !!!')