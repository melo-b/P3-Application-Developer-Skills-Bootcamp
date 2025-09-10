from ..base_screen import BaseScreen


class MatchResults(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"\nEnter results for '{self.tournament.name}'")
        print("This is a stub: no rounds/matches yet. Type B to go back.")

    def get_command(self):
        from commands import NoopCmd
        _ = self.input_string("Press Enter or type B to go back")
        return NoopCmd("tournament-view", tournament=self.tournament)


