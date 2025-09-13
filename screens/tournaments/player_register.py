from ..base_screen import BaseScreen


class PlayerRegister(BaseScreen):
    def __init__(self, tournament):
        self.tournament = tournament

    def display(self):
        print(f"\nRegister a player to '{self.tournament.name}'")
        print("Options:")
        print("1 - Search by Chess ID")
        print("2 - Search by name")
        print("3 - View all available players")
        print("B - Back to tournament view")

    def get_command(self):
        from commands import NoopCmd
        
        choice = self.input_string("Your choice")
        
        if choice.upper() == "B":
            return NoopCmd("tournament-view", tournament=self.tournament)
        elif choice == "1":
            return self._search_by_chess_id()
        elif choice == "2":
            return self._search_by_name()
        elif choice == "3":
            return self._view_all_players()
        else:
            print("Invalid choice")
            return NoopCmd("tournament-view", tournament=self.tournament)

    def _search_by_chess_id(self):
        """Search for a player by Chess ID"""
        from commands import NoopCmd
        
        chess_id = self.input_chess_id("Enter Chess ID (e.g., AB12345) or B to go back")
        if chess_id.upper() == "B":
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        # Search for player in all clubs
        player = self._find_player_by_chess_id(chess_id)
        if player:
            return self._register_player(player)
        else:
            print(f"Player with Chess ID '{chess_id}' not found in any club.")
            return NoopCmd("tournament-view", tournament=self.tournament)

    def _search_by_name(self):
        """Search for players by name (case insensitive partial match)"""
        from commands import NoopCmd
        
        name_part = self.input_string("Enter part of player name (case insensitive) or B to go back")
        if name_part.upper() == "B":
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        # Search for players matching name
        matching_players = self._find_players_by_name(name_part)
        if matching_players:
            return self._select_from_player_list(matching_players, f"Players matching '{name_part}'")
        else:
            print(f"No players found matching '{name_part}'.")
            return NoopCmd("tournament-view", tournament=self.tournament)

    def _view_all_players(self):
        """Display all available players from all clubs"""
        from commands import NoopCmd
        
        all_players = self._get_all_available_players()
        if all_players:
            return self._select_from_player_list(all_players, "All available players")
        else:
            print("No players found in any club.")
            return NoopCmd("tournament-view", tournament=self.tournament)

    def _find_player_by_chess_id(self, chess_id):
        """Find a player by Chess ID across all clubs"""
        try:
            from models.club_manager import ClubManager
            club_manager = ClubManager()
            
            for club in club_manager.clubs:
                for player in club.players:
                    if player.chess_id == chess_id:
                        return player
            return None
        except Exception:
            return None

    def _find_players_by_name(self, name_part):
        """Find players by partial name match (case insensitive)"""
        try:
            from models.club_manager import ClubManager
            club_manager = ClubManager()
            matching_players = []
            
            name_lower = name_part.lower()
            for club in club_manager.clubs:
                for player in club.players:
                    if name_lower in player.name.lower():
                        matching_players.append(player)
            return matching_players
        except Exception:
            return []

    def _get_all_available_players(self):
        """Get all players from all clubs"""
        try:
            from models.club_manager import ClubManager
            club_manager = ClubManager()
            all_players = []
            
            for club in club_manager.clubs:
                all_players.extend(club.players)
            return all_players
        except Exception:
            return []

    def _select_from_player_list(self, players, title):
        """Display a list of players and allow selection"""
        from commands import NoopCmd
        
        print(f"\n{title}:")
        print("-" * 60)
        
        # Filter out already registered players
        available_players = []
        for player in players:
            if player not in self.tournament.players:
                available_players.append(player)
        
        if not available_players:
            print("All matching players are already registered for this tournament.")
            input("Press Enter to continue")
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        # Display available players
        for i, player in enumerate(available_players, 1):
            print(f"{i}. {player.name} ({player.chess_id}) - {player.email}")
        
        print(f"\nEnter player number (1-{len(available_players)}) or B to go back:")
        
        choice = self.input_string("Your choice")
        if choice.upper() == "B":
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        try:
            player_idx = int(choice) - 1
            if 0 <= player_idx < len(available_players):
                selected_player = available_players[player_idx]
                return self._register_player(selected_player)
            else:
                print("Invalid player number")
                return NoopCmd("tournament-view", tournament=self.tournament)
        except ValueError:
            print("Invalid input")
            return NoopCmd("tournament-view", tournament=self.tournament)

    def _register_player(self, player):
        """Register a player for the tournament"""
        from commands import NoopCmd
        
        if player in self.tournament.players:
            print(f"{player.name} is already registered for this tournament.")
            input("Press Enter to continue")
            return NoopCmd("tournament-view", tournament=self.tournament)
        
        try:
            # Add player to tournament
            self.tournament.add_player(player)
            
            # Persist change
            from models.tournament_manager import TournamentManager
            TournamentManager().save_tournament(self.tournament)
            
            print(f"✅ {player.name} ({player.chess_id}) successfully registered!")
            input("Press Enter to continue")
            
        except Exception as e:
            print(f"❌ Could not register player: {e}")
            input("Press Enter to continue")
        
        return NoopCmd("tournament-view", tournament=self.tournament)