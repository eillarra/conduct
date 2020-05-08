import uuid

from conduct.wallets import LNbitsWallet, LndHubWallet, LNPayWallet, LntxbotWallet


def short_uuid() -> str:
    return f"conduct_{str(uuid.uuid4())[:8]}"


class TestTransactions:
    """Tests a chain of transactions between wallets."""

    def test_chain(self):
        invoice = LNPayWallet().create_invoice(amount=10, description=short_uuid())
        LNbitsWallet().pay_invoice(payment_request=invoice.payment_request)
        invoice = LNbitsWallet().create_invoice(amount=10, description=short_uuid())
        LndHubWallet().pay_invoice(payment_request=invoice.payment_request)
        invoice = LndHubWallet().create_invoice(amount=10, description=short_uuid())
        LntxbotWallet().pay_invoice(payment_request=invoice.payment_request)
        invoice = LntxbotWallet().create_invoice(amount=10, description=short_uuid())
        LNPayWallet().pay_invoice(payment_request=invoice.payment_request)
