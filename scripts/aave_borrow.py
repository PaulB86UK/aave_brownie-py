from scripts.pp_functions import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth


def main():
    account = get_account()
    erc2_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active in ["mainnet-fork"]:
        get_weth()
    lending_pool = get_lending_pool()


def get_lending_pool():
    # This part is to get the address of the lending Pool
    # lending_pool_addresses_provider is the contract that returns the address
    lending_pool_addresses_provider = interface.IlendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    # this is the function to store the address
    # function getLendingPool() external view returns (address);

    lending_pool_addresses = lending_pool_addresses_provider.getLendingPool()

    # abi

    # adress check!
