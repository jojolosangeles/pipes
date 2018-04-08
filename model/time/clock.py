
class Universe:
    """Only the Universe ticks.  Clicks just follow along."""
    tick_count = 0
    registered_tickers = []

    @classmethod
    def tick(cls):
        cls.tick_count += 1
        for ticker in cls.registered_tickers:
            ticker.tick()

class Clock:
    def __init__(self, start_time = 0):
        self.start_time = start_time
        self.tick_count_at_start = Universe.tick_count

    def time(self):
        return Universe.tick_count - self.tick_count_at_start + self.start_time

