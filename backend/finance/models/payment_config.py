# finance/models/payment_config.py
from django.db import models

class PaymentConfig(models.Model):
    name = models.CharField(max_length=50, default='Pagarme')
    api_token = models.CharField(max_length=255)
    api_url = models.URLField(help_text="URL da API Pagarme dev. Ex.: https://sdx-api.pagar.me/core/v5/paymentlinks")
    dev_url_hint = models.URLField(
        blank=True, null=True,
        help_text="URL sandbox Pagarme (só informativo). Ex.: https://sdx-api.pagar.me/core/v5/paymentlinks"
    )
    postback_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL que será chamada como webhook."
    )

    redirect_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL para redirecionar o cliente após o pagamento."
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"

