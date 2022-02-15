from click import FloatRange
from scripts.pp_functions import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3

# 0.1
AMOUNT = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()  # this function mints 0.1weth with eth
    lending_pool = get_lending_pool()  # get lending pool address
    approve_tx = approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)
    print("Depositing...")
    tx = lending_pool.deposit(
        erc20_address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("Lets Borrow")
    # DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_to_eth_price_feed"]
    )
    amount_dai_to_borrow = (borrowable_eth * 0.95) / dai_eth_price
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print(" We succesfully borrow some DAI")
    # borrowable -> borrowable DAI * 0.95 (avoid being liquidated)
    print(f"We are going to borrow {amount_dai_to_borrow}")


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)


def get_lending_pool():
    # This part is to get the address of the lending Pool using the contract address of the provider contract
    # lending_pool_addresses_provider is the contract that returns the address
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    # this is the function to store the address
    # function getLendingPool() external view returns (address);

    lending_pool_address = (
        lending_pool_addresses_provider.getLendingPool()
    )  # get lending pool is the "method" inside the provider
    lending_pool = interface.ILendingPool(
        lending_pool_address
    )  # ILendingpool returns the addres of the lending pool
    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 Token")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})  # aprove a transaction
    tx.wait(1)
    print("Approved")
    return tx


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH Deposited.")
    print(f"You have {total_debt_eth} worth of ETH Borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))


# how much deposit, collateral, debt etc we have
# with the get user account data
