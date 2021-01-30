import scrython

# Generates a list of objects for use in the brewing script
# Reads from a file listing Jankiness rating, Min Count, Max Count, and Card Name (in that order, separated by a space)
# Queries Scryfall for the information (color, name, etc))
# Writes it to a new file with ALL the info from Scryfall, which will be ingested in the brewing script

def Ingest(text_file):
    List = []
    with open(text_file) as file:
        for line in enumerate(file):
            split = line[1].split(" ", 3)
            card_name = split[3].replace("\n", "")
            JankScore = split[0]
            MinCount = split[1]
            MaxCount = split[2]
            Card_tuple = [card_name, MinCount, MaxCount, JankScore]
            List.append(Card_tuple)
    return(List)

List = Ingest('Input.txt')
# print(Test_Dict)
file1 = open("Card_Database.txt","a")
for card in List:
    print(card)
    Card_obj = scrython.cards.Named(exact=card[0])
    Colors = Card_obj.color_identity()
    if "Snow" in Card_obj.type_line() or card[0] == "Dead of Winter": 
        # If adding more snow-related cards without the snow SuperType, will need to add special exceptions for them here too.
        # For now, this is just a one-off issue.
        Snow = "S"
    else:
        Snow = " "
    Typeline = str(Card_obj.type_line())
    minC = card[1]
    maxC = card[2]
    Jank = card[3]
    output = card[0] + "|" + Jank + "|" + minC + "|" + maxC + "|" + Snow + "|" + Typeline + "|" + "|".join(map(str, Colors)) + "\n"
    file1.write(output)
file1.close()