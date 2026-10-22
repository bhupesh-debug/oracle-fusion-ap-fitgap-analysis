-- ============================================================================
-- ORACLE FUSION PAYABLES (AP): SUBLEDGER TIE-OUT & HOLD RECONCILIATION SUITE
-- Target Enterprise: CORP_GLOBAL_HOLDINGS
-- Purpose: Verify AP subledger liability against GL Account 211000,
--          audit active system holds, and verify 3-way matching tolerances.
-- ============================================================================

-- 1. SUBLEDGER TO GENERAL LEDGER LIABILITY BALANCE TIE-OUT
-- Compares total open unpaid invoice liabilities in AP against GL Account 211000.
WITH ap_liability AS (
    SELECT 
        ai.org_id,
        ai.invoice_currency_code,
        SUM(ai.invoice_amount - COALESCE(ai.amount_paid, 0)) AS subledger_open_liability
    FROM ap_invoices_all ai
    WHERE ai.payment_status_flag <> 'Y' -- Unpaid or Partially Paid
      AND ai.wfapproval_status = 'WFAPPROVED'
    GROUP BY ai.org_id, ai.invoice_currency_code
),
gl_liability AS (
    SELECT 
        gcc.segment1 AS company,
        SUM(gb.end_balance_cr - gb.end_balance_dr) AS gl_ending_balance
    FROM gl_balances gb
    JOIN gl_code_combinations gcc ON gb.code_combination_id = gcc.code_combination_id
    WHERE gcc.segment3 = '211000' -- Accounts Payable Trade
      AND gb.period_name = 'OCT-26'
    GROUP BY gcc.segment1
)
SELECT 
    ap.org_id,
    ap.subledger_open_liability,
    gl.gl_ending_balance,
    ROUND(ap.subledger_open_liability - gl.gl_ending_balance, 2) AS reconciliation_variance
FROM ap_liability ap
CROSS JOIN gl_liability gl;

-- 2. AUDIT INVOICES STUCK ON SYSTEM HOLDS BLOCKING PAYMENT DISBURSEMENT
SELECT 
    ai.invoice_num,
    ai.invoice_date,
    ai.invoice_amount,
    ai.vendor_id,
    ah.hold_lookup_code,
    ah.hold_reason,
    ah.hold_date,
    ah.status_flag
FROM ap_invoices_all ai
JOIN ap_holds_all ah ON ai.invoice_id = ah.invoice_id
WHERE ah.status_flag = 'H' -- Active Hold
ORDER BY ai.invoice_amount DESC;

-- 3. SUMMARY OF PRICE VARIANCE VS. QUANTITY VARIANCE HOLDS
SELECT 
    ah.hold_lookup_code,
    COUNT(*) AS hold_count,
    SUM(ai.invoice_amount) AS total_held_exposure
FROM ap_holds_all ah
JOIN ap_invoices_all ai ON ah.invoice_id = ai.invoice_id
WHERE ah.status_flag = 'H'
GROUP BY ah.hold_lookup_code;
