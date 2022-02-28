from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    # Get current blockchain account
    account = get_account()
    # Deploy lottery
    lottery = Lottery.deploy(
        # Get address of MockV3Aggregator
        get_contract("eth_usd_price_feed").address,
        # Get address of VRFCoordinatorMock
        get_contract("vrf_coordinator").address,
        # Get address of LinkToken Mock
        get_contract("link_token").address,
        # Get fee value from active network
        config["networks"][network.show_active()]["fee"],
        # Get keyhash from active network
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        # Enable publish_source if the network is a testnet
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery!")
    return lottery


def start_lottery():
    # Get current account
    account = get_account()
    # Get the last contract and save in lottery var
    lottery = Lottery[-1]
    # Start lottery
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started!")


def enter_lottery():
    # Get current account
    account = get_account()
    # Get the last contract and save in lottery var
    lottery = Lottery[-1]
    # Get lottery entrance fee and add 100000000 gwei
    value = lottery.getEntranceFee() + 100000000
    # Fund the contract
    # Enter in a lottery with entrance fee + 1000000wei
    tx = lottery.enter({"from": account, "value": value})
    # Wait 1 second before transaction
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    # Get current account
    account = get_account()
    # Get the last contract and save in lottery var
    lottery = Lottery[-1]
    # fund the contract
    # then end the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
