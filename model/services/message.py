
class MessageService:
    queued_events = []

    @classmethod
    def send(cls, src_entity, target_entity, value, transit_duration):
        """Queue a message for sending.  When transit_duration gets to 0, it is sent."""
        cls.queued_events.append(
            { "source": src_entity,
              "target": target_entity,
              "value": value,
              "transit_duration": transit_duration})

    @classmethod
    def tick(cls):
        """Process any messages that have been waiting for this tick."""
        for event in cls.queued_events:
            event["transit_duration"] -= 1
            if (event["transit_duration"] == 0):
                event["target"].process(event["value"])
        cls.queued_events = [ event for event in cls.queued_events if event["transit_duration"] > 0]


