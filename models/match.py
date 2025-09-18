# Key Points
# Represents a match between two players
# Enforces that a match must have 2 players
# Allows updating results with set_result()
# Has serialize() method for JSON export


class Match:
    """Represents a match between two players in a round"""

    def __init__(self, player1, player2, score1=0, score2=0):
        if not player1 or not player2:
            raise ValueError("A match requires two players!")

        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def __str__(self):
        return f"<Match {self.player1} vs {self.player2} ({self.score1}-{self.score2})>"

    def set_result(self, score1, score2):
        """Set or update the match result"""
        self.score1 = score1
        self.score2 = score2

    def serialize(self):
        """Serialize match data for JSON export"""
        return {
            "player1": self.player1.serialize(),
            "player2": self.player2.serialize(),
            "score1": self.score1,
            "score2": self.score2,
        }
