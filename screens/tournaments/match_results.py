from ..base_screen import BaseScreen


class MatchResults(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"\nEnter results for '{self.tournament.name}'")
        
        if not self.tournament.rounds:
            print("No rounds have been created yet. Advance to next round first.")
            return
        
        current_round = self.tournament.rounds[-1]
        print(f"Current Round: {current_round.name}")
        
        if not current_round.matches:
            print("No matches in this round. Advance to next round first.")
            return
        
        print("\nCurrent matches:")
        for i, match in enumerate(current_round.matches, 1):
            print(f"{i}. {match.player1} vs {match.player2} - Score: {match.score1}-{match.score2}")

    def get_command(self):
        from commands import NoopCmd
        
        if not self.tournament.rounds:
            input("Press Enter to go back")
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        current_round = self.tournament.rounds[-1]
        
        if not current_round.matches:
            input("Press Enter to go back")
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        print("\nEnter match number to update result, or:")
        print("B - Back to tournament view")
        
        choice = self.input_string("Your choice")
        
        if choice.upper() == "B":
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        if choice.isdigit():
            match_idx = int(choice) - 1
            if 0 <= match_idx < len(current_round.matches):
                match = current_round.matches[match_idx]
                self._enter_match_result(match)
        
        return NoopCmd("tournament-view", tournament=self.tournament)

    def _enter_match_result(self, match):
        """Enter result for a specific match"""
        print(f"\nEntering result for: {match.player1} vs {match.player2}")
        print("1 - Player 1 wins")
        print("2 - Player 2 wins") 
        print("3 - Draw")
        
        result = self.input_string("Result (1/2/3)")
        
        if result == "1":
            match.set_result(1, 0)
            self.tournament.add_points(match.player1, 1.0)
            self.tournament.add_points(match.player2, 0.0)
            print(f"{match.player1} wins!")
        elif result == "2":
            match.set_result(0, 1)
            self.tournament.add_points(match.player1, 0.0)
            self.tournament.add_points(match.player2, 1.0)
            print(f"{match.player2} wins!")
        elif result == "3":
            match.set_result(0.5, 0.5)
            self.tournament.add_points(match.player1, 0.5)
            self.tournament.add_points(match.player2, 0.5)
            print("Draw!")
        else:
            print("Invalid choice")
            return
        
        # Save the tournament
        try:
            from models.tournament_manager import TournamentManager
            TournamentManager().save_tournament(self.tournament)
            print("Result saved!")
        except Exception:
            print("Could not save result")