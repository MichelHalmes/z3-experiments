"""
Entities

    There are five houses in unique colors: Blue, green, red, white and yellow.
    In each house lives a person of unique nationality: British, Danish, German, Norwegian and Swedish.
    Each person drinks a unique beverage: Beer, coffee, milk, tea and water.
    Each person smokes a unique cigar brand: Blue Master, Dunhill, Pall Mall, Prince and blend.
    Each person keeps a unique pet: Cats, birds, dogs, fish and horses.

Constraints
    The Brit lives in a red house.
    The Swede keeps dogs as pets.
    The Dane drinks tea.
    The green house is on the left of the white, next to it.
    The green house owner drinks coffee.
    The person who smokes Pall Mall rears birds.
    The owner of the yellow house smokes Dunhill.
    The man living in the house right in the center drinks milk.
    The Norwegian lives in the first house.
    The man who smokes blend lives next to the one who keeps cats.
    The man who keeps horses lives next to the man who smokes Dunhill.
    The owner who smokes Blue Master drinks beer.
    The German smokes Prince.
    The Norwegian lives next to the blue house.
    The man who smokes blend has a neighbor who drinks water.


"""

from z3 import Solver, sat, Int, Distinct, And, Or

# Stating our unknown variables
COLOR_H = {"blue": Int("blue"), "green": Int("green"), "red": Int("red"), "white": Int("white"), "yellow": Int("yellow")}
NATIONALITY_H = {"british": Int("british"), "danish": Int("danish"), "german": Int("german"), "norwegian": Int("norwegian"), "swedish": Int("swedish")}
DRINK_H = {"beer": Int("beer"), "coffee": Int("coffee"), "milk": Int("milk"), "tea": Int("tea"), "water": Int("water")}
CIGAR_H = {"blue_master": Int("blue_master"), "dunhill": Int("dunhill"), "pall_mall": Int("pall_mall"), "prince": Int("prince"), "blend": Int("blend")}
PET_H = {"cats": Int("cats"), "birds": Int("birds"), "dogs": Int("dogs"), "fish": Int("fish"), "horses": Int("horses")}

GROUPS = [COLOR_H, NATIONALITY_H, DRINK_H, CIGAR_H, PET_H]

# House number are in [1, 5]
numbers = [And(house >= 1, house <= 5) for group in GROUPS for house in group.values()]
# House numbers are uniquely assigned in each group
unique = [Distinct(list(group.values())) for group in GROUPS]

def are_neighbors(house_a, house_b):
    return Or(house_a + 1 == house_b, house_a - 1 == house_b)

# Known facts
facts = [
    NATIONALITY_H["british"] == COLOR_H["red"],
    NATIONALITY_H["swedish"] == PET_H["dogs"],
    NATIONALITY_H["danish"] == DRINK_H["tea"],
    COLOR_H["green"] + 1 == COLOR_H["white"],
    COLOR_H["green"] == DRINK_H["coffee"],
    CIGAR_H["pall_mall"] == PET_H["birds"],
    COLOR_H["yellow"] == CIGAR_H["dunhill"],
    DRINK_H["milk"] == 3,
    NATIONALITY_H["norwegian"] == 1,
    are_neighbors(CIGAR_H["blend"], PET_H["cats"]),
    are_neighbors(PET_H["horses"], CIGAR_H["dunhill"]),
    CIGAR_H["blue_master"] == DRINK_H["beer"],
    NATIONALITY_H["german"] == CIGAR_H["prince"],
    are_neighbors(NATIONALITY_H["norwegian"], COLOR_H["blue"]),
    are_neighbors(CIGAR_H["blend"], DRINK_H["water"]),
]

s = Solver()
s.add(facts + numbers + unique)
print(s.check())
m = s.model()
sol = [nat for nat in NATIONALITY_H.values() if m[nat] == m[PET_H["fish"]]][0]
print("Who keeps fish:", sol)

