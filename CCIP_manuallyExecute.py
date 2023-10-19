# manuallyExecute For CCIP
# This sample test on Polygon but you can make it on other chains as well

from web3 import Web3

# select RPC depend on your network
RPC_url = "https://polygon-rpc.com/"
web3 = Web3(Web3.HTTPProvider(RPC_url))

# Just fancy commenet for showing the connection
if web3.is_connected():
    print("-" * 50)
    print("Connection Successful")
    print("-" * 50)
else:
    print("Connection Failed")


# need to change by you own Account that has some facet
account_1 = "{your Account address}"
private_key1 = "{your Account Private Key}"

# some confige
from web3.gas_strategies.rpc import rpc_gas_price_strategy
web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)


# get the nonce.  Prevents one from sending the transaction twice
nonce = web3.eth.get_transaction_count(account_1)
Chain_id = web3.eth.chain_id

# CCIP EVM2EVMOffRamp Contract on destination Chain.
contractAddr = "0xa73bf37f78cd1629ff11fa2b397ced39f49f6efe"  # CCIP EVM2EVMOffRamp Contract on Polygon Change if your destination Chain is different.
# do not need to change ABI, it is same in all chains.
contractABI = [
    {
        "inputs": [
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "uint64",
                                "name": "sourceChainSelector",
                                "type": "uint64",
                            },
                            {
                                "internalType": "uint64",
                                "name": "sequenceNumber",
                                "type": "uint64",
                            },
                            {
                                "internalType": "uint256",
                                "name": "feeTokenAmount",
                                "type": "uint256",
                            },
                            {
                                "internalType": "address",
                                "name": "sender",
                                "type": "address",
                            },
                            {
                                "internalType": "uint64",
                                "name": "nonce",
                                "type": "uint64",
                            },
                            {
                                "internalType": "uint256",
                                "name": "gasLimit",
                                "type": "uint256",
                            },
                            {"internalType": "bool", "name": "strict", "type": "bool"},
                            {
                                "internalType": "address",
                                "name": "receiver",
                                "type": "address",
                            },
                            {"internalType": "bytes", "name": "data", "type": "bytes"},
                            {
                                "components": [
                                    {
                                        "internalType": "address",
                                        "name": "token",
                                        "type": "address",
                                    },
                                    {
                                        "internalType": "uint256",
                                        "name": "amount",
                                        "type": "uint256",
                                    },
                                ],
                                "internalType": "struct Client.EVMTokenAmount[]",
                                "name": "tokenAmounts",
                                "type": "tuple[]",
                            },
                            {
                                "internalType": "address",
                                "name": "feeToken",
                                "type": "address",
                            },
                            {
                                "internalType": "bytes32",
                                "name": "messageId",
                                "type": "bytes32",
                            },
                        ],
                        "internalType": "struct Internal.EVM2EVMMessage[]",
                        "name": "messages",
                        "type": "tuple[]",
                    },
                    {
                        "internalType": "bytes[][]",
                        "name": "offchainTokenData",
                        "type": "bytes[][]",
                    },
                    {
                        "internalType": "bytes32[]",
                        "name": "proofs",
                        "type": "bytes32[]",
                    },
                    {
                        "internalType": "uint256",
                        "name": "proofFlagBits",
                        "type": "uint256",
                    },
                ],
                "internalType": "struct Internal.ExecutionReport",
                "name": "report",
                "type": "tuple",
            },
            {
                "internalType": "uint256[]",
                "name": "gasLimitOverrides",
                "type": "uint256[]",
            },
        ],
        "name": "manuallyExecute",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]



# for send transaction

contract = web3.eth.contract(
    address=Web3.to_checksum_address(contractAddr), abi=contractABI
)

# Just check connection and read some data from contract
callResult = contract.functions.owner().call()
print(callResult)


# Create Transaction, change parameter by your own CCIP tx data. you can find parameter by searching same transaction you want to Manually execute on tenderly.co
# Sample for some transaction that reverted for gas. check this  https://dashboard.tenderly.co/tx/polygon/0x5d7b75e1eb59e7884e5cc4902e8143e8eb0b5b473fa537ee2e534e7a744c96c5
# Change all parameter with you own message. you need to search transaction hash of your CCIP reverted transaction on tenderly
# you should need to change sourceChainSelector, nounce and gasLimitOverrides.
tx = contract.functions.manuallyExecute(
    [
        [
            [
                5009297550715157269,    #sourceChainSelector
                1298,   #sequenceNumber
                336324413442966,    #feeTokenAmount
                Web3.to_checksum_address("0xCCC8170EB01434CA514A6F7A5D9ACEB5BA84DCCC"),     #sender
                1,  #nonce
                200000, #gasLimit
                False,  #strict
                Web3.to_checksum_address("0xCCC8170EB01434CA514A6F7A5D9ACEB5BA84DCCC"), #receiver
                "0x000000000000000000000000FC2BE4522A4E2C4865050F8B595C47EF634C636A0000000000000000000000000B50F2518AC7E963673D2055308DAF4E0BCA08D600000000000000000000000000000000000000000000000000000000000015BE00000000000000000000000000000000000000000000000000000000000000C000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000140000000000000000000000000000000000000000000000000000000000000000B70756E6B7356536170657300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000045076734100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000005D68747470733A2F2F70756E6B737673617065732E6D7970696E6174612E636C6F75642F697066732F516D525673374D79477646734458624347714B6737514D436A37624D566774533834545777586B336762413965522F302F35353636000000",   #data
                [], #tokenAmounts
                Web3.to_checksum_address("0xC02AAA39B223FE8D0A0E5C4F27EAD9083C756CC2"), #feeToken
                "0x178B64062B1A449A92C29927196DE07E5806AE75D718596AC3810D18E5EFC801",   #messageId
            ]
        ],
        [[]],   #offchainTokenData
        [], #proofs
        0,  #proofFlagBits
    ],
    [600000],   #gasLimitOverrides
).build_transaction(
    {"chainId": Chain_id, "from": account_1, "nonce": nonce, "gas": 1000000}
)

# Signe transaction with your wallet
signed_tx = web3.eth.account.sign_transaction(tx, private_key1)
# Send transaction to the RPC
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
# Wait for geting transaction receipt
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)
