from enum import Enum

from django_tatum.apps.tatum.tatum_client.wallet_generation.crypto_wallets.ethereum import EthereumWallet
from django_tatum.apps.tatum.tatum_client.wallet_generation.crypto_wallets.matic import PolygonMatic
from django_tatum.apps.tatum.tatum_client.wallet_generation.crypto_wallets.solana import SolanaWallet


class WalletType(Enum):
    ETH = "ETH"
    MATIC = "MATIC"
    SOL = "SOL"


# Dictionary mapping enum values to corresponding classes
WALLET_CLASSES = {
    WalletType.ETH: EthereumWallet,
    WalletType.MATIC: PolygonMatic,
    WalletType.SOL: SolanaWallet,
}

# Dictionary mapping enum values to methods in the corresponding classes
WALLET_GENERATE_METHODS = {
    WalletType.ETH: 'generate_ethereum_wallet',
    WalletType.MATIC: 'generate_polygon_wallet',
    WalletType.SOL: 'generate_solana_wallet',

}
