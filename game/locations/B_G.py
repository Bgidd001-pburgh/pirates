from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random

class IslandB(location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Rocky_beach(self)
        self.locations["cavern"] = Damp_cavern(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)


class Rocky_beach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['south'] = self
    
    def enter (self):
        display.announce ("Your ship is at anchor in a small bay to the south. You paddle ashore on a small rowboat.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        if (verb == "north"):
            display.announce ("You enter the mysterious looking cavern.")

class Dungeon_map(items.Item):
    def __init__(self):
        super().__init__("dungeon_map", 0)

    def process_verb (self, verb, cmd_list, nouns):
        display.announce(f"{self.nouns} can't {verb}", pause=False)

class Damp_cavern (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "cavern"
        self.rats_present = True
       
        
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            display.announce("You ascend deeper into the cavern")
        if (verb == "south" or "west" or "east"):
            display.announce("You wonder around the perimeter of the island, finding yourself back at your ship.")
        
        

    def enter (self):
        #add another announcement for re-entry
        description = "You notice a squeeking sound that becomes louder the deeper you ascend."
        display.announce(description)
        self.scare_rats()
        if not self.rats_present
    
    def scare_rats(self):
        #ask the question and inform about the rats.
        action = display.get_text_input("")
        if action == "scare":
            while self.rats_present:
                success = random.choice([True, False])
                if success:
                    print("You flail your arms and swing your Cutlass around,/nin an attempt to scare them off.")
                    self.rats_present = False
                    self.find_adventurer()
                else: 
                    print("Your first attempt was unsucessful.")
        
                            

        
    def find_adventurer(self):
         print("As the rats disperse from around you, a forsaken body appears.")
         print("You notice a scroll lodged in their tattered clothing.")
         print("Study the scroll, it reveals the path for the dungeon!")
