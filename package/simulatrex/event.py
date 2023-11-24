"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: event.py
Description: Defines an event for a simulation and the event engine to manage events.

"""
from typing import List

from simulatrex.utils.log import SingletonLogger
from simulatrex.utils.time_utils import TimeUtils

_logger = SingletonLogger


class Event:
    def __init__(
        self,
        id: str,
        type: str,
        source: str = None,
        content: str = None,
        impact: float = 0.0,
        scheduled_time: str = None,
    ):
        """
        Initialize an event.

        Args:
            id (str): Unique identifier for the event.
            type (str): Type of the event.
            source (str, optional): Source of the event. Defaults to None.
            content (str, optional): content of the event. Defaults to None.
            impact (float, optional): Impact of the event. Defaults to 0.0.
            scheduled_time (str, optional): Scheduled time of the event. Defaults to None.
        """
        self.id = id
        self.type = type
        self.source = source
        self.content = content
        self.impact = impact
        self.scheduled_time = TimeUtils.to_timestamp(scheduled_time)
        self.is_triggered = False

    def __str__(self):
        return f"Event(id={self.id}, type={self.type}, source={self.source}, content={self.content}, scheduled_time={self.scheduled_time})"


class EventEngine:
    def __init__(self, events: List[any]):
        self.events = [
            Event(
                event.id,
                event.type,
                event.source,
                event.content,
                event.impact,
                event.scheduled_time,
            )
            for event in events
        ]

        self.init_events()

    def init_events(self):
        # Clear the list of events
        self.active_events: List[Event] = []
        self.past_events: List[Event] = []

    def process_events(self, previous_time: int, current_time: int):
        # Iterate over all events and check their conditions
        self.init_events()
        for event in self.events:
            if self._should_trigger(event, previous_time, current_time):
                _logger.debug(f"Event triggered: #{event.id} - {event.content}")
                self.active_events.append(event)
                event.is_triggered = True
            else:
                self.past_events.append(event)

        return self.active_events

    def _should_trigger(self, event: Event, previous_time: int, current_time: int):
        # Placeholder method. This should check the event's trigger conditions
        # and return True if they are met.
        # For simplicity, let's check against a time condition here.
        return (
            previous_time <= event.scheduled_time < current_time
            and not event.is_triggered
        )

    def get_recent_events(self, max_events=5):
        return self.active_events[-max_events:]
