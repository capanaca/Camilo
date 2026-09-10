# Wallet Transaction Tracker

Rastrea tus gastos de billetera/banco a partir de los correos de notificación
que ya recibes en Gmail (Bancolombia, Mercado Pago, Bold, Santander), los
organiza mes a mes por categoría, y genera un reporte mensual junto con un
resumen histórico comparable entre meses.

No usa un scraper ni credenciales de banco: solo lee los mismos correos de
notificación transaccional que el banco/wallet ya te envía por cada
movimiento.

## Cómo funciona

1. **Extracción**: se buscan en Gmail los correos de los remitentes
   transaccionales conocidos, dentro de un rango de fechas, y se exportan a
   un JSON crudo (`id`, `threadId`, `date`, `sender`, `subject`,
   `plaintextBody`).
2. **Parseo** (`wallettracker/parsers/`): cada remitente tiene un parser
   dedicado que reconoce sus plantillas de texto (compra aprobada/rechazada,
   retiro en cajero, transferencia recibida, pago de nómina, pago de tarjeta
   de crédito) y extrae monto, fecha, comercio/contraparte y estado.
3. **Categorización** (`wallettracker/categorize.py`): reglas por
   palabra clave sobre el nombre del comercio, configurables en
   `config/categories.json` (genérico, va al repo) y
   `config/categories.local.json` (tus comercios reales, no se commitea).
4. **Almacenamiento** (`wallettracker/storage.py`): SQLite local
   (`data/transactions.db`, no se commitea), deduplicado por el id del
   correo — correr la ingesta varias veces sobre el mismo mes es seguro.
5. **Reporte** (`wallettracker/report.py`): genera un Markdown mensual
   (`reports/YYYY-MM.md`) con ingresos, gastos, neto, desglose por categoría
   y por fuente, top 10 gastos, y comparación contra el mes anterior. También
   mantiene `data/monthly_summary.json` como histórico acumulado mes a mes.

Los pagos de tarjeta de crédito (transferir de tu cuenta a tu propia tarjeta)
se muestran aparte y **no** se suman como gasto nuevo, porque la compra
original ya quedó contabilizada cuando ocurrió. Las transacciones rechazadas
se listan pero tampoco se contabilizan.

## Extracto de tarjeta de crédito (fuente adicional)

Bancolombia solo envía una notificación por correo de las compras hechas a
través de Mercado Pago o Bold — el resto de tu compras con tarjeta de
crédito (Uber, Rappi, restaurantes, tiendas, etc.) no generan un correo
individual, solo aparecen en el extracto mensual PDF que Bancolombia envía
(remitente `extractosbancolombia@extractos.documentosbancolombia.com`,
asunto "¡Toc-toc! Llegó tu extracto del mes"), protegido con tu cédula/NIT.

`scripts/ingest_statement_pdf.py` descifra ese PDF y extrae cada movimiento
del detalle ("Detalle del movimiento"). Como el extracto es la fuente más
completa, cuando lo ingieres **reemplaza** cualquier compra ya cargada por
correos de Mercado Pago/Bold/Bancolombia que caiga en el mismo rango de
fechas, para no contar la misma compra dos veces.

```bash
pip install -r requirements-statement.txt
python scripts/ingest_statement_pdf.py extracto.pdf TU_CEDULA_O_NIT 4491
python scripts/make_report.py 2026-08
```

Requiere `pikepdf` y `pdfplumber` (no están en la dependencia base del
proyecto, que es solo librería estándar). El PDF y la contraseña no se
commitean — igual que el resto de `data/raw/`.

## Remitentes reconocidos hoy

| Fuente | Remitente | Qué detecta |
|---|---|---|
| Bancolombia | `alertasynotificaciones@bancolombia.com.co` | compra aprobada/rechazada en tarjeta de crédito, retiro en cajero, retiro Fiducuenta, pago de nómina recibido, transferencia recibida, pago de tarjeta de crédito |
| Mercado Pago | `info@mercadopago.com` / `no-responder@mercadopago.com` | pago aprobado/rechazado, confirmación "ya recibió tu pago" |
| Bold | `no-responder@bold.co` | transacción aprobada/rechazada |
| Santander (Chile) | `mensajeria@santander.cl` | transferencia de fondos recibida |

Agregar un nuevo remitente es crear un módulo en `wallettracker/parsers/`
con `matches(sender)` y `parse(raw_email) -> Transaction | None`, y
registrarlo en `wallettracker/parsers/__init__.py`.

## Uso manual

```bash
# 1. Exporta los correos del mes a un JSON (ver "Cómo obtener el JSON" abajo)
# 2. Ingiere ese JSON al ledger local
python scripts/ingest.py data/raw/2026-09.json

# 3. Genera el reporte del mes + actualiza el resumen histórico
python scripts/make_report.py 2026-09
```

### Cómo obtener el JSON de correos

Dentro de una sesión de Claude Code con Gmail conectado, pide algo como:

> Busca en Gmail los correos de alertasynotificaciones@bancolombia.com.co,
> info@mercadopago.com, no-responder@bold.co y mensajeria@santander.cl entre
> el 1 y el 30 de septiembre de 2026, trae el cuerpo en texto plano de cada
> uno, y guárdalos como data/raw/2026-09.json con los campos id, threadId,
> date, sender, subject, plaintextBody.

Luego corre `ingest.py` y `make_report.py` como arriba.

## Reporte de fin de mes automático

Este repo puede combinarse con una Rutina (trigger) mensual de Claude Code
que: reconecta el acceso a Gmail, trae los correos nuevos del mes que
termina, corre `ingest.py` + `make_report.py`, y te envía el reporte. Pídele
a Claude que la configure si quieres esta automatización.

## Pruebas

```bash
python -m pytest tests/
```

Los fixtures de test usan la misma redacción real de las plantillas de cada
banco/wallet, pero con montos y nombres de comercio ficticios — así no hay
datos personales en el repo.
