from ..base_screen import BaseScreen


class TournamentReport(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"\nReport for '{self.tournament.name}'")
        print(f"Location: {self.tournament.location}")
        print(f"Dates: {self.tournament.start_date} to {self.tournament.end_date}")
        print(f"Rounds: {len(self.tournament.rounds)} | Current: {self.tournament.current_round}")
        print(f"Players ({len(self.tournament.players)}): {self.tournament.players}")
        print("\n(Stub) Full report generation will be implemented later.")

    def get_command(self):
        from commands import NoopCmd
        _ = self.input_string("Press Enter to go back")
        return NoopCmd("tournament-view", tournament=self.tournament)


