# filename: models/event.py

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class PaymentStatus(str, Enum):
    INITIATED  = "INITIATED"
    AUTHORIZED = "AUTHORIZED"
    CAPTURED   = "CAPTURED"
    SETTLED    = "SETTLED"
    REFUNDED   = "REFUNDED"
    FAILED     = "FAILED"
    CANCELLED  = "CANCELLED"


# ── Legal state machine ───────────────────────────────────────
VALID_TRANSITIONS: Dict[Optional[str], list] = {
    None:                        ["INITIATED"],
    "INITIATED":                 ["AUTHORIZED", "FAILED", "CANCELLED"],
    "AUTHORIZED":                ["CAPTURED",   "FAILED", "CANCELLED"],
    "CAPTURED":                  ["SETTLED",    "REFUNDED", "FAILED"],
    "SETTLED":                   ["REFUNDED"],
    "REFUNDED":                  [],
    "FAILED":                    ["INITIATED"],
    "CANCELLED":                 [],
}


@dataclass
class PaymentEvent:
    event_id:        str
    payment_id:      str
    sequence_number: int
    status:          PaymentStatus
    amount_cents:    int
    currency:        str
    merchant_id:     str
    event_time:      datetime
    ingestion_time:  datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata:        Dict[str, Any] = field(default_factory=dict)
    source_system:   str = "payments-api-v1"

    # ── Derived properties ────────────────────────────────────
    @property
    def content_hash(self) -> str:
        payload = json.dumps({
            "payment_id":  self.payment_id,
            "status":      self.status,
            "amount_cents": self.amount_cents,
            "event_time":  self.event_time.isoformat(),
        }, sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()[:12]

    def is_valid_transition(self, current_status: Optional[str]) -> bool:
        allowed = VALID_TRANSITIONS.get(current_status, [])
        return self.status.value in allowed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id":        self.event_id,
            "payment_id":      self.payment_id,
            "sequence_number": self.sequence_number,
            "status":          self.status.value,
            "amount_cents":    self.amount_cents,
            "currency":        self.currency,
            "merchant_id":     self.merchant_id,
            "event_time":      self.event_time.isoformat(),
            "ingestion_time":  self.ingestion_time.isoformat(),
            "metadata":        self.metadata,
            "source_system":   self.source_system,
            "content_hash":    self.content_hash,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PaymentEvent":
        return cls(
            event_id        = d["event_id"],
            payment_id      = d["payment_id"],
            sequence_number = d["sequence_number"],
            status          = PaymentStatus(d["status"]),
            amount_cents    = d["amount_cents"],
            currency        = d["currency"],
            merchant_id     = d["merchant_id"],
            event_time      = datetime.fromisoformat(d["event_time"]),
            metadata        = d.get("metadata", {}),
            source_system   = d.get("source_system", "payments-api-v1"),
        )
