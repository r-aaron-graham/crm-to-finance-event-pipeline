"""Tests for the CRM to finance event pipeline."""

from __future__ import annotations

import asyncio

import events
import pipeline


def test_mapping_and_idempotency() -> None:
    ledger = pipeline.FinanceLedger()
    crm_pipeline = pipeline.CRMPipeline(ledger)
    events_list = [
        events.CustomerCreatedEvent(id="1", customer_id="C001", name="Test", email="t@example.com"),
        events.InvoiceCreatedEvent(id="2", invoice_id="I001", customer_id="C001", amount=50.0),
        events.PaymentReceivedEvent(id="3", payment_id="P001", invoice_id="I001", amount=50.0),
        # Duplicate invoice event
        events.InvoiceCreatedEvent(id="2", invoice_id="I001", customer_id="C001", amount=50.0),
    ]

    asyncio.run(crm_pipeline.run(events_list))
    assert len(ledger.transactions) == 3
    ids = [tx.id for tx in ledger.transactions]
    assert "inv-I001" in ids
    assert "pay-P001" in ids
    assert "cust-C001" in ids