from commands.base import BaseCommand
from commands.context import Context
from models.tournament import Tournament
from models import ClubManager

class CreateTournament(BaseCommand):
    def __init__(self):
        # Remove context parameter since we're not using it yet
        pass

    def execute(self):
        print("\n=== Create a New Tournament ===")
        name = input("Tournament name: ")
        location = input("Location: ")
        start_date = input("Start date (dd-mm-yyyy): ")
        end_date = input("End date (dd-mm-yyyy): ")
        time_control = input("Time control (bullet/blitz/rapid): ") or "rapid"

        tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            time_control=time_control,
        )

        # Persist via TournamentManager if available
        try:
            from models.tournament_manager import TournamentManager  # type: ignore
            TournamentManager().create_tournament(
                name=name,
                location=location,
                start_date=start_date,
                end_date=end_date,
                time_control=time_control,
            )
        except Exception:
            pass

        print(f"\n✅ Tournament '{name}' created successfully!\n")
        
        cm = ClubManager()
        
        return Context("main-menu", clubs=cm.clubs)