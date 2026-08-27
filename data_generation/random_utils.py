import random, hashlib, uuid
from datetime import datetime, timedelta, timezone

class RNG:
    def __init__(self, seed=42):
        self.r = random.Random(seed)
    def choice(self, seq): return self.r.choice(seq)
    def choices(self, seq, k): return [self.r.choice(seq) for _ in range(k)]
    def randint(self, a,b): return self.r.randint(a,b)
    def uniform(self, a,b): return self.r.uniform(a,b)
    def shuffle(self, x): self.r.shuffle(x); return x
    def uuid(self, name): return uuid.uuid5(uuid.NAMESPACE_DNS, name)
    def hash(self, s): return hashlib.sha256(s.encode()).hexdigest()
    def date_between(self, start: datetime, end: datetime):
        delta = (end - start).total_seconds()
        return start + timedelta(seconds=self.r.uniform(0, delta))
    def date(self, y,m,d): return datetime(y,m,d, tzinfo=timezone.utc)

rng = RNG()
