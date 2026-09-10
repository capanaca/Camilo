import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from wallettracker.parsers import parse_email
from wallettracker.models import DIRECTION_EXPENSE, DIRECTION_INCOME, DIRECTION_INTERNAL, DIRECTION_EXCLUDED

# Fixtures mirror the real notification wording/structure observed in the
# user's inbox, with merchant names, amounts and card numbers replaced by
# synthetic values so no personal data lives in the repo.


def _email(sender, subject, body, msg_id="m1", date="2026-01-15T12:00:00Z"):
    return {
        "id": msg_id,
        "threadId": msg_id,
        "date": date,
        "sender": sender,
        "subject": subject,
        "plaintextBody": body,
    }


def test_bancolombia_retiro():
    txn = parse_email(_email(
        "alertasynotificaciones@bancolombia.com.co",
        "Alertas y Notificaciones",
        "Bancolombia: Retiraste $200.000,00 en CAJERO CENTRO de tu T.Deb **9999 el 15/01/2026 a las 09:00.",
    ))
    assert txn.kind == "retiro"
    assert txn.direction == DIRECTION_EXPENSE
    assert txn.amount == 200000.0
    assert "CAJERO CENTRO" in txn.counterparty


def test_bancolombia_nomina():
    txn = parse_email(_email(
        "alertasynotificaciones@bancolombia.com.co",
        "Alertas y Notificaciones",
        "Bancolombia: Recibiste un pago de Nomina de EMPRESA DEMO SA por $4,000,000.00 en tu cuenta de Ahorros el 15/01/2026 a las 12:00.",
    ))
    assert txn.kind == "nomina"
    assert txn.direction == DIRECTION_INCOME
    assert txn.amount == 4000000.0


def test_bancolombia_transferencia_recibida():
    txn = parse_email(_email(
        "alertasynotificaciones@bancolombia.com.co",
        "Alertas y Notificaciones",
        "Bancolombia: Recibiste una transferencia por $50,000 de JUAN PEREZ en tu cuenta **1234, el 15/01/2026 a las 08:00.",
    ))
    assert txn.kind == "transferencia_recibida"
    assert txn.direction == DIRECTION_INCOME
    assert txn.amount == 50000.0


def test_bancolombia_pago_tarjeta_credito():
    txn = parse_email(_email(
        "alertasynotificaciones@bancolombia.com.co",
        "Alertas y Notificaciones",
        "Bancolombia le informa Pago de Tarjeta de Credito por $300,000 desde cta *1111 a la tarjeta *2222. 15/01/2026 10:00.",
    ))
    assert txn.kind == "pago_tarjeta_credito"
    assert txn.direction == DIRECTION_INTERNAL


def test_bancolombia_pago_tarjeta_credito_variante_pagaste():
    txn = parse_email(_email(
        "alertasynotificaciones@bancolombia.com.co",
        "Alertas y Notificaciones",
        "Bancolombia: Pagaste $500,000 en la tarjeta de credito *1234 desde la cuenta *5678, el 15/01/2026 10:00.",
    ))
    assert txn.kind == "pago_tarjeta_credito"
    assert txn.direction == DIRECTION_INTERNAL
    assert txn.amount == 500000.0


def test_bancolombia_compra_moneda_extranjera():
    txn = parse_email(_email(
        "alertasynotificaciones@bancolombia.com.co",
        "Alertas y Notificaciones",
        "Bancolombia: Compraste USD45,30 en TIENDA EXTRANJERA con tu T.Cred *4491, el 15/01/2026 a las 10:00.",
    ))
    assert txn.kind == "compra"
    assert txn.direction == DIRECTION_EXPENSE
    assert txn.currency == "USD"
    assert txn.amount == 45.30
    assert "TIENDA EXTRANJERA" in txn.counterparty


def test_bancolombia_compra_rechazada():
    txn = parse_email(_email(
        "alertasynotificaciones@bancolombia.com.co",
        "Alertas y Notificaciones",
        "tu compra en TIENDA DEMO por COP99.000,00 no fue exitosa, el cupo de tu T.Credito *3333 "
        "no se afecto. 07:08.29/05/2026.¿Dudas?",
    ))
    assert txn.kind == "compra_rechazada"
    assert txn.direction == DIRECTION_EXCLUDED
    assert txn.date == "2026-05-29"


def test_bancolombia_second_sender_domain_recognized():
    txn = parse_email(_email(
        "alertasynotificaciones@an.notificacionesbancolombia.com",
        "Alertas y Notificaciones",
        "Bancolombia: Compraste COP50.000,00 en TIENDA DEMO con tu T.Cred *4491, el 15/01/2026 a las 10:00.",
    ))
    assert txn is not None
    assert txn.kind == "compra"
    assert txn.amount == 50000.0


def test_bancolombia_compra_suscripcion_sin_tarjeta():
    txn = parse_email(_email(
        "alertasynotificaciones@an.notificacionesbancolombia.com",
        "Alertas y Notificaciones",
        "Bancolombia: Compraste COP20.900,00 en GOOGLE YouTube, el 15/01/2026 a las 17:33. "
        "Esta compra esta asociada a T.Cred *4491.",
    ))
    assert txn.kind == "compra"
    assert txn.amount == 20900.0
    assert txn.counterparty == "GOOGLE YouTube"


def test_bancolombia_transferencia_enviada_a_cuenta():
    txn = parse_email(_email(
        "alertasynotificaciones@an.notificacionesbancolombia.com",
        "Alertas y Notificaciones",
        "Bancolombia: Transferiste $200000.00 desde tu cuenta *7808 a la cuenta *3155313578 "
        "el 09/09/26 a las 19:54. ¿Dudas?",
    ))
    assert txn.kind == "transferencia_enviada"
    assert txn.direction == DIRECTION_EXPENSE
    assert txn.amount == 200000.0
    assert txn.date == "2026-09-09"


def test_bancolombia_transferencia_enviada_a_llave():
    txn = parse_email(_email(
        "alertasynotificaciones@an.notificacionesbancolombia.com",
        "Alertas y Notificaciones",
        "Bancolombia: CAMILO, transferiste $79233.00 a la llave @alguienmas desde tu cuenta *7808 "
        "a Colombia a traves de Transfiya.",
    ))
    assert txn.kind == "transferencia_enviada"
    assert txn.direction == DIRECTION_EXPENSE
    assert txn.amount == 79233.0


def test_bancolombia_pago_qr():
    txn = parse_email(_email(
        "alertasynotificaciones@an.notificacionesbancolombia.com",
        "Alertas y Notificaciones",
        "Bancolombia: CAMILO HERNANDEZ SANCHEZ pagaste $27000.00 por codigo QR desde tu cuenta *7808 "
        "a la llave 0091234.",
    ))
    assert txn.kind == "pago_qr"
    assert txn.direction == DIRECTION_EXPENSE
    assert txn.amount == 27000.0


def test_bancolombia_uses_transaction_date_not_email_arrival_date():
    """A transaction made late at night in Colombia (UTC-5) can be emailed
    after midnight UTC the next day; the body's own date must win so the
    transaction isn't misfiled into the following day/month."""
    txn = parse_email(_email(
        "alertasynotificaciones@an.notificacionesbancolombia.com",
        "Alertas y Notificaciones",
        "Bancolombia: Compraste COP10.000,00 en TIENDA NOCTURNA con tu T.Cred *4491, "
        "el 31/08/2026 a las 23:50.",
        date="2026-09-01T04:50:00Z",
    ))
    assert txn.date == "2026-08-31"


def test_mercadopago_aprobado():
    txn = parse_email(_email(
        "info@mercadopago.com",
        "Pago aprobado en TIENDA DEMO S.A.",
        "Hola, CAMILO Le compraste a TIENDA DEMO S.A. Tu pago fue aprobado Pagaste $ 150.000 Bancolombia Crédito **** 4491 1 cuota de $ 150.000",
    ))
    assert txn.kind == "compra"
    assert txn.direction == DIRECTION_EXPENSE
    assert txn.amount == 150000.0
    assert txn.counterparty == "TIENDA DEMO S.A."


def test_mercadopago_rechazado():
    txn = parse_email(_email(
        "info@mercadopago.com",
        "Pago rechazado en TIENDA DEMO S.A.",
        "Intentaste pagarle a TIENDA DEMO S.A. Tu pago fue rechazado Medio de pago usado Bancolombia Crédito **** 4491 $ 150.000",
    ))
    assert txn.direction == DIRECTION_EXCLUDED
    assert txn.amount == 150000.0


def test_bold_aprobada():
    txn = parse_email(_email(
        "no-responder@bold.co",
        "Compra por $300.000 COP en TIENDA DEMO",
        "Transacción aprobada Resumen de tu compra: $300.000 COP 2026/01/15 11:00:00 Comercio TIENDA DEMO Método de pago 549158******4491 ID Transacción Bold ABC123",
    ))
    assert txn.kind == "compra"
    assert txn.direction == DIRECTION_EXPENSE
    assert txn.amount == 300000.0
    assert txn.counterparty == "TIENDA DEMO"


def test_bold_rechazada():
    txn = parse_email(_email(
        "no-responder@bold.co",
        "Transaccion Rechazada",
        "Transacción rechazada Resumen: 300.000 COP Comercio TIENDA DEMO Referencia de compra LNK_DEMO ID transaccion Bold ABC123",
    ))
    assert txn.direction == DIRECTION_EXCLUDED


def test_santander_transferencia():
    txn = parse_email(_email(
        "mensajeria@santander.cl",
        "Comprobante Transferencia de fondos",
        "Te informamos que, con fecha 15/01/2026, nuestro cliente MARIA DEMO realizó una transferencia a tu cuenta. Monto transferido $ 10.000",
    ))
    assert txn.kind == "transferencia_recibida"
    assert txn.direction == DIRECTION_INCOME
    assert txn.amount == 10000.0
    assert txn.currency == "CLP"


def test_unrecognized_marketing_email_returns_none():
    txn = parse_email(_email(
        "ofertas@a.mercadopago.com",
        "¡Compra a cuotas sin interés!",
        "Aprovecha nuestras promociones.",
    ))
    assert txn is None
