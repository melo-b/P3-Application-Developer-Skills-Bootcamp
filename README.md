# Chess Tournament Management System - P3

This is a comprehensive chess tournament management application built with Python. The system allows you to manage chess clubs, players, and run complete tournaments from start to finish.

## Features

- **Club Management**: Create and manage chess clubs with player registration
- **Tournament Management**: Create, run, and manage chess tournaments
- **Swiss System Pairing**: Automatic matchmaking using Swiss tournament system
- **Player Registration**: Register players for tournaments from existing clubs
- **Match Results**: Enter match results and automatic point calculation
- **Tournament Reports**: Generate detailed reports in text and HTML formats
- **Data Persistence**: All data saved to JSON files for offline operation

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

Start the application with:
```bash
python manage_clubs.py
```

### Tournament Flow

The application follows this tournament flow:

1. **Main Menu**: 
   - If there's one active tournament, you'll be redirected to tournament management
   - If there are multiple active tournaments, you'll see a tournament list
   - If no active tournaments exist, you'll see the club management menu

2. **Creating a Tournament**:
   - From the main menu, type 'T' to create a new tournament
   - Enter tournament details (name, location, dates, time control)
   - Tournament is automatically saved to `data/tournaments/`

3. **Managing a Tournament**:
   - View tournament details and current status
   - Register players from existing clubs
   - Enter match results for completed games
   - Advance to next rounds (automatic pairing generation)
   - Generate tournament reports

4. **Player Registration**:
   - Search players by Chess ID (e.g., AB12345)
   - Players must exist in clubs before registration
   - Players are automatically added to tournament roster

5. **Match Results**:
   - Enter results for each match in the current round
   - Options: Player 1 wins, Player 2 wins, or Draw
   - Points automatically calculated (1 for win, 0.5 for draw, 0 for loss)

6. **Round Advancement**:
   - Generates pairings using Swiss system:
     - Round 1: Random pairings
     - Subsequent rounds: Point-based pairings avoiding repeat matches
   - Tournament marked as completed after final round

7. **Tournament Reports**:
   - View detailed tournament summary on screen
   - Generate HTML report (requires Jinja2)
   - Save text report to `reports/` directory
   - Includes player rankings, round results, and match details

### Data Structure

#### Clubs
- Located in `data/clubs/`
- Each club is a JSON file containing player information
- Players have: name, email, chess_id, birthday

#### Tournaments
- Located in `data/tournaments/`
- Contains tournament metadata, registered players, rounds, and matches
- Supports both legacy format and new normalized schema

#### Reports
- Generated in `reports/` directory
- Available in text and HTML formats
- Includes comprehensive tournament statistics

### Code Quality

This project follows Python best practices:

- **Object-Oriented Design**: Models, screens, and commands are properly separated
- **Single Responsibility Principle**: Each class has a focused purpose  
- **Template Pattern**: Commands follow consistent execution pattern
- **Data Persistence**: Immediate JSON file updates prevent data loss
- **Error Handling**: Graceful fallbacks and user-friendly error messages

### Generating flake8 Report

To generate a code quality report:

1. Install flake8-html (already in requirements.txt):
   ```bash
   pip install flake8-html
   ```

2. Generate HTML report:
   ```bash
   flake8 --format=html --htmldir=flake8_report --max-line-length=119
   ```

3. View the report by opening `flake8_report/index.html` in your browser

The project is configured to use flake8 with max line length of 119 characters as specified in the technical requirements.

### Project Structure

```
├── manage_clubs.py          # Main application entry point
├── models/                  # Data models
│   ├── club.py             # Chess club management
│   ├── club_manager.py     # Club operations
│   ├── tournament.py       # Tournament with matchmaking
│   ├── tournament_manager.py # Tournament operations
│   ├── player.py           # Player data model
│   ├── round.py            # Tournament round model
│   └── match.py            # Match data model
├── screens/                # User interface screens
│   ├── main_menu.py        # Main navigation
│   ├── clubs/              # Club management screens
│   ├── players/            # Player management screens
│   └── tournaments/        # Tournament management screens
├── commands/               # Command pattern implementations
├── data/                   # JSON data files
│   ├── clubs/              # Club data
│   └── tournaments/        # Tournament data
└── reports/                # Generated tournament reports
```

### Technical Specifications Compliance

This application meets all technical requirements:

- ✅ Standalone offline operation
- ✅ Python console application
- ✅ Cross-platform compatibility (Windows, Mac, Linux)
- ✅ JSON data persistence
- ✅ Complete tournament flow implementation
- ✅ Swiss system matchmaking
- ✅ Clean OOP architecture
- ✅ PEP 8 compliance (verified with flake8)
- ✅ Comprehensive documentation

### Troubleshooting

**Tournament not loading**: Ensure JSON files in `data/tournaments/` are valid JSON format

**Player registration fails**: Verify player exists in a club and has valid Chess ID format (XX12345)

**HTML reports not generating**: Install Jinja2 with `pip install Jinja2`

**Flake8 errors**: Run `flake8 --max-line-length=119` to check code quality

For additional help or bug reports, please check the project documentation or create an issue in the repository.