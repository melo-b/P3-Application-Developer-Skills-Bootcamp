import json
import os
from .tournament import Tournament
from .round import Round
from .match import Match

class TournamentManager:
    """Manages tournament data loading, saving, and operations"""
    
    def __init__(self):
        self.tournaments = []
        self.tournaments_dir = "data/tournaments"
        self.load_tournaments()
    
    def load_tournaments(self):
        """Load all tournaments from JSON files"""
        if not os.path.exists(self.tournaments_dir):
            return
            
        for filename in os.listdir(self.tournaments_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.tournaments_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    # Convert JSON data to Tournament objects
                    tournament = self._json_to_tournament(data)
                    self.tournaments.append(tournament)

    def _json_to_tournament(self, data):
        """Adapt on-disk JSON (supports existing sample schema) to a Tournament object"""
        # Handle two schemas: new (flat) or sample (dates/from-to, venue)
        name = data.get("name")
        location = data.get("location") or data.get("venue")
        # Dates: either flat start_date/end_date or nested dates.from/to
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if not start_date or not end_date:
            dates = data.get("dates", {})
            start_date = dates.get("from")
            end_date = dates.get("to")

        number_of_rounds = data.get("number_of_rounds", 4)
        current_round = data.get("current_round")
        completed = data.get("completed", False)
        description = data.get("description", "")
        time_control = data.get("time_control", "rapid")

         tournament = Tournament(
        name=name,
        location=location,
        start_date=start_date,
        end_date=end_date,
        description=description,
        time_control=time_control,
        number_of_rounds=number_of_rounds,
        current_round=current_round,
        completed=completed,
    )

        # Players (for now, store raw IDs if sample data provides chess IDs)
        tournament.players = data.get("players", [])

        # Rounds/matches: keep raw for now; future work can turn into objects
        tournament.rounds = data.get("rounds", [])
    
        # Load player points if available
        tournament.player_points = data.get("player_points", {})

        return tournament

    def save_tournament(self, tournament):
        """Persist a tournament to disk using a normalized schema"""
        os.makedirs(self.tournaments_dir, exist_ok=True)
        safe_name = tournament.name.replace(" ", "_").lower()
        filepath = os.path.join(self.tournaments_dir, f"{safe_name}.json")
        with open(filepath, "w") as f:
            json.dump(tournament.serialize(), f, indent=2)

    def create_tournament(self, **kwargs):
        """Create, register, and persist a new tournament"""
        tournament = Tournament(**kwargs)
        self.tournaments.append(tournament)
        self.save_tournament(tournament)
        return tournament
    
    def get_active_tournaments(self):
        """Get tournaments that are not completed"""
        return [t for t in self.tournaments if not getattr(t, 'completed', False)]
    
    def get_completed_tournaments(self):
        """Get completed tournaments"""
        return [t for t in self.tournaments if getattr(t, 'completed', False)]