from ..base_screen import BaseScreen


class RoundAdvance(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"\nAdvance round for '{self.tournament.name}'")
        print("This is a stub: pairing logic not implemented yet.")
        print("Type Y to confirm advancing, any other key to cancel.")

    def get_command(self):
        from commands import NoopCmd
        choice = self.input_string("Advance round? (Y/N)")
        if choice.upper() == "Y":
            try:
                # Minimal increment and persist
                if self.tournament.current_round is None:
                    self.tournament.current_round = 1
                else:
                    self.tournament.current_round += 1
                from models.tournament_manager import TournamentManager  # type: ignore
                TournamentManager().save_tournament(self.tournament)
                print("Round advanced.")
            except Exception:
                print("Could not save changes.")
        return NoopCmd("tournament-view", tournament=self.tournament)


