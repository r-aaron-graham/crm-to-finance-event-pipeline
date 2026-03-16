"""Core pipeline logic for syncing CRM events to finance transactions."""

from __future__ import annotations

import asyncio
from typing import Iterable, List, Set

from events import (
    CRMEvent,
    CustomerCreatedEvent,
    InvoiceCreatedEvent,
    PaymentReceivedEvent,
    FinanceTransaction,
)


class FinanceLedger:
    """In‑memory ledger representing a finance system."""

    def __init__(self) -> None:
        self.transactions: List[FinanceTransaction] = []

    async def write_transaction(self, tx: FinanceTransaction) -> None:
        # In a real system this would persist to a database or API.
        await asyncio.sleep(0)  # Yield control to simulate async I/O
        self.transactions.append(tx)


class CRMPipeline:
    """Pipeline that processes CRM events and writes them to the finance ledger."""

    def __init__(self, ledger: FinanceLedger) -> None:
        self.ledger = ledger
        self.processed_event_ids: Set[str] = set()

    async def process_event(self, event: CRMEvent) -> None:
        """Process a single CRM event, converting it into a finance transaction if needed."""
        if event.id in self.processed_event_ids:
            # Idempotent processing: skip events we've already handled
            return
        self.processed_event_ids.add(event.id)

        tx: FinanceTransaction | None = None
        if isinstance(event, InvoiceCreatedEvent):
            tx = FinanceTransaction(
                id=f"inv-{event.invoice_id}",
                customer_id=event.customer_id,
                invoice_id=event.invoice_id,
                amount=event.amount,
                description=f"Invoice created: {event.invoice_id}",
            )
        elif isinstance(event, PaymentReceivedEvent):
            tx = FinanceTransaction(
                id=f"pay-{event.payment_id}",
                invoice_id=event.invoice_id,
                amount=-event.amount,
                description=f"Payment received: {event.payment_id}",
            )
        elif isinstance(event, CustomerCreatedEvent):
            # For a customer creation, we might not create a transaction but could record a memo
            tx = FinanceTransaction(
                id=f"cust-{event.customer_id}",
                customer_id=event.customer_id,
                amount=0.0,
                description=f"Customer created: {event.name}",
            )

        if tx:
            await self.ledger.write_transaction(tx)

    async def run(self, events: Iterable[CRMEvent]) -> None:
        """Process a sequence of events sequentially."""
        for event in events:
            await self.process_event(event)


async def main() -> None:
    """Example usage of the pipeline with mock events."""
    ledger = FinanceLedger()
    pipeline = CRMPipeline(ledger)
    events: List[CRMEvent] = [
        CustomerCreatedEvent(id="e1", customer_id="C001", name="Alice", email="alice@example.com"),
        InvoiceCreatedEvent(id="e2", invoice_id="I001", customer_id="C001", amount=100.0),
        PaymentReceivedEvent(id="e3", payment_id="P001", invoice_id="I001", amount=100.0),
        # Duplicate event to test idempotency
        InvoiceCreatedEvent(id="e2", invoice_id="I001", customer_id="C001", amount=100.0),
    ]
    await pipeline.run(events)
    for tx in ledger.transactions:
        print(tx)


if __name__ == "__main__":
    asyncio.run(main())