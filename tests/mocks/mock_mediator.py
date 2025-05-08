class MockMediator:
    def __init__(self):
        self.published = []

    async def publish(self, events):
        self.published.extend(events)
