# Key Points
# Dates are stored internally as datetime objects but are input and output
# as strings in "DD-MM-YYYY" format. Similar to Player class.
# Keeps lists of players and rounds.
# Has serialize() method so the whole tournament can be saved to JSON.

from datetime import datetime
import random


class Tournament:
    """The Tournament class holds all information related to a chess tournament"""

    DATE_FORMAT = "%d-%m-%Y"

    def __init__(self, name, location, start_date, end_date, description="",
                 time_control="bullet", number_of_rounds=4,
                 current_round=None, completed=False):
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
        self.player_points = {}  # Track tournament points for each player

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
        self.player_points[player] = 0.0

    def add_round(self, round_obj):
        """Adds a Round object to the tournament"""
        self.rounds.append(round_obj)

    def get_player_points(self, player):
        """Get current tournament points for a player"""
        return self.player_points.get(player, 0.0)

    def add_points(self, player, points):
        """Add points to a player's tournament total"""
        if player not in self.player_points:
            self.player_points[player] = 0.0
        self.player_points[player] += points

    def get_player_rankings(self):
        """Get players sorted by tournament points (descending)"""
        return sorted(self.players, key=lambda p: self.get_player_points(p),
                      reverse=True)

    def has_played_against(self, player1, player2):
        """Check if two players have played against each other in previous rounds"""
        for round_obj in self.rounds:
            for match in round_obj.matches:
                if ((match.player1 == player1 and match.player2 == player2) or
                        (match.player1 == player2 and match.player2 == player1)):
                    return True
        return False

    def generate_pairings(self):
        """Generate pairings for the next round using Swiss system"""
        if len(self.rounds) == 0:
            return self._generate_random_pairings()
        else:
            return self._generate_swiss_pairings()

    def _generate_random_pairings(self):
        """Generate random pairings for round 1"""
        players = self.players.copy()
        random.shuffle(players)

        pairings = []
        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                pairings.append((players[i], players[i + 1]))
        return pairings

    def _generate_swiss_pairings(self):
        """Generate Swiss system pairings based on current standings"""
        ranked_players = self.get_player_rankings()
        pairings = []
        used_players = set()

        for i, player1 in enumerate(ranked_players):
            if player1 in used_players:
                continue

            # Find best opponent for this player
            for j in range(i + 1, len(ranked_players)):
                player2 = ranked_players[j]
                if (player2 not in used_players and
                        not self.has_played_against(player1, player2)):
                    pairings.append((player1, player2))
                    used_players.add(player1)
                    used_players.add(player2)
                    break
            else:
                # If no unplayed opponent found, pair with closest available
                for j in range(i + 1, len(ranked_players)):
                    player2 = ranked_players[j]
                    if player2 not in used_players:
                        pairings.append((player1, player2))
                        used_players.add(player1)
                        used_players.add(player2)
                        break

        return pairings

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
            "player_points": {
                str(p): points for p, points in self.player_points.items()
            }
        }