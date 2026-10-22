# BPM Worklist Invoice Approval Rules Specification

**Application:** Oracle Fusion Cloud Payables  
**Workflow Engine:** Oracle Business Process Management (BPM) Worklist  
**Task Code:** `FinApInvoiceApproval`  

---

## 1. Approval Hierarchy Matrix

```
[Invoice Validated]
        │
        ▼
Is Total < $10,000 AND 3-Way Matched? ──► YES ──► Auto-Approve (System)
        │
        ▼ NO
Is Total between $10,000 and $49,999.99? ─► Route to Cost Center Manager (Tier 1)
        │
        ▼ NO
Is Total between $50,000 and $99,999.99? ─► Route to Department VP (Tier 2)
        │
        ▼ NO
Is Total >= $100,000? ────────────────────► Route to Chief Financial Officer (Tier 3)
```

---

## 2. Rule Definitions & Logic

### Rule 1: Auto-Approval for Clean Matched Invoices (`RULE_AUTO_APPROVE`)
- **Condition:**
  ```xpath
  InvoiceHeader.invoiceAmount < 10000.00 and
  InvoiceHeader.validationStatus == "VALIDATED" and
  InvoiceHeader.hasHolds == "N" and
  InvoiceHeader.matchedToPO == "Y"
  ```
- **Action:** `AUTO_APPROVE` (Bypasses human routing).

### Rule 2: Cost Center Manager Routing (`RULE_TIER1_CC_MGR`)
- **Condition:**
  ```xpath
  InvoiceHeader.invoiceAmount >= 10000.00 and InvoiceHeader.invoiceAmount < 50000.00
  ```
- **Action:** Route approval task to `GetManager("CostCenter", InvoiceLine.costCenterSegment)`.

### Rule 3: Department Vice President (`RULE_TIER2_VP`)
- **Condition:**
  ```xpath
  InvoiceHeader.invoiceAmount >= 50000.00 and InvoiceHeader.invoiceAmount < 100000.00
  ```
- **Action:** Route approval task sequentially to Cost Center Manager $\rightarrow$ Department VP.

### Rule 4: CFO / Executive Sign-Off (`RULE_TIER3_CFO`)
- **Condition:**
  ```xpath
  InvoiceHeader.invoiceAmount >= 100000.00
  ```
- **Action:** Route approval task sequentially to Cost Center Manager $\rightarrow$ Department VP $\rightarrow$ Chief Financial Officer (`CFO_APPROVER_GROUP`).

---

## 3. Fallback & Timeout Policies
- **Fallback Approver:** If a Cost Center Manager position is vacant or lacking an active user in HCM, route automatically to `AP_SUPERVISOR_QUEUE`.
- **Escalation SLA:** If an approval task is unaddressed after 48 business hours, send automated reminder; escalate to supervisor after 72 hours.
