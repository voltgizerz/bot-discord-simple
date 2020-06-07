import datetime

def get_timestamp(*, fmt="%H:%M:%S", wrap=lambda ts: f"[{ts}]"):
    ts = datetime.datetime.now().strftime(fmt)
    if callable(wrap):
        return wrap(ts)
    return ts
