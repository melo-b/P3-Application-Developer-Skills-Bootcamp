# Key Points
# Handles start and end timestamps
# Holds matches
# Has serialize() method for JSON export


from datetime import datetime


class Round:
    """Represents a single round in a tournament"""

    DATETIME_FORMAT = "%d-%m-%Y %H:%M"

    def __init__(self, name, start_datetime=None, end_datetime=None):
        if not name:
            raise ValueError("Round name is required!")

        self.name = name
        self._start_datetime = None
        self._end_datetime = None
        self.start_datetime = start_datetime or datetime.now().strftime(self.DATETIME_FORMAT)
        self.end_datetime = end_datetime or None

        self.matches = []  # list of Match objects

    def __str__(self):
        return f"<Round {self.name}>"

    @property
    def start_datetime(self):
        return self._start_datetime.strftime(self.DATETIME_FORMAT)

    @start_datetime.setter
    def start_datetime(self, value):
        self._start_datetime = datetime.strptime(value, self.DATETIME_FORMAT)

    @property
    def end_datetime(self):
        if self._end_datetime:
            return self._end_datetime.strftime(self.DATETIME_FORMAT)
        return None

    @end_datetime.setter
    def end_datetime(self, value):
        if value:
            self._end_datetime = datetime.strptime(value, self.DATETIME_FORMAT)

    def add_match(self, match):
        """Adds a Match object to this round"""
        self.matches.append(match)

    def serialize(self):
        """Serialize round data for JSON export"""
        return {
            "name": self.name,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "matches": [m.serialize() for m in self.matches],
        }
