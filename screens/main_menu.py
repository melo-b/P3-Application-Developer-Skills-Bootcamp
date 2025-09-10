from commands import ExitCmd, NoopCmd
from commands.create_tournament import CreateTournament

from .base_screen import BaseScreen


class MainMenu(BaseScreen):
    """Main menu screen"""

    def __init__(self, clubs):
        self.clubs = clubs
        # Lazy/optional tournament manager to avoid hard dependency before Step 2
        try:
            from models.tournament_manager import TournamentManager  # type: ignore
            self.tournament_manager = TournamentManager()
        except Exception:
            self.tournament_manager = None

    def display(self):
        # Check for active tournaments first (per spec requirement) if manager available
        if getattr(self, "tournament_manager", None):
            active_tournaments = self.tournament_manager.get_active_tournaments()
            if len(active_tournaments) == 1:
                print(f"Active Tournament: {active_tournaments[0].name}")
                print("Redirecting to tournament management...")
                # Return tuple for get_command to forward as kwargs
                return ("tournament-view", {"tournament": active_tournaments[0]})
            elif len(active_tournaments) > 1:
                print("Multiple active tournaments:")
                for idx, tournament in enumerate(active_tournaments, 1):
                    print(f"{idx}. {tournament.name}")
                return ("tournament-list", {"tournaments": active_tournaments})

        # Fallback: Show club list if no active tournaments or manager unavailable
        print("Available Clubs:")
        for idx, club in enumerate(self.clubs, 1):
            print(idx, club.name)

    def get_command(self):
        # Check if we should redirect to tournament screens
        display_result = self.display()
        if isinstance(display_result, tuple):
            screen_name, kwargs = display_result
            return NoopCmd(screen_name, **kwargs)
        
        # Normal club menu logic
        while True:
            print("Type C to create a club or a club number to view/edit it.")
            print("Type T to create a tournament.")
            print("Type X to exit.")
            value = self.input_string()
            if value.isdigit():
                value = int(value)
                if value in range(1, len(self.clubs) + 1):
                    return NoopCmd("club-view", club=self.clubs[value - 1])
            elif value.upper() == "C":
                return NoopCmd("club-create")
            elif value.upper() == "T":
                return CreateTournament()  # Fixed: no parameter needed
            elif value.upper() == "X":
                return ExitCmd()
