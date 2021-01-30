# NicFitBrew
So, you wanna build some nic fit decks?  This script will do it for you.  sort of.

# "Set up"
First, you need to run the "List_generator.py" With your input.txt.
This input file is very strict in the format.  It needs to contain the following on each line in specifically this order:
<Jank Score 1-10, with 10 being jankiest> <Minimum amount to add to the deck> <Maximum amount to add to the deck> <Exact Card Name>

Feel free to look at the included file for my ratings, and card list.  Append to it if you'd like.  it's probably easier that way.

If you want to skip that, I've also included the Card_Database.txt that I last generated which should be fine.

# Brewing
To brew, just run the Brew.py script, and tell it how many decks you want.  if you ask for 1, it'll just output in the display.  any more than that makes files.
If outputting to files, you need to make the directories for yourself, because I'm lazy and didn't make the script make them for you.
