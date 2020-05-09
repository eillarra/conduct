import pytest
import uuid

from conduct.wallets import LNbitsWallet, LndHubWallet, LNPayWallet, LntxbotWallet


def short_uuid() -> str:
    return f"conduct_{str(uuid.uuid4())[:8]}"


class TestTransactions:
    """Tests a chain of transactions between wallets."""

    @pytest.mark.parametrize(
        "wallet_class, txid_key, pr_key",
        [
            (LNbitsWallet, "checking_id", "payment_request"),
            # (LndHubWallet, ..., "pay_req"),
            (LNPayWallet, "id", "payment_request"),
            (LntxbotWallet, "payment_hash", "payment_request"),
        ],
    )
    def test_chain(self, wallet_class, txid_key, pr_key):
        data = wallet_class()._create_invoice(amount=10, description=short_uuid())
        assert txid_key in data and isinstance(data[txid_key], str)
        assert pr_key in data and isinstance(data[pr_key], str)
