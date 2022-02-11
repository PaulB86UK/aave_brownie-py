0. Swap eth for Weth
1.Deposit some ETH into Aave
2.Borrow some asset with the ETH Collateral
    1.Sell that borrowed asset (Short Selling)#
3. Repay Everything back

Integration Test :Kovan
Local Test: ? 
Unit Test: Mainnet - Fork Test

brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1 fork=https://eth-mainnet.alchemyapi.io/v2/JO2aK5_xacHXrC0JQcUU3dQE0R3MhtzT accounts=10 mnemonic=brownie port=8545    