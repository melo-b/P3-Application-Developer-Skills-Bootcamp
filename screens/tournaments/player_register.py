from ..base_screen import BaseScreen


class PlayerRegister(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"\nRegister a player to '{self.tournament.name}'")
        print("Enter a Chess ID (e.g., AB12345) to add the player.")
        print("Type B to go back.")

    def get_command(self):
        from commands import NoopCmd
        value = self.input_string("Chess ID or B")
        if value.upper() == "B":
            return NoopCmd("tournament-view", tournament=self.tournament)

        # Minimal logic: append chess_id if not already present
        if value and value not in self.tournament.players:
            try:
                self.tournament.players.append(value)
                # Persist change
                from models.tournament_manager import TournamentManager  # type: ignore
                TournamentManager().save_tournament(self.tournament)
                print("Player registered.")
            except Exception:
                print("Could not save changes. Player was not persisted.")
        else:
            print("Player already registered or invalid input.")

        return NoopCmd("tournament-view", tournament=self.tournament)


