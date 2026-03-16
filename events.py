"""Event and record models for the CRM to finance pipeline."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CRMEvent(BaseModel):
    """Base class for events emitted from the CRM system."""

    id: str = Field(..., description="Unique identifier for the event")
    type: str = Field(..., description="Event type (e.g. customer_created, invoice_created)")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CustomerCreatedEvent(CRMEvent):
    """Event emitted when a new customer is created."""

    type: str = "customer_created"
    customer_id: str
    name: str
    email: str


class InvoiceCreatedEvent(CRMEvent):
    """Event emitted when an invoice is created in the CRM."""

    type: str = "invoice_created"
    invoice_id: str
    customer_id: str
    amount: float


class PaymentReceivedEvent(CRMEvent):
    """Event emitted when a payment is recorded in the CRM."""

    type: str = "payment_received"
    payment_id: str
    invoice_id: str
    amount: float


class FinanceTransaction(BaseModel):
    """Model for transactions to be recorded in the finance system."""

    id: str
    customer_id: Optional[str] = None
    invoice_id: Optional[str] = None
    amount: float
    description: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)