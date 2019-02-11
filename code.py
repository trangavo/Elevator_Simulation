# STRATEGY 1, TRANG'S VERSION

# This code was written before we agreed on the classes

class Elevator():
    def __init__(self,start_floor,capacity,occupancy):
        self.start_floor = start_floor
        self.capacity = capacity
        self.occupancy = occupancy
class Building():
    def __init__(self,num_floors):
        self.num_floors = num_floors
class Passenger():
    def __init__(self,init_floor,destination,at_destination,in_elevator):
        self.init_floor = init_floor
        self.destination = destination
        self.at_destination = at_destination
        self.in_elevator = in_elevator


import numpy as np        
def strategy_1(start_floor, capacity, num_floors, num_people):
    
    # Create an elevator (object)
    elevator = Elevator(start_floor=start_floor, capacity=capacity, occupancy=0)
    
    # Create a building (object)
    building = Building(num_floors)
    
    # Empty data structure to hold all the people in the building (list)
    people = [] #[Passenger(1,4,0,0),Passenger(2,3,0,0),Passenger(0,1,0,0),Passenger(3,4,0,0)]
    
    # Loop that creates [num_people] number of passengers  
    for i in range(num_people):
        
        # What do these three lines do?
          # Get a random integer between 1 and the number of floors
        init_floor = np.random.randint(0, num_floors)
          # A strategy to get a destination that is different from initial floor        
        f = [x for x in range(0, num_floors) if x != init_floor]
          # Get a random integer between 1 and the number of floors that is different from the initial floor
        destination = np.random.choice(f)
        
        person = Passenger(init_floor=init_floor, destination=destination, at_destination=0, in_elevator=0)
        people.append(person)
      
    # Variable for tracking our progress
    arrived = 0
    
    #print( list(map(atget('init_floor'), people)))
    #print( list(map(atget('destination'), people)))

    
    floor = start_floor
    # number of people who are still waiting
    while arrived != num_people:
        
        # unload the elevator
        #print( list(map(atget('in_elevator'), people)))
        for each in people:
            if each.at_destination == 0 and each.in_elevator == 1 and abs(floor) == each.destination:
                elevator.occupancy -= 1
                each.at_destination = 1
                each.in_elevator = 0
                arrived += 1
                
        if arrived == num_people:
            break
        #load the elevator
        #print( list(map(atget('in_elevator'), people)))
        for each in people:
            #print( list(map(atget('in_elevator'), people)))
            if elevator.occupancy < elevator.capacity and each.at_destination == 0 and abs(floor) == each.init_floor and each.in_elevator == 0:
                elevator.occupancy += 1
                each.in_elevator = 1
        # move the elevator, if reach top, reverse
        if floor == num_floors-1:
            floor = -floor
            floor += 1
        else:
            floor += 1
    return arrived, people, elevator, building


# STRATEGY 3, TRANG'S VERSION

# Braden's code for class definition - used in the official code
class Building():
    def __init__(self, num_floors):
        self.num_floors = num_floors
        

# Create a passenger with a unique location and destination, at_destination is a dummy variable
class Passenger():
    def __init__(self, location, destination, at_destination):
        self.location = location
        self.destination = destination
        self.at_destination = at_destination
        
        
# Create an elevator with locations and a specified capacity, occupants is a list of passengers on the elevator
class Elevator():
    
    def __init__(self, location, capacity):
        self.location = location
        self.capacity = capacity
        self.occupants = []
        
    # Move the elevator up one floor
    def move_up(self):
        self.location += 1
        
    # Move the elevator down one floor
    def move_down(self):
        self.location -= 1
        
    # Move the elevator to a given floor
    def to_floor(self, go_to):
        self.location = go_to
        
    # Unload the elevator
    def unload(self):
        # for each person in the elevator whose destination is the same as the
        # elevator's location, remove them from the elevator and mark their location as "arrived"
        for person in self.occupants:
            if person.destination == self.location:
                person.location =  'arrived'
                self.occupants.remove(person)
    
    # Load the elevator
    def load(self, people):
        # At a certain floor, if there is still space in the elevator,
        # load as many people who are waiting on that floor as possible to the elevator
        if len(self.occupants) < self.capacity:
            queued = [person for person in people if person.location==self.location]
            for person in queued[:(self.capacity-len(self.occupants))]:
                person.location = 'on elevator'
                self.occupants.append(person)
            return
        # If the elevator is full, don't do anything
        elif len(self.occupants) == self.capacity:
            return
        else:
            print('overfull')

# Trang's code from here
from operator import attrgetter
import numpy as np
def strategy_3(start_floor, elev_cap, num_floors, num_people):
    elevator = Elevator(location=start_floor, capacity=elev_cap)
    building = Building(num_floors)
    
    people = []
    
    for i in range(num_people):
        init_floor = np.random.randint(1, num_floors+1)
        f = [x for x in range(1, num_floors+1) if x != init_floor]
        destination = np.random.choice(f)
        
        person = Passenger(location=init_floor, destination=destination, at_destination=0)
        people.append(person)
            
    arrived = 0  
    #print('Locations: ', list(map(attrgetter('location'), people)))
    #print('Destinations: ', list(map(attrgetter('destination'), people)))
    
    stops = 0
    floors_travelled = 0
    while arrived < len(people):
        #print('Locations: ', list(map(attrgetter('location'), people)))
        floor_occurrences = []
        floors = []
            
        if len(elevator.occupants) > 0:
            elevator.unload()#people)
            elevator.load(people)
            stops += 1
            #if len(elevator.occupants) == 0:
            #    break
            for each in people:
                if each.location == "on elevator":
                    floors.append(each.destination)
            for each in range(1, num_floors + 1):
                floor_occurrences.append(floors.count(each))
            count_popular = max(floor_occurrences)
            floor_occurrences = np.array(floor_occurrences)
            popular = np.where(floor_occurrences == count_popular)[0]
            popular = popular.tolist()
            floor_occurrences = floor_occurrences.tolist()
            
            current = elevator.location
            if len(popular) == 1:
                go_to = popular[0] + 1
            else:
                distance = []
                for each in popular:
                    distance.append(abs(each-current))
                go_to = popular[distance.index(min(distance))] + 1
            
            elevator.to_floor(go_to)            
            arrived = np.sum([person.location=='arrived' for person in people])
            floors_travelled += abs(current-go_to)
        else:
            for each in people:
                if each.location != "on elevator" and each.location != "arrived":
                    floors.append(each.location)
            for each in range(1, num_floors + 1):
                floor_occurrences.append(floors.count(each))
            count_popular = max(floor_occurrences)
            floor_occurrences = np.array(floor_occurrences)
            popular = np.where(floor_occurrences == count_popular)[0]
            popular = popular.tolist()
            floor_occurrences = floor_occurrences.tolist()
            
            current = elevator.location
            if len(popular) == 1:
                go_to = popular[0] + 1
            else:
                distance = []
                for each in popular:
                    distance.append(abs(each-current))
                go_to = popular[distance.index(min(distance))] + 1
           
            elevator.to_floor(go_to)
            elevator.load(people)
            stops += 1
            floors_travelled += abs(current-go_to)
            
        if arrived == len(people):
            break
    return people, stops, floors_travelled

def checking(people):
    for each in people:
        if each.location != "arrived":
            return False
    return True

for i in range(1000):
    people, stops, floors_travelled = strategy_3(1, 10, 6, 1000%(i+1))
    print(1000%(i+1), checking(people))
#print('Locations: ', list(map(attrgetter('location'), people)))
#print (stops, floors_travelled)
