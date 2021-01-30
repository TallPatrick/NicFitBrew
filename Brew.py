import random
from time import time

class Card:
    def __init__(self, name, Jank, MinCount, MaxCount, isSnow, TypeLine, isWhite, isBlue, isBlack, isRed, isGreen):
        self.name = name # String
        self.MinCount = MinCount # int
        self.MaxCount = MaxCount # int
        self.isWhite = isWhite # bool
        self.isBlue = isBlue # bool
        self.isBlack = isBlack # bool
        self.isRed = isRed # bool
        self.isGreen = isGreen # bool
        self.isSnow = isSnow # bool
        self.TypeLine = TypeLine # string
        self.Jank = int(Jank) # int from 1-10, 10 being Jankier
    def GSZable(self):
        if self.isGreen and "Creature" in self.TypeLine:
            return(True)
        else:
            return(False)
    def JankTest(self):
        if self.Jank != 1:
            if random.randint(1,10) >= self.Jank:
                return(True)
            else:
                return(False)
        else:
            return(True) # Cards with a Jank rating of 1 should always be added
    def isFiveColor(self):
        if self.isGreen and self.isRed and self.isWhite and self.isBlue and self.isBlack:
            return(True)
        else:
            return(False)
    def TypeCheck(self, TypeString):
        if TypeString in self.TypeLine:
            return(True)
        else:
            return(False)

def count_deck(dict): # Counts number of cards in any deck dictionary
    n = 0
    for entry in dict:
        n = n + int(dict[entry])
    return(int(n))

def Printer(dict): # Prints decklist to screen for debugging
    for val in dict:
        print(dict[val], val)

def Writer(file, dict): # Writes to file
    for val in dict:
        file.write(str(dict[val]) + " " + str(val) + "\n")

def Importer(filename): # Reads text file of card information into list for future use.
    Output_List = []
    with open(filename) as file:
        for line in enumerate(file):
            Snow = White = Blue = Black = Red = Green = False        
            split = line[1].split("\n") # This is hacky and ugly and I hate it.
            split = split[0].split("|")
            name = split[0]
            Jank = split[1]
            MinCount = split[2]
            MaxCount = split[3]
            if split[4] == "S":
                Snow = True
            TypeLine = split[5]
            if "W" in split:
                White = True
            if "U" in split:
                Blue = True
            if "B" in split:
                Black = True
            if "R" in split:
                Red = True
            if "G" in split:
                Green = True
            Output_List.append(Card(name,Jank,MinCount,MaxCount,Snow,TypeLine,White,Blue,Black,Red,Green))
    return(Output_List)


def main(loops):
    total_time = int(time() * 1000)
    cycles = 0
    random.seed()
    while cycles < loops:
        cycles = cycles + 1
        Start_Time = int(time() * 1000)
        # The core:
        Decklist = {
            "Veteran Explorer" : 4, 
            "Cabal Therapy" : 4,
            }

        # Color Picking
        DeckWhite = DeckBlue = DeckRed = False
        Colors_list = ("GB","GB","GB","GBW","GBW","GBW","BUG","BUG","Jund","Jund","NotRed","WUBRG")
        Colors = random.choice(Colors_list) # This is hackier, but more adaptable than using weighted random lists.
        if Colors == "BUG" or Colors == "NotRed" or Colors == "WUBRG":
            DeckBlue = True

        if Colors == "GBW" or Colors == "NotRed" or Colors == "WUBRG":
            DeckWhite = True

        if Colors == "Jund" or Colors == "WUBRG":
            DeckRed = True

        # Import Card Database into card objects

        All_Available_Cards = Importer("Card_Database.txt")

        GSZCount = 4 # Setting to 4, because Vets.
        SnowCount = 0
        JankScore = 0 # Used to track how Janky the deck is.
        Added = [] # Created so that added card objects are in a list for future reference.
        Card_Count = 8 # Initial count for the vets and Cabal Therapies
        while Card_Count < 39:
            if len(All_Available_Cards) == 0:
                Decklist["Relentless Rats"] = 39 - Card_Count # To cover for the VERY rare case where RNG doesn't want to add any cards, This will force add Relentless rats to fill the deck.  Chances of this happening are so small this probably doesn't even matter.
            else:
                index = random.randint(0,len(All_Available_Cards)-1)
                Adding = All_Available_Cards.pop(index)
                if Adding.JankTest: # Do the Jank Test and only add the card if it passes
                    # Check colors match            
                    if (DeckWhite == Adding.isWhite or DeckWhite) and (DeckBlue == Adding.isBlue or DeckBlue) and (DeckRed == Adding.isRed or DeckRed): # Color Checking
                        count = random.randint(int(Adding.MinCount),int(Adding.MaxCount)) # Pick how many to add
                        JankScore = JankScore + (int(Adding.Jank) * count) # Update the running Jank Score of the Deck
                        Decklist[Adding.name] = count # Assign it into the deck dict
                        Added.append(Adding) # Add these in to another list for land count later
                        if Adding.GSZable():
                            GSZCount = GSZCount + count
                        if Adding.isSnow:
                            SnowCount = SnowCount + count
                        # Begin Special Cases
                        # Rectors
                        if Adding.name == "Academy Rector": # Special Handling for Academy Rector
                            if Card_Count < 34:
                                for i in ["Curse of Misfortunes","Curse of Death's Hold","Curse of Exhaustion","Overwhelming Splendor","Cruel Reality","Dovescape","Ethereal Absolution","Sandwurm Convergence","Omniscience","Starfield of Nyx"]:
                                    if random.randint(0,1) == 1:
                                        Decklist[i] = 1
                            else:
                                del Decklist[Adding.name]
                                del Added[-1]
                                JankScore = JankScore - (int(Adding.Jank) * count)
                        if Adding.name == "Arena Rector": # Special Handling for Arena Rector (Yes, it intentionally works a little different than the Academy rector section)
                            if Card_Count < 34:
                                for i in ["Ugin, the Spirit Dragon","Nicol Bolas, Planeswalker","Nicol Bolas, God-Pharaoh","Karn Liberated","Elspeth, Sun's Champion","Nicol Bolas, Dragon-God"]:
                                    rand_count = random.randint(0,2)
                                    if rand_count != 0:
                                        Decklist[i] = rand_count
                            else:
                                del Decklist[Adding.name]
                                del Added[-1]
                                JankScore = JankScore - (int(Adding.Jank) * count)
                        if Adding.name == "Stoneforge Mystic":
                            offset = random.randint(0,2) # Add an Equipment, This works because the Equipment is next to SFM in the database.
                            equipment = All_Available_Cards.pop(index + offset)
                            Added.append(equipment)
                            Decklist[equipment.name] = 1
                            JankScore = JankScore + (int(equipment.Jank) * count)
                            offset = random.randint(0,1)  # do it again!
                            equipment = All_Available_Cards.pop(index + offset)
                            Added.append(equipment)
                            Decklist[equipment.name] = 1
                            JankScore = JankScore + (int(equipment.Jank) * count)
                        # "Partners With" and other simple synergy Cards (should try to make this into a function at some point)
                        if Adding.name == "Zealous Conscripts":
                            if All_Available_Cards[index].name == "Kiki-Jiki, Mirror Breaker":
                                Decklist["Kiki-Jiki, Mirror Breaker"] = 1
                                Added.append(All_Available_Cards.pop(index)) # Adding synergy card, which is adjacent in the list
                            else:
                                del Decklist[Adding.name]
                                del Added[-1]
                                JankScore = JankScore - (int(Adding.Jank) * count)
                        if Adding.name == "Kiki-Jiki, Mirror Breaker":
                            if All_Available_Cards[index - 1].name == "Zealous Conscripts":
                                Decklist["Zealous Conscripts"] = 1
                                Added.append(All_Available_Cards.pop(index - 1)) # Adding synergy card, which is adjacent in the list
                            else:
                                del Decklist[Adding.name]
                                del Added[-1]
                                JankScore = JankScore - (int(Adding.Jank) * count)
                        if Adding.name == "Punishing Fire":
                            Decklist["Grove of the Burnwillows"] = 2
                        if Adding.name == "Pir, Imaginative Rascal" and DeckBlue:
                            if All_Available_Cards[index].name == "Toothy, Imaginary Friend":
                                Decklist["Toothy, Imaginary Friend"] = 1
                                Added.append(All_Available_Cards.pop(index)) # Adding partner card, which is adjacent in the list
                            else:
                                del Decklist[Adding.name]
                                del Added[-1]
                                JankScore = JankScore - (int(Adding.Jank) * count)
                        if Adding.name == "Toothy, Imaginary Friend":
                            if All_Available_Cards[index - 1].name == "Pir, Imaginative Rascal":
                                Decklist["Pir, Imaginative Rascal"] = 1
                                Added.append(All_Available_Cards.pop(index - 1)) # Adding partner card, which is adjacent in the list
                                GSZCount = GSZCount + 1
                            else:
                                del Decklist[Adding.name]
                                del Added[-1]
                                JankScore = JankScore - (int(Adding.Jank) * count)
                        if Adding.name == "Yannik, Scavenging Sentinel":
                            if All_Available_Cards[index].name == "Nikara, Lair Scavenger":
                                Decklist["Nikara, Lair Scavenger"] = 1
                                Added.append(All_Available_Cards.pop(index)) # Adding partner card, which is adjacent in the list
                            else:
                                del Decklist[Adding.name]
                                del Added[-1]
                                JankScore = JankScore - (int(Adding.Jank) * count)
                        if Adding.name == "Nikara, Lair Scavenger":
                            if All_Available_Cards[index - 1].name == "Yannik, Scavenging Sentinel":
                                Decklist["Yannik, Scavenging Sentinel"] = 1
                                Added.append(All_Available_Cards.pop(index - 1)) # Adding partner card, which is adjacent in the list
                                GSZCount = GSZCount + 1
                            else:
                                del Decklist[Adding.name]
                                del Added[-1]
                                JankScore = JankScore - (int(Adding.Jank) * count)
            Card_Count = 1 # Again, setting for the Bayou that will be added later
            for i in Decklist:
                Card_Count = Card_Count + Decklist[i]

        GreenCount = 0
        # Add Green Sun's Zeniths based on break points for GSZ Counts
        if GSZCount > 10 and GSZCount < 16:
            Decklist["Green Sun's Zenith"] = 2
            GreenCount = 2
        if GSZCount >= 16 and GSZCount < 21:
            Decklist["Green Sun's Zenith"] = 3
            GreenCount = 3
        if GSZCount >= 21:
            Decklist["Green Sun's Zenith"] = 4
            GreenCount = 4

        # Add the Bayou
        Decklist["Bayou"] = 1
        # Color Counting
        WhiteCount = BlueCount = RedCount= 0
        BlackCount = 4 # Initializing at 4 for Therapies
        GreenCount = GreenCount + 4 # Adding the 4 vets
        for i in Added:
            if i.isWhite:
                WhiteCount = WhiteCount + int(Decklist[i.name])
            if i.isBlue:
                BlueCount = BlueCount + int(Decklist[i.name])
            if i.isBlack:
                BlackCount = BlackCount + int(Decklist[i.name])
            if i.isRed:
                RedCount = RedCount + int(Decklist[i.name])
            if i.isGreen:
                GreenCount = GreenCount + int(Decklist[i.name])
        TotalCount = WhiteCount + BlueCount + BlackCount + RedCount + GreenCount
        LandCount = int((59 - Card_Count) / 2) # One less because there's already a Bayou, divided in half because ~half basics should lead to at least 8

        # Do ratio math for each color and add at least 1 basic of each type
        if DeckBlue:
            BlueRatio = int((BlueCount / TotalCount) * LandCount)
            if BlueRatio > 0 and DeckBlue:
                Decklist['Island'] = BlueRatio
            else:
                Decklist['Island'] = 1
            
        if DeckRed:
            RedRatio = int((RedCount / TotalCount) * LandCount)
            if RedRatio > 0 and DeckRed:
                Decklist['Mountain'] = RedRatio
            else:
                Decklist['Mountain'] = 1

            
        if DeckWhite:
            WhiteRatio = int((WhiteCount / TotalCount) * LandCount)
            if WhiteRatio > 0 and DeckWhite:
                Decklist['Plains'] = WhiteRatio
            else:
                Decklist['Plains'] = 1

        # Do Ratio math for Forests and Swamps here, because all decks will have Black and Green.
        Decklist["Forest"] = int(((GreenCount / TotalCount) * LandCount)) 

        Decklist["Swamp"] = int(((BlackCount / TotalCount) * LandCount))
            
        # Some hard codings for utility lands

        if DeckWhite:
            Decklist['Karakas'] = 1

        if random.randint(0,6) > 2:
            Decklist['Phyrexian Tower'] = 1

        # Find the most prominent color (besides Black and Green), and add 2 G/x duals for it, otherwise add 1.
        if WhiteCount > BlueCount and WhiteCount > RedCount:
            Decklist['Savannah'] = 2

        else:
            if DeckWhite:
                Decklist['Savannah'] = 1
                

        if BlueCount > WhiteCount and BlueCount > RedCount:
            Decklist['Tropical Island'] = 2

        else:
            if DeckBlue:
                Decklist['Tropical Island'] = 1
                

        if RedCount > WhiteCount and RedCount > BlueCount:
            Decklist['Taiga'] = 2

        else:
            if DeckRed:
                Decklist['Taiga'] = 1
                
        # Fill the rest of the deck with lands.  Fetches if it can, then duals, then basics.
        while Card_Count < 60:
            randomizer = random.randint(1,4)
            if randomizer == 1:
                if "Verdant Catacombs" in Decklist:
                    if Decklist["Verdant Catacombs"] < 4:
                        Decklist["Verdant Catacombs"] = Decklist["Verdant Catacombs"] + 1
                    else:
                        if Decklist["Bayou"] < 4:
                            Decklist["Bayou"] = Decklist["Bayou"] + 1
                        else:
                            if Decklist["Swamp"] < Decklist["Forest"]:
                                Decklist["Swamp"] = Decklist["Swamp"] + 1
                            else:
                                Decklist["Forest"] = Decklist["Forest"] + 1
                else:
                    Decklist["Verdant Catacombs"] = 1
            if randomizer == 2 and DeckWhite:
                if "Windswept Heath" in Decklist:
                    if Decklist["Windswept Heath"] < 4:
                        Decklist["Windswept Heath"] = Decklist["Windswept Heath"] + 1
                    else:
                        if Decklist["Savannah"] < 4:
                            Decklist["Savannah"] = Decklist["Savannah"] + 1
                        else:
                            if Decklist["Plains"] < Decklist["Forest"]:
                                Decklist["Plains"] = Decklist["Plains"] + 1
                            else:
                                Decklist["Forest"] = Decklist["Forest"] + 1
                else:
                    Decklist["Windswept Heath"] = 1
            if randomizer == 3 and DeckBlue:
                if "Misty Rainforest" in Decklist:
                    if Decklist["Misty Rainforest"] < 4:
                        Decklist["Misty Rainforest"] = Decklist["Misty Rainforest"] + 1
                    else:
                        if Decklist["Tropical Island"] < 4:
                            Decklist["Tropical Island"] = Decklist["Tropical Island"] +1
                        else:
                            if Decklist["Island"] < Decklist["Forest"]:
                                Decklist["Island"] = Decklist["Island"] + 1
                            else:
                                Decklist["Forest"] = Decklist["Forest"] + 1
                else:
                    Decklist["Misty Rainforest"] = 1
            if randomizer == 4 and DeckRed:
                if "Wooded Foothills" in Decklist:
                    if Decklist["Wooded Foothills"] < 4:
                        Decklist["Wooded Foothills"] = Decklist["Wooded Foothills"] +1
                    else:
                        if Decklist["Taiga"] < 4:
                            Decklist["Taiga"] = Decklist["Taiga"] + 1
                        else:
                            if Decklist["Mountain"] < Decklist["Forest"]:
                                Decklist["Mountain"] = Decklist["Mountain"] + 1
                            else:
                                Decklist["Forest"] = Decklist["Forest"] + 1
                else:
                    Decklist["Wooded Foothills"] = 1
            Card_Count = 0 # Not setting to 1, because the Bayou has been added.
            for i in Decklist:
                Card_Count = Card_Count + Decklist[i]

        # Snow Support

        if SnowCount > 0 or random.randint(0,2) == 0:
            for land in ["Forest","Swamp","Island","Plains","Mountain"]:
                if land in Decklist:
                    Decklist["Snow-Covered " + land] = Decklist.pop(land)


        # Deck naming section
        DeckName = ""
        if Colors == "GB":
            if random.randint(0,1) == 1:
                DeckName = "Golgari "
            else:
                DeckName = "BG "
        if Colors == "BUG":
            DeckName = "BUG "
        if Colors == "GBW":
            if random.randint(0,4) > 0:
                DeckName = "Junk "
            else:
                DeckName = "Abzan "
        if Colors == "Jund":
            DeckName = "Jund "
        if Colors == "NotRed":
            if random.randint(0,5) > 0:
                DeckName = "4 Color "
            else:
                DeckName = "Wet Abzan " # LOL
        if Colors == "WUBRG":
            DeckName = "5 Color "

        n=0
        name_choices = random.randint(1,3)
        while n < name_choices: # Yes, I could do random.coices(list), but this way is funnier, because sometimes you get the same word twice.
            Card1 = random.choice(Added).name.split(" ", 1)
            DeckName = DeckName + Card1[0] + " "
            n=n+1

        DeckName = DeckName.replace(",","") + "Fit"

        # Make Sideboard from Green and Black Cards because I'm too lazy to go through the hassle of checking for other colors in the deck
        Sideboard = {}
        SBCount = 0
        # The order of these sections can be changed if the meta changes.
        # I found that the aggro hate is pretty good all purpose, and fights against blue stews decently
        # After that combo is the next biggest pain in the butt, so it's next on the list.

        # Add some Aggro Hate
        if random.randint(1,2) == 1:
            if random.randint(1,2) == 1:
                if "Pernicious Deed" not in Decklist:
                    Sideboard["Pernicious Deed"] = random.randint(2,3)
                else:
                    Sideboard["Pernicious Deed"] = 4 - Decklist["Pernicious Deed"]
            else:
                if "Plague Engineer" not in Decklist:
                    Sideboard["Plague Engineer"] = random.randint(2,3)
                else:
                    Sideboard["Plague Engineer"] = 3 - Decklist["Plague Engineer"] 
        else:
            if "Pernicious Deed" not in Decklist:
                Sideboard["Pernicious Deed"] = random.randint(2,3)
            else:
                Sideboard["Pernicious Deed"] = 4 - Decklist["Pernicious Deed"]
            if "Plague Engineer" not in Decklist:
                Sideboard["Plague Engineer"] = random.randint(2,3)
            else:
                Sideboard["Plague Engineer"] = 3 - Decklist["Plague Engineer"]

        # Add some Combo Hate
        if DeckWhite and "Gaddock Teeg" not in Decklist:
            Sideboard["Gaddock Teeg"] = 1
        if random.randint(1,2) == 1:
            if random.randint(1,2) == 1:
                if "Thoughtseize" not in Decklist:
                    Sideboard["Thoughtseize"] = random.randint(3,4)
                else:
                    if Decklist["Thoughtseize"] != 4:
                        Sideboard["Thoughtseize"] = 4 - Decklist["Thoughtseize"]
            else:
                Sideboard["Collector Ouphe"] = 2

        else:
            if "Thoughtseize" not in Decklist:
                Sideboard["Thoughtseize"] = random.randint(2,3)
            else:
                if Decklist["Thoughtseize"] != 4:
                    Sideboard["Thoughtseize"] = 4 - Decklist["Thoughtseize"]
            Sideboard["Collector Ouphe"] = 2

        SBCount = count_deck(Sideboard)
        # Add some GY Hate
        if SBCount < 12 and random.randint(1,5) > 1:
            Sideboard["Leyline of the Void"] = 4
            SBCount = SBCount + 4

        if SBCount < 14 and "Scavenging Ooze" not in Decklist and random.randint(1,5) > 2:
            Sideboard["Scavenging Ooze"] = 2
            SBCount = SBCount + 2

        if SBCount < 13 and random.randint(1,5) > 3:
            Sideboard["Surgical Extraction"] = 3
            SBCount = SBCount + 3

        # Add some specific Blue Hate
        if SBCount < 13 and random.randint(1,5) > 2:
            Sideboard["Veil of Summer"] = 3
            SBCount = SBCount + 3

        if SBCount < 14 and random.randint(1,6) > 4:
            Sideboard["Carpet of Flowers"] = 2
            SBCount = SBCount + 2

        # Fill with other cards
        if SBCount < 12 and "Assassin's Trophy" not in Decklist:
            Sideboard["Assassin's Trophy"] = 4
            SBCount = SBCount + 4
        if SBCount < 13 and "Assassin's Trophy" not in Decklist and "Assassin's Trophy" not in Sideboard:
            Sideboard["Assassin's Trophy"] = 3
            SBCount = SBCount + 3
        if SBCount < 14 and "Assassin's Trophy" not in Decklist and "Assassin's Trophy" not in Sideboard:
            Sideboard["Assassin's Trophy"] = 2
            SBCount = SBCount + 2

        if SBCount < 13 and random.randint(1,7) > 3:
            Sideboard["Force of Vigor"] = 3
            SBCount = SBCount + 3

        if (SBCount < 12 and SBCount > 6):
            Sideboard["Faerie Macabre"] = 12 - SBCount
            SBCount = 12

        if SBCount < 15 and "Veil of Summer" not in Sideboard:
            Sideboard["Veil of Summer"] = 15 - SBCount
            SBCount = 15

        if SBCount < 15:
            Sideboard["Seedtime"] = 15 - SBCount
            SBCount = 15

        # Sort the list
        # Make Blank dicts for each type
        Creatures = {}
        Enchantments = {}
        Artifacts = {}
        Planeswalkers = {}
        Spells = {}
        Lands = {}
        AddedNames = {}
        for index in range(len(Added)):
            AddedNames[Added[index].name] = index

        for card in Decklist:
        # Find all the Creatures in the list
            if card in ["Veteran Explorer"]:
                Creatures[card] = Decklist[card]
            if card in AddedNames:
                if "Creature" in Added[AddedNames[card]].TypeLine:
                    Creatures[card] = Decklist[card]
        # Find all the Enchantments in the list
            if card in ["Curse of Misfortunes","Curse of Death's Hold","Curse of Exhaustion","Overwhelming Splendor","Cruel Reality","Dovescape","Ethereal Absolution","Sandwurm Convergence","Omniscience","Starfield of Nyx"]:
                Enchantments[card] = Decklist[card]
            if card in AddedNames:
                if "Enchantment" in Added[AddedNames[card]].TypeLine and "Creature" not in Added[AddedNames[card]].TypeLine:
                    Enchantments[card] = Decklist[card]
        # Find all the Artifacts in the list
            if card in AddedNames:
                if "Artifact" in Added[AddedNames[card]].TypeLine and "Creature" not in Added[AddedNames[card]].TypeLine:
                    Artifacts[card] = Decklist[card]
        # Find all the Planeswalkers in the list
            if card in ["Ugin, the Spirit Dragon","Nicol Bolas, Planeswalker","Nicol Bolas, God-Pharaoh","Karn Liberated","Elspeth, Sun's Champion","Nicol Bolas, Dragon-God"]:
                Planeswalkers[card] = Decklist[card]
            if card in AddedNames:
                if "Planeswalker" in Added[AddedNames[card]].TypeLine:
                    Planeswalkers[card] = Decklist[card]
        # Find all the Instants and Sorceries in the list
            if card in ["Cabal Therapy","Green Sun's Zenith"]:
                Spells[card] = Decklist[card]
            if card in AddedNames:
                if "Instant" in Added[AddedNames[card]].TypeLine or "Sorcery" in Added[AddedNames[card]].TypeLine:
                    Spells[card] = Decklist[card]
        # Everything left must be a land.
            if card not in AddedNames and card not in ["Veteran Explorer","Cabal Therapy","Green Sun's Zenith","Ugin, the Spirit Dragon","Nicol Bolas, Planeswalker","Nicol Bolas, God-Pharaoh","Karn Liberated","Elspeth, Sun's Champion","Nicol Bolas, Dragon-God","Curse of Misfortunes","Curse of Death's Hold","Curse of Exhaustion","Overwhelming Splendor","Cruel Reality","Dovescape","Ethereal Absolution","Sandwurm Convergence","Omniscience","Starfield of Nyx"]:
                Lands[card] = Decklist[card]

        if loops == 1:    # Print the decklist to the display if only running 1 loop
            print(DeckName)
            print("Creatures:")
            Printer(Creatures)
            if len(Enchantments) != 0:
                print("Enchantments:")
                Printer(Enchantments)
            if len(Artifacts) != 0:
                print("Artifacts:")
                Printer(Artifacts)
            if len(Planeswalkers) != 0:
                print("Planeswalkers:")
                Printer(Planeswalkers)
            if len(Spells) != 0:
                print("Non-Permanent Spells:")
                Printer(Spells)
            print("Lands:")
            Printer(Lands)
            print("")
            print("Sideboard:")
            Printer(Sideboard)
            print("Jank Score: ", int((JankScore/len(Decklist)) * 12)) # Multiplying by 12 to make it possible to get a jank score of 69
        else: # Write to file if looping multiple times
            File = open("./Output/MTGO/MTGO_Deck" + str(cycles) + ".txt", "w+")  # Also note, that because I'm lazy, you have to make the directories ahead of time.
            Writer(File, Decklist)
            File = open("./Output/Formatted/Title_" + str(cycles) + ".txt", "w+")
            File.write(str(DeckName + " (Jank Score:" + str(int((JankScore/len(Decklist) * 12))) + ")")) # Multiplying by 12 to make it possible to get a jank score of 69
            File.close()
            File = open("./Output/Formatted/Decklist_" + str(cycles) + ".txt", "w+")
            File.write("Creatures: (" + str(count_deck(Creatures)) + ")\n")
            Writer(File, Creatures)
            if len(Enchantments) != 0:
                File.write("\nEnchantments: (" + str(count_deck(Enchantments)) + ")\n")
                Writer(File, Enchantments)
            if len(Artifacts) != 0:
                File.write("\nArtifacts: (" + str(count_deck(Artifacts)) + ")\n")
                Writer(File, Artifacts)
            if len(Planeswalkers) != 0:
                File.write("\nPlaneswalkers: (" + str(count_deck(Planeswalkers)) + ")\n")
                Writer(File, Planeswalkers)
            if len(Spells) != 0:
                File.write("\nSpells: (" + str(count_deck(Spells)) + ")\n")
                Writer(File, Spells)
            File.write("\nLands: (" + str(count_deck(Lands)) + ")\n")
            Writer(File, Lands)
            File.write("\n")
            File.write("\nSideboard: (" + str(count_deck(Sideboard)) + ")\n")
            Writer(File, Sideboard)


        print("Time to Generate (ms): " + str(int(time() * 1000) - Start_Time))
    if loops != 1:
        print("Total Time(ms): " + str(int(time() * 1000) - total_time))

if __name__ == '__main__':
    HowMany = input("How many decks would you like to make? (1 does not create a file) ")
    main(int(HowMany))
    