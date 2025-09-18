from ..base_screen import BaseScreen


class RoundAdvance(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"\nAdvance round for '{self.tournament.name}'")
        current_round_num = len(self.tournament.rounds)
        
        if current_round_num >= self.tournament.number_of_rounds:
            print("Tournament is complete! All rounds have been played.")
            return
        
        print(f"Current round: {current_round_num}/{self.tournament.number_of_rounds}")
        print("Type Y to confirm advancing to next round, any other key to cancel.")

    def get_command(self):
        from commands import NoopCmd
        
        current_round_num = len(self.tournament.rounds)
        
        if current_round_num >= self.tournament.number_of_rounds:
            input("Press Enter to go back")
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        choice = self.input_string("Advance round? (Y/N)")
        if choice.upper() == "Y":
            from models.round import Round
            from models.match import Match
            
            new_round = Round(f"Round {current_round_num + 1}")
            
            # Generate pairings for this round
            pairings = self.tournament.generate_pairings()
            
            # Create matches from pairings
            for player1, player2 in pairings:
                match = Match(player1, player2)
                new_round.add_match(match)
            
            # Add the round to tournament
            self.tournament.add_round(new_round)
            self.tournament.current_round = current_round_num + 1
            
            # Check if tournament is complete
            if self.tournament.current_round >= self.tournament.number_of_rounds:
                self.tournament.completed = True
                print("Tournament completed!")
            
            # Save the tournament
            try:
                from models.tournament_manager import TournamentManager
                TournamentManager().save_tournament(self.tournament)
                print("Round advanced successfully!")
            except Exception:
                print("Could not save tournament")
        else:
            print("Round advancement cancelled")
            
        return NoopCmd("tournament-view", tournament=self.tournament)