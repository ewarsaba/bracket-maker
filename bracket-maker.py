import csv
import sys
import random

class Team:
    def __init__(self, seed, name, pyth):
        self.seed = int(seed)
        self.name = str(name)
        self.pyth = float(pyth)
    
    # weighted seeding based on kenpom pyth and seed
    def adjustedSeed(self):
        return int(((16 / self.seed) ** 1) * (self.pyth ** 2) * 1e8)
    
    def __str__(self):
        return str(self.name) + " (" + str(self.seed) + ")"

# randomly generate a winner between these two teams. 
# random number generated between 0 and team1.adjustedSeed + team2.adjustedSeed. 
# if number falls between 0 and team1.adjustedSeed, team1 wins, else team2 wins
def playGame(team1, team2):
    
    seed_total = team1.adjustedSeed() + team2.adjustedSeed()
    
    result = random.randrange(0, seed_total)
    
    winner = team1 if result < team1.adjustedSeed() else team2
    
    print "\t" + str(team1) + " vs. " + str(team2) + "\n\t\twinner: " + str(winner);
    return winner

# only argument is filename
if len(sys.argv) != 2:
    print "usage: bracket-maker.py csv_file"
    sys.exit()

bracket = {}

try:
    
    bracketReader = csv.reader(open(sys.argv[1], 'rb'), delimiter='|', quotechar='"')
    
    current_region = ""

    for row in bracketReader:
        
        # reading in new region
        if (str(row[0]).startswith("--")):
            current_region = str(row[0])
            bracket[current_region] = [0] * 16
        # add new team to bracket
        else:
            team = Team(row[0], row[1], row[2])
            bracket[current_region][team.seed - 1] = team
            
except IOError:
    print "Error reading in file " + sys.argv[1]
    sys.exit(0)

final_four = []

# simulate tournament
for region, teams in bracket.items():
    print region
    
    current_teams = teams
    
    # go through rounds up to final four
    for rnd in range(1, 5):
        winners = []
        print "\n\nround " + str(rnd) + "\n\n"
        
        # pick winners
        for i in range(0, len(current_teams) / 2):
            winners.append(playGame(current_teams[i], current_teams[len(current_teams) - i - 1]))
            
        current_teams = winners;
     
    # add region winner to final four
    final_four.append(winners[0])

finalists = final_four
print "FINAL FOUR " 
for rnd in range(5, 7):
    winners = []
    print "\n\nround " + str(rnd) + "\n\n"
    
    #pick winners
    for i in range(0, len(finalists) / 2):
        winners.append(playGame(finalists[i], finalists[len(finalists) - i - 1]))
    
    finalists = winners;

print "\n\nCHAMPION: " + str(finalists[0])
    
    
