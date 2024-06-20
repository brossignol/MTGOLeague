This project is used to MTGO leagues decks, classifiy the decks into archetype and prepare the results to display on Google spreadsheets.

Use: run main.py

The doc for MTGO API can be found here: https://census.daybreakgames.com

Register yourself at https://census.daybreakgames.com/#devSignup an place the ID inside a "login.txt" of this project.

Leagues ID (4 digits number) are required to call the API. There are directly visible on MTGO. 
For the history of ID we use Badaro deck list cache.

"C:/Projects/mtgo/MTGODecklistCache/Tournaments/mtgo.com" point toward https://github.com/Badaro/MTGODecklistCache it is used to get leaguesID.
"C:\Projects\mtgo\MTGOFormatData\Formats" point toward https://github.com/Badaro/MTGOFormatData, it is for the archetype parser.
mapping.csv contain the mapping subarchetype vs archetype (currently the Vintage one).