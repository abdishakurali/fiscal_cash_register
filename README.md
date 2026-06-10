# Fiscal Cash Register Integration (Romania) — Odoo 19

[![Odoo 19](https://img.shields.io/badge/Odoo-19.0-purple)](https://odoo.com)
[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

Professional Odoo bridge for physical fiscal printers using the [FiscalNet.ro](https://fiscalnet.ro) driver. Automates receipt printing, Z-reports, and legal cash book reporting for Romanian businesses.

## Features

- 🖨️ **Fiscal Receipt Printing** — automatic receipt generation after every POS sale via FiscalNet API
- 📊 **Z-Report** — daily fiscal closure report directly from the POS closing popup
- 📒 **Registrul de Casă** — Romanian legal cash book (opening balance, cash in/out, closing balance)
- 💵 **Cash In / Cash Out** — tracked cash operations with fiscal log
- 🏷️ **SGR Support** — Romanian ecological deposit (Sistemul de Garanție-Returnare) product handling
- 🖥️ **Local File or API** — choose between local file download or direct FiscalNet REST API integration
- 🏢 **Multi-printer support** — Datecs, Daisy, Olivetti, Tremol, and all FiscalNet-compatible devices

## Compatibility

| Odoo Version | Branch  | Status     |
|---|---|---|
| 19.0         | `19.0`  | ✅ Active  |
| 17.0         | `17.0`  | Legacy     |

## Installation

1. Add this repo to your Odoo addons path
2. Install the `fiscal_cash_register` module from Apps
3. Configure the fiscal printer in POS → Configuration → Point of Sales → My Company

## Configuration

| Field | Description |
|---|---|
| Enable Fiscal Printer | Toggle fiscal printer integration |
| Fiscal Integration Method | `Local File` or `FiscalNet API` |
| FiscalNet API Endpoint | e.g. `http://localhost:65400/api/Receipt` |
| FiscalNet OS Type | Windows or Android |
| Fiscal Files Directory | Output directory for local file mode |

## Odoo.sh Setup

1. Create a new Odoo.sh project
2. Connect this GitHub repository
3. The `fiscal_cash_register` module will be discovered automatically

## Author

**Franchise Tech** — [franchisetech.ro](https://franchisetech.ro)

## License

LGPL-3 — see [LICENSE](https://www.gnu.org/licenses/lgpl-3.0) for details.
