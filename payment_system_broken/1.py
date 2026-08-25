from models.event import PaymentEvent, PaymentStatus, VALID_TRANSITIONS
import uuid
from datetime import datetime, timezone

e = PaymentEvent(
    event_id        = str(uuid.uuid4()),
    payment_id      = 'PAY-TEST-001',
    sequence_number = 1,
    status          = PaymentStatus.INITIATED,
    amount_cents    = 9999,
    currency        = 'USD',
    merchant_id     = 'MERCH-001',
    event_time      = datetime.now(timezone.utc),
)

print('event created     :', e.payment_id)
print('status            :', e.status.value)
print('content hash      :', e.content_hash)

d  = e.to_dict()
e2 = PaymentEvent.from_dict(d)
print('round-trip ok     :', e2.event_id == e.event_id)

print()
print('state transitions:')
for from_state, allowed in VALID_TRANSITIONS.items():
    print(f'  {str(from_state):<12} -> {allowed}')

print()
print('ALL GOOD - models/event.py works correctly')
