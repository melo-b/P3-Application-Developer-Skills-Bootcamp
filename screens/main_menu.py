from commands import ExitCmd, NoopCmd
from commands.create_tournament import CreateTournament

from .base_screen import BaseScreen


class MainMenu(BaseScreen):
    """Main menu screen"""

    def __init__(self, clubs=None, skip_auto_redirect=False):
        # Load clubs if not provided
        if clubs is None:
            try:
                from models import ClubManager
                cm = ClubManager()
                self.clubs = cm.clubs
            except Exception:
                self.clubs = []
        else:
            self.clubs = clubs
            
        # Flag to skip automatic tournament redirect (useful when coming back from tournament screens)
        self.skip_auto_redirect = skip_auto_redirect
            
        # Lazy/optional tournament manager to avoid hard dependency before Step 2
        try:
            from models.tournament_manager import TournamentManager  # type: ignore
            self.tournament_manager = TournamentManager()
        except Exception:
            self.tournament_manager = None

    def display(self):
        # Check for active tournaments first (per spec requirement) if manager available
        # But skip auto-redirect if we're coming back from a tournament screen
        if getattr(self, "tournament_manager", None) and not self.skip_auto_redirect:
            # Reload tournaments to get the latest data
            self.tournament_manager.load_tournaments()
            active_tournaments = self.tournament_manager.get_active_tournaments()
            if len(active_tournaments) == 1:
                print(f"Active Tournament: {active_tournaments[0].name}")
                print("Redirecting to tournament management...")
                # Store the redirect info for get_command to use
                self._redirect_to = ("tournament-view", {"tournament": active_tournaments[0]})
                return None  # Don't return tuple from display()
            elif len(active_tournaments) > 1:
                print("Multiple active tournaments:")
                for idx, tournament in enumerate(active_tournaments, 1):
                    print(f"{idx}. {tournament.name}")
                # Store the redirect info for get_command to use
                self._redirect_to = ("tournament-list", {"tournaments": active_tournaments})
                return None  # Don't return tuple from display()

        # Fallback: Show club list if no active tournaments or manager unavailable
        print("Available Clubs:")
        for idx, club in enumerate(self.clubs, 1):
            print(idx, club.name)

    def get_command(self):
        # Check if we should redirect to tournament screens
        if hasattr(self, '_redirect_to'):
            screen_name, kwargs = self._redirect_to
            delattr(self, '_redirect_to')  # Clear the redirect
            return NoopCmd(screen_name, **kwargs)
        
        # Normal club menu logic
        while True:
            print("Type C to create a club or a club number to view/edit it.")
            print("Type T to create a tournament.")
            print("Type V to view all tournaments.")
            print("Type X to exit.")
            value = self.input_string()
            if value.isdigit():
                value = int(value)
                if value in range(1, len(self.clubs) + 1):
                    return NoopCmd("club-view", club=self.clubs[value - 1])
                else:
                    print("Invalid club number. Please try again.")
            elif value.upper() == "C":
                return NoopCmd("club-create")
            elif value.upper() == "T":
                return CreateTournament()
            elif value.upper() == "V":
                return self._view_all_tournaments()
            elif value.upper() == "X":
                return ExitCmd()
            else:
                print("Invalid choice. Please try again.")

    def _view_all_tournaments(self):
        """View all tournaments (active and completed)"""
        if not getattr(self, "tournament_manager", None):
            print("Tournament manager not available.")
            return NoopCmd("main-menu")
        
        # Reload tournaments to get the latest data
        self.tournament_manager.load_tournaments()
        all_tournaments = self.tournament_manager.tournaments
        
        if not all_tournaments:
            print("No tournaments found.")
            input("Press Enter to continue")
            return NoopCmd("main-menu")
        
        return NoopCmd("tournament-list", tournaments=all_tournaments)
