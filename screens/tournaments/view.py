from ..base_screen import BaseScreen

class TournamentView(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament
    
    def display(self):
        print(f"\n=== {self.tournament.name} ===")
        print(f"Location: {self.tournament.location}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        print(f"Rounds: {len(self.tournament.rounds)}")
        print(f"Current Round: {getattr(self.tournament, 'current_round', 'Not started')}")
        print(f"Players: {len(self.tournament.players)}")
    
    def get_command(self):
        print("\nOptions:")
        print("1. Register a player")
        print("2. Enter match results")
        print("3. Advance to next round")
        print("4. Generate tournament report")
        print("5. Back to main menu")
        
        choice = self.input_string("Your choice")
        from commands import NoopCmd
        if choice == "1":
            return NoopCmd("player-register", tournament=self.tournament)
        if choice == "2":
            return NoopCmd("match-results", tournament=self.tournament)
        if choice == "3":
            return NoopCmd("round-advance", tournament=self.tournament)
        if choice == "4":
            return NoopCmd("tournament-report", tournament=self.tournament)
        return NoopCmd("main-menu")