# CRM to Finance Event Pipeline

This repository implements a prototype event pipeline that synchronizes data from a customer
relationship management (CRM) system into a finance platform.  It illustrates patterns such as
event sourcing, idempotent message processing, and schema mapping.  While the source and
target systems are mocked, the pipeline demonstrates how to structure such integrations in a
robust and testable way.

## Components

* `events.py` – Defines the data models for CRM events and finance transactions using Pydantic.
* `pipeline.py` – Contains the core logic for consuming CRM events, transforming them into
  finance transactions, and writing them to the finance system.
* `tests/` – Simple tests to validate mapping and idempotency.

## Running the example

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Execute the pipeline with sample events:

```bash
python pipeline.py
```

This will simulate consuming a list of CRM events, transform them into finance transaction
records, and print the resulting finance ledger.

## Extending

In a real integration you would replace the mock CRM consumer and finance writer with
implementations that connect to actual services (e.g. via webhooks, message queues, or
REST APIs).  The mapping logic in `pipeline.py` can be extended to handle additional
event types and perform validations.

## Deployment verification

Use Python 3.12 on Linux. CI and Docker apply the checked-in dependency constraints.

```sh
python -m pip install -c requirements.lock -r requirements-dev.txt
python -m pytest -q
docker build -t reviewer-smoke .
docker run --rm reviewer-smoke
```

Expected result: three ledger entries, including one payment. The duplicate invoice event is skipped. The ledger and deduplication state are process-local.
