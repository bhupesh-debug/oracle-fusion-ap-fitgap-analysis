#!/usr/bin/env python3
"""
generate_ap_synthetic_data.py
Generates realistic synthetic suppliers, purchase orders, AP invoices with
matching types and hold distributions, and payment records for Oracle Fusion Payables testing.
"""

import csv
import os
import random

random.seed(42)
OUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT_DIR, exist_ok=True)

VENDOR_NAMES = [
    "Apex Logistics Solutions", "NexGen Cloud Hosting", "Beacon Industrial Supplies",
    "Pinnacle Facilities Management", "Summit Tech Hardware", "Vanguard Office Interiors",
    "Atlas Strategic Consulting", "Crestview Security Systems", "Quantum Data Analytics",
    "Horizon Global Freight", "Dynamic Packaging Corp", "Matrix Precision Tooling"
]

SUPPLIERS = []
for i in range(1, 51):
    base_name = VENDOR_NAMES[(i - 1) % len(VENDOR_NAMES)]
    SUPPLIERS.append({
        "supplier_id": f"SUP{i:04d}",
        "supplier_name": f"{base_name} - Region {i}",
        "tax_id": f"XX-XXX{i:04d}",
        "payment_terms": random.choice(["Net 30", "Net 60", "2% 10 Net 30"]),
        "payment_method": "Electronic (ACH)",
        "matching_level": random.choice(["2-Way", "3-Way", "3-Way"])
    })

INVOICES = []
total_liability = 0.0

for n in range(1, 301):
    supp = random.choice(SUPPLIERS)
    amount = round(random.uniform(250.0, 125000.0), 2)
    match_level = supp["matching_level"]

    # Assign approval and hold statuses
    if amount < 10000.0:
        approval_status = "Auto-Approved"
        hold_status = "None"
    elif amount < 50000.0:
        approval_status = "Approved by Cost Center Mgr"
        hold_status = "None"
    elif amount < 100000.0:
        approval_status = "Approved by Department VP"
        hold_status = "None"
    else:
        approval_status = "Pending CFO Approval" if random.random() > 0.4 else "Approved by CFO"
        hold_status = "None"

    # Introduce realistic 5% variance holds
    if random.random() < 0.05:
        hold_status = "PRICE HOLD"
        approval_status = "Held - Pending Change Order"
    elif random.random() < 0.03 and match_level == "3-Way":
        hold_status = "QTY REC HOLD"
        approval_status = "Held - Awaiting Warehouse Receipt"

    payment_status = "Unpaid"
    if hold_status == "None" and "Approved" in approval_status and random.random() > 0.3:
        payment_status = "Paid"

    if payment_status != "Paid":
        total_liability += amount

    INVOICES.append({
        "invoice_id": f"INV{n:05d}",
        "invoice_num": f"AP-{2026000 + n}",
        "supplier_id": supp["supplier_id"],
        "supplier_name": supp["supplier_name"],
        "invoice_date": "2026-10-15",
        "amount": amount,
        "currency": "USD",
        "match_level": match_level,
        "approval_status": approval_status,
        "hold_status": hold_status,
        "payment_status": payment_status,
        "gl_account": "101-200-511000-000-000"
    })

total_liability = round(total_liability, 2)


def write_csv(filename, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} records to {filename}")


if __name__ == "__main__":
    write_csv("suppliers.csv", SUPPLIERS)
    write_csv("invoices.csv", INVOICES)
    print(f"Summary: 50 Suppliers, 300 Invoices generated. Net Open AP Liability = ${total_liability:,.2f}")
