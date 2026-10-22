# Functional Process Design: Invoice-to-Pay Lifecycle

**Application:** Oracle Fusion Cloud Payables (AP)  
**Enterprise:** `CORP_GLOBAL_HOLDINGS`  
**Business Unit:** `US_COMMERCIAL_BU`  

---

## 1. Common Options for Payables & Procurement
Configured in Functional Setup Manager (FSM) under *Manage Common Options for Payables and Procurement*:
- **Business Unit:** `US_COMMERCIAL_BU`
- **Liability Account:** `101-000-211000-000-000` (AP Trade Payables Control Account)
- **Prepayment Account:** `101-000-145000-000-000` (Prepaid Expenses)
- **Conversion Rate Type:** `Corporate`
- **Expense Accrual:** *At Receipt* for inventory items; *Period End* for expense lines.
- **Discount Distribution Method:** *Prorate Expense* or *System Account* (Configured to Account `491000` Discounts Taken).

---

## 2. Invoice Matching & Tolerance Architecture

### 2.1 Matching Rules
1. **2-Way Match:**
   - *Condition:* Quantity Billed $\le$ Quantity Ordered; Unit Price Billed $\le$ PO Unit Price.
   - *Use Case:* IT subscriptions, legal fees, facility maintenance.
2. **3-Way Match:**
   - *Condition:* Quantity Billed $\le$ Quantity Received; Unit Price Billed $\le$ PO Unit Price.
   - *Use Case:* Tangible inventory, warehouse stock, physical hardware assets.

### 2.2 Configured Invoice Tolerances Table
| Tolerance Type | Threshold Value | Hold Placed Upon Breach | Resolution Action |
|---|---|---|---|
| **Price Variance (%)** | `2.0%` | `PRICE HOLD` | Issue PO Change Order or Supplier Credit Memo |
| **Price Variance (Amount)** | `$50.00` | `PRICE HOLD` | Issue PO Change Order or Supplier Credit Memo |
| **Quantity Variance (%)** | `0.0%` | `QTY REC HOLD` | Warehouse staff must enter Goods Receipt |
| **Line Amount Variance** | `$0.05` | `LINE VARIANCE` | Adjust distribution penny rounding in Payables |

---

## 3. Payment Processing Architecture
- **Payment Method:** Electronic Funds Transfer (ACH) & ISO20022 SEPA/XML.
- **Payment Process Profile (PPP):** `CORP_ELECTRONIC_ACH`
  - *Disbursement Bank Account:* JPMorgan Chase Operating Checking (`...4892`)
  - *Format:* NACHA Generic Standard Format
  - *Batch Booking:* Group invoices by supplier site to minimize wire fees.
