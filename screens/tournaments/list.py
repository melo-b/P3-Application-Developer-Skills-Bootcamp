from ..base_screen import BaseScreen
from commands import NoopCmd
from commands.create_tournament import CreateTournament

class TournamentList(BaseScreen):
    def __init__(self, tournaments):
        self.tournaments = sorted(tournaments, key=lambda t: t.start_date, reverse=True)
    
    def display(self):
        print("Available Tournaments (sorted by start date):")
        for idx, tournament in enumerate(self.tournaments, 1):
            status = "Active" if not getattr(tournament, 'completed', False) else "Completed"
            print(f"{idx}. {tournament.name} - {tournament.start_date} ({status})")
    
    def get_command(self):
        while True:
            print("\nEnter tournament number to view/manage, or:")
            print("C - Create new tournament")
            print("B - Back to main menu")
            
            choice = self.input_string("Your choice")
            
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.tournaments):
                    return NoopCmd("tournament-view", tournament=self.tournaments[idx])
                else:
                    print("Invalid tournament number. Please try again.")
            elif choice.upper() == "C":
                return CreateTournament()
            elif choice.upper() == "B":
                return NoopCmd("main-menu", skip_auto_redirect=True)
            else:
                print("Invalid choice. Please try again.")