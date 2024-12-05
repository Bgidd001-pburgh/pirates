from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random
from game.context import Context
from game.combat import Monster


class IslandB(location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["rockybeach"] = Rocky_beach(self)
        self.locations["cavern"] = Damp_cavern(self)
        self.locations["room"] = Entry_room(self)
        self.starting_location = self.locations["rockybeach"]

    def enter (self, ship):
        display.announce ("arrived at an island with a big cavern.", pause=False)



class Rocky_beach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "rockybeach"
        self.verbs['south'] = self
    
    def enter (self):
        display.announce ("Your ship is at anchor to the south. You paddle ashore on a small rowboat.\nAvoiding the treacherous rocks")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.", pause=False)
            self.main_location.end_visit()
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["cavern"]
        if (verb in ["west", "east"]):
            display.announce("You wonder around the perimeter of the island, finding yourself back at your ship.")

class Dungeon_map(items.Item):
    def __init__(self):
        super().__init__("dungeon-map", 0)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "read"):
         display.announce("Study the scroll, it reveals the path for the dungeon! N:E:N")

class Damp_cavern (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "cavern"
        self.rats_present = True
        self.verbs['scare'] = self
        self.verbs['run'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            display.announce("You find yourself facing a wall.")

        if (verb == "west"):
            display.announce("You ascend deeper into the cavern, and discover a room.")
            config.the_player.next_loc = self.main_location.locations["room"]
            config.the_player.go = True

        if (verb == "east"):
            display.announce("You find yourself facing a wall.")

        if (verb == "south"):
            display.announce("You turn back.")
            config.the_player.next_loc = self.main_location.locations["rockybeach"]

        if (verb == "scare"):
            while self.rats_present:
                success = random.choice([True, False])
                if success:
                    print("You flail your arms and swing your Cutlass around,\nin an attempt to scare them off.")
                    self.rats_present = False
                    self.find_adventurer()
                else: 
                    print("Your first attempt was unsucessful.")
        if (verb == "run"):
            description = "You lack the bravery and walk back to the beach in defeat to regain some courage."
            display.announce(description)
            config.the_player.next_loc = self.main_location.locations["rockybeach"]
            config.the_player.go = True
    

        

    def enter (self):
        #add another announcement for re-entry
        if self.rats_present:
            description = "You notice a squeeking sound that becomes louder the deeper you ascend."
            display.announce(description, pause = False)
            description = "Do you scare them off or turn back?"
            display.announce(description, pause = True)
        if not self.rats_present:
            description = "This looks familiar, You notice nothing has changed since you were last here."
            display.announce(description)

    

        
    def find_adventurer(self):
         display.announce("As the rats disperse from around you, a forsaken body appears.")
         display.announce("You notice a scroll lodged in their tattered clothing.")
         display.announce("Study the scroll, it reveals the path for the dungeon! W:N:E:N")
         #adds to inventory
         config.the_player.add_to_inventory([Dungeon_map()])



class Entry_room(location.SubLocation):#West to get here
    def __init__ (self, m):
        super().__init__(m)
        self.name = "room"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 100
        self.events.append(SkeletonEvent())

    def enter (self):
        description = "Hazy fog filled room with torches that are somehow still lit."
        display.announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "exit" or verb == "leave"):
            config.the_player.next_loc = self.main_location.locations["cavern"]
            config.the_player.go = True
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["armorroom"]
            config.the_player.go = True

class Skeleton(Monster):
    def __init__ (self):
        attacks = {}
        attacks["smash"] = ["smashes",random.randrange(40,90), (5,15)]
        attacks["slash"] = ["slashes",random.randrange(40,90), (5,15)]
        super().__init__("Skeleton", random.randint(25,75), attacks, 15 + random.randint(0, 10))
        self.type_name = "Skeleton" 
class SkeletonEvent(event.Event):

    def __init__ (self):
        self.name = " skeleton attack."

    def process (self, world):
        result = {}
        skeleton = Skeleton()
        display.announce("A skeleton appears to rise from the corner")
        combat.Combat([skeleton]).combat()
        display.announce("The skeleton is once again at rest.")
        result["newevents"] = []
        result["message"] = ""
        return result
    
class Armor_room(location.SubLocation): #North to get here
    def __init__ (self, m):
        super().__init__(m)
        self.name = "armorroom"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['pickup'] = self
        self.verbs['place'] = self
        self.pickedup = []
        self.floor_items = ["bascinet", "byrnie", "chausses", "aegis", "strop", "canthus", "rapier", "katana"]
        self.mannequin_items = []
        self.required_items = ["bascinet", "byrnie", "chausses", "rapier"]
    #list of words picked up, on the floor, on the mannequin. where the value changes. description is based on the state of the lists
    

    def enter (self):   #pickup the armor pieces scattered amongst garbage
        display.announce("Upon entry you notice scattered pieces of armor, 2 statues and one of the two are un-armored.")
    #
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["room"]
        if (verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["door"]
        if verb == "pickup":
            self.pickedup.append()


        #add a comment for when they complete the puzzle(assembling the armor on the statuette, a unlocking sound can be heard to the east.

#class next_loct #east to get here
class Ornate_door(location.SubLocation):
    pass

#class next_loct #north to get here #back to the beach


