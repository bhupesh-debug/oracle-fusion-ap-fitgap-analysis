# Fit-Gap Analysis Matrix: 30 Enterprise Business Requirements

**Application:** Oracle Fusion Cloud Payables (AP) & Procurement  
**Release:** Oracle Cloud Financials 24A/24B  
**Author:** Bhupesh Dimri, Oracle Fusion ERP Functional Consultant  

---

## Classification Taxonomy
- **1. Standard Fit (OOTB):** Standard out-of-the-box Oracle Fusion feature; zero configuration or code needed.
- **2. Configuration:** Standard FSM setup parameters, BPM approval task rules, tolerance tables, or SLA derivation.
- **3. Workaround / Reporting:** Satisfied via operational process adjustment, user procedure, or OTBI real-time dashboard.
- **4. Extension / Gap:** Custom code required (PaaS/OIC, custom database extension, or formal enhancement request).

---

## Master Fit-Gap Requirements Table

| Req # | Business Requirement Description | Classification | Proposed Oracle Fusion Resolution | Owner | Decision / Status |
|---|---|---|---|---|---|
| **REQ-01** | Capture supplier invoices from electronic files and manual entry | Standard Fit | Standard Payables invoice workbench & FBDI import | AP Lead | Adopt Standard |
| **REQ-02** | Automated 3-way matching of physical goods against PO & Receipt | Standard Fit | Configure 3-Way Match level on item and supplier site | AP Lead | Adopt Standard |
| **REQ-03** | 2-way matching for recurring professional services & software licenses | Standard Fit | Configure 2-Way Match level on service purchase categories | AP Lead | Adopt Standard |
| **REQ-04** | Prevent duplicate invoice entry by supplier, invoice number, and amount | Standard Fit | Standard duplicate invoice checking enabled in Payables Options | AP Lead | Adopt Standard |
| **REQ-05** | Enforce multi-tier managerial approvals based on invoice total amount | Configuration | BPM Worklist approval task rules using amount hierarchy | Functional Lead | Configured in FSM |
| **REQ-06** | Route invoices to Department Cost Center Manager for expense sign-off | Configuration | BPM rule routing based on `InvoiceLine.costCenter` segment | Functional Lead | Configured in FSM |
| **REQ-07** | Automatic hold on invoices exceeding PO unit price by more than 2% | Configuration | Configure *Invoice Tolerances* table: 2% price variance threshold | AP Lead | Configured in FSM |
| **REQ-08** | Automatic hold when billed quantity exceeds received quantity | Standard Fit | Standard `QTY ORD` and `QTY REC` system hold rules | AP Lead | Adopt Standard |
| **REQ-09** | Electronic payment batch creation via NACHA ACH format | Standard Fit | Standard Oracle Payments NACHA payment process profile | Treasury Lead | Adopt Standard |
| **REQ-10** | Electronic payment file generation in ISO20022 XML format | Standard Fit | Standard Oracle Payments ISO20022 payment template | Treasury Lead | Adopt Standard |
| **REQ-11** | Automatic early payment discount calculation based on Net 10 / 2% Terms | Standard Fit | Standard Payment Terms definition with discount dates | AP Lead | Adopt Standard |
| **REQ-12** | Ability to place ad-hoc manual holds on invoices pending dispute | Standard Fit | Standard *Apply Hold* task with configurable hold reasons | AP Specialist | Adopt Standard |
| **REQ-13** | Segregation of Duties: invoice creator cannot approve or pay invoice | Standard Fit | Standard Oracle Cloud Role-Based Access Control (RBAC) | Security Admin | Adopt Standard |
| **REQ-14** | Prepayment tracking and automated application against final invoices | Standard Fit | Standard Prepayment invoice type and Apply Prepayment task | AP Specialist | Adopt Standard |
| **REQ-15** | Withholding tax calculation and reporting for 1099 contractors | Standard Fit | Standard Oracle Fusion Tax withholding configuration | Tax Lead | Adopt Standard |
| **REQ-16** | Daily notification digest to procurement buyers for open invoice holds | Workaround / Report | Automated OTBI scheduled agent alert delivering daily email | Procurement Lead | Report Configured |
| **REQ-17** | Supplier self-service portal to view invoice status and payment dates | Standard Fit | Standard Oracle Fusion Supplier Portal cloud service | Vendor Relations | Adopt Standard |
| **REQ-18** | Automated monthly subledger-to-GL liability balance reconciliation | Standard Fit | Standard *Subledger to GL Reconciliation Report* & OTBI | Financial Controller | Adopt Standard |
| **REQ-19** | Subledger Accounting derivation of expense account from PO charge line | Standard Fit | Standard SLA Journal Line Rule for Payables Invoices | Functional Lead | Adopt Standard |
| **REQ-20** | Enforce mandatory Purchase Order number on all invoices over $2,500 | Configuration | BPM workflow rule rejecting non-PO invoices exceeding $2,500 | AP Lead | Configured in FSM |
| **REQ-21** | Foreign currency invoice entry with automated exchange rate conversion | Standard Fit | Standard daily corporate exchange rate integration | Treasury Lead | Adopt Standard |
| **REQ-22** | Ability to sweep unapproved/unaccounted invoices to next month during close | Standard Fit | Standard *Payables Unaccounted Transactions Sweep* process | AP Manager | Adopt Standard |
| **REQ-23** | Capture freight and miscellaneous charges at the invoice line level | Standard Fit | Standard Freight and Miscellaneous invoice line types | AP Specialist | Adopt Standard |
| **REQ-24** | Automated email remittance advice dispatch upon payment confirmation | Standard Fit | Standard *Send Separate Remittance Advice* scheduled process | Treasury Lead | Adopt Standard |
| **REQ-25** | Urgent payment processing out of scheduled cycle with manual check printing | Standard Fit | Standard Quick Payment task with local check formatting | AP Specialist | Adopt Standard |
| **REQ-26** | Audit trail of all invoice approval comments, timestamps, and rejections | Standard Fit | Standard BPM Transaction Console and approval audit logs | Internal Audit | Adopt Standard |
| **REQ-27** | Custom legacy field for external freight forwarder customs clearance code | Configuration | Standard Descriptive Flexfield (DFF) on invoice header | Functional Lead | Configured in FSM |
| **REQ-28** | Real-time AP aging report grouped by supplier payment terms | Workaround / Report | Standard OTBI Payables Invoices Real Time Subject Area query | AP Manager | Report Configured |
| **REQ-29** | Automated notification when a supplier's banking information changes | Workaround / Report | OTBI audit alert on `POZ_SUPPLIER_BANK_ACCOUNTS` updates | Risk & Controls | Report Configured |
| **REQ-30** | Real-time automated voice verification of supplier bank accounts | Extension / Gap | External third-party telephony integration (non-standard) | Executive Sponsor | **Rejected / Deferred** |
