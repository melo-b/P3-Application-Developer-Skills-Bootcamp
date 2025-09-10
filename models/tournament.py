
# Key Points
# Dates are stored internally as datetime objects but are input and output as strings in "DD-MM-YYYY" format. Similar to Player class. 
# Keeps lists of players and rounds. 
# Has serialize() method so the whole tournament can be saved to JSON.

from datetime import datetime


class Tournament:
    """The Tournament class holds all information related to a chess tournament"""

    DATE_FORMAT = "%d-%m-%Y"

    def __init__(self, name, location, start_date, end_date, description="", time_control="bullet", number_of_rounds=4, current_round=None, completed=False):
        if not name:
            raise ValueError("Tournament name is required!")
        if not location:
            raise ValueError("Tournament location is required!")

        self.name = name
        self.location = location
        self.description = description
        self.time_control = time_control  # e.g., "bullet", "blitz", "rapid"
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.completed = completed

        # Dates
        self._start_date = None
        self._end_date = None
        self.start_date = start_date  # uses setter
        self.end_date = end_date

        # Containers
        self.players = []   # list of Player objects
        self.rounds = []    # list of Round objects

    def __str__(self):
        return f"<Tournament {self.name} at {self.location}>"

    @property
    def start_date(self):
        return self._start_date.strftime(self.DATE_FORMAT)

    @start_date.setter
    def start_date(self, value):
        self._start_date = datetime.strptime(value, self.DATE_FORMAT)

    @property
    def end_date(self):
        return self._end_date.strftime(self.DATE_FORMAT)

    @end_date.setter
    def end_date(self, value):
        self._end_date = datetime.strptime(value, self.DATE_FORMAT)

    def add_player(self, player):
        """Adds a Player object to the tournament"""
        self.players.append(player)

    def add_round(self, round_obj):
        """Adds a Round object to the tournament"""
        self.rounds.append(round_obj)

    def serialize(self):
        """Serialize tournament data into JSON-compatible format"""
        return {
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "time_control": self.time_control,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round": self.current_round,
            "completed": self.completed,
            "players": [p.serialize() for p in self.players],
            "rounds": [r.serialize() for r in self.rounds],
        }
