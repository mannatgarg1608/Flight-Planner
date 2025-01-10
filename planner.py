# planner.py
from cmath import inf
from flight import Flight



# i need this object mainly because i need to have track of each path and again and again copying it could result in complexity problems
class city :
    # this city class has variables that i could need in any one of the three cases 
    def __init__(self,flight_arrival_time,minimum_cost,number_flight,flight,previous,current_city):
        self.flight_arrival=flight_arrival_time     # it is the current time
        self.minimum_cost =minimum_cost              # it is for keeping record of cost for that city with that flight reaching
        self.number_flight =number_flight           # it keeps record for number of flights
        self.flight =flight                        # it keeps flight taken to reach that city
        self.previous_object = previous          # previous to trace paths
        self.current_city = current_city         #  my present city

class Planner:
    def __init__(self, flights):
        self.flights =flights
        self.length= 2*len(self.flights)
        self.cities = [None]*(2*len(flights))
        for flight in flights :
            if self.cities[flight.start_city] is None :
                self.cities[flight.start_city]=[]
            self.cities[flight.start_city].append(flight)
        


# in this i starting from start city , ia m traversing through bfs
 
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        # returning empty list if start city is eual to end city
        if start_city == end_city:
            return []
        
       # this is my queue , i have created queue using a linked list to avid all the issues of length and make it simpler 
        tracking_paths =Queue()
        tracking_paths.enqueue(city(t1,0,0,None,None,start_city))
        # minimum_flights records my flights for end city

        minimum_flights =float('inf')
        # records earliest time to reach end city
        earliest_arrival =float('inf')
        # this stores the best final object of the  end city
        final_ans_stored= None
        flight_list =[0]*(len(self.flights))
        
        while not tracking_paths.isEmpty() :
            main_data= tracking_paths.dequeue()
            
         # the queue will always have flights in order of the number_of flights since we are traversing that way 
         # this means the first encounter would give us least number of fights 
            if main_data.number_flight > minimum_flights:
                break
           # we traverse further to get the least cost
            if main_data.current_city == end_city :
                if main_data.number_flight <= minimum_flights:
                    minimum_flights= main_data.number_flight
                    if main_data.flight_arrival < earliest_arrival:
                        earliest_arrival=main_data.flight_arrival
                        final_ans_stored= main_data

        # we now traverse each flight from the popped out city object
            if self.cities[main_data.current_city] is not None :
                for flights in self.cities[main_data.current_city] :
                    if flight_list[flights.flight_no] ==1:
                        continue
                    # we check for all valid reasons fpr that flight checking for differnce of 20 minutes ,it lying between t1 and t2
                    if (flights.departure_time >= main_data.flight_arrival + 20 or main_data.flight_arrival ==t1) and flights.departure_time >= t1 and flights.arrival_time <=t2 :
                        # we dont need to reinsert a flight
                        flight_list[flights.flight_no] = 1
                        tracking_paths.enqueue(city(flights.arrival_time,0,main_data.number_flight +1,flights,main_data,flights.end_city))
            
        # after complete traversal we recahed to the best path according to our condition
        path =[]
        if final_ans_stored == None:
            return []
        else:
            while final_ans_stored is not None:
                if final_ans_stored.flight is not None :
                    path.append(final_ans_stored.flight)
                final_ans_stored= final_ans_stored.previous_object
        
        path.reverse()
        return path


# this is my comparison basis i have my cost to reach that place as the comparator basis
    def comparison_function( self,element_1,element_2):
        if element_1.minimum_cost > element_2.minimum_cost:
            return 0
        elif element_1.minimum_cost <= element_2.minimum_cost:
            return 1

        pass

# for this i have used dijkstra algorithm to tace through the cheapest path
    def cheapest_route(self, start_city, end_city, t1, t2):
        if start_city == end_city:
            return []

# this my heap in which i am insering my object
        traversing_heap = Heappq(self.comparison_function,[])
        traversing_heap.insert(city(t1,0,0,None,None,start_city))
        # this list prevents from reinserting the same flight
        flights_list = [0]*(len(self.flights))
        # this is to keep my final best element
        cheapest_route =None
        # it keeps recprd of minimum cost for end city
        minimum_value = float('inf')


        while not traversing_heap.is_empty():
            element = traversing_heap.extract()
            # getting element from heap
            
            cost_of_travel = element.minimum_cost
            present_city =element.current_city
            current_time =element.flight_arrival
     
          # if i reach the end city i keep record of the minimum cost and the point where i got it 
            if present_city == end_city:
                if element.minimum_cost < minimum_value:
                    minimum_value = element.minimum_cost
                    cheapest_route = element

          # here i cant use the break statement as in two other cases since here we have to travesr complete heap to get best cost 
            if self.cities[present_city] is None :
                continue
          # traversing through flights of each city extracted out
            for flights in self.cities[present_city]:
                if flights_list[flights.flight_no] == 1:
                    continue 
            # checks all condition for my flight to be valid
                if (flights.departure_time >= element.flight_arrival + 20 or element.flight_arrival ==t1) and (flights.departure_time >= t1) and  (flights.arrival_time <=t2) :
                    flights_list[flights.flight_no] = 1
                    traversing_heap.insert(city(flights.arrival_time,element.minimum_cost + flights.fare,element.number_flight +1,flights,element,flights.end_city))

        # got my final element and now getting a path form it by traversing backwards through it 
        path =[]
        if cheapest_route == None:
            return []
        else:
            while cheapest_route is not None:
                if cheapest_route.flight is not None :
                    path.append(cheapest_route.flight)
                cheapest_route= cheapest_route.previous_object
        
        path.reverse()
        return path

  # this is my comparator which first sorts on basis of flight number and then on cost to reach that place 
    def comparison_function_2(self,element_1,element_2):
        if element_1.number_flight > element_2.number_flight:
            return 0
        elif element_1.number_flight < element_2.number_flight:
            return 1
        else:
            if element_1.minimum_cost > element_2.minimum_cost:
                return 0
            elif element_1.minimum_cost <= element_2.minimum_cost:
                return 1
            
    # i am using dijkstra algorithm to obtain the best route for given condition
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        # returning empty list for start city beingsame as end city
        if start_city == end_city:
            return []
        # this si my heaop and i am inserting my city object in it
        traversing_heap = Heappq(self.comparison_function_2,[])
        traversing_heap.insert(city(t1,0,0,None,None,start_city))
        
        flights_list = [0]*(len(self.flights))
       # the above list prevents me to reinsert the same lfight
       
       # this keeps record for my final path and minimum flights for the last city 
        final_output = None
        minimum_end_cost = float('inf')
        minimum_end_flights= float('inf')


        while  not traversing_heap.is_empty():
            element = traversing_heap.extract()

            no_of_flights =element.number_flight
            cost_of_travel = element.minimum_cost
            present_city =element.current_city
            current_time =element.flight_arrival
            # here i can use this break condition since 
            # we can see that we are traversing so we always get the less number of flights one before more number one

            if no_of_flights > minimum_end_flights:
                break

            # recording for best city everytime we reach best city
            if present_city == end_city:
                if no_of_flights < minimum_end_flights:
                    final_output =element
                    minimum_end_flights=no_of_flights
                    minimum_end_cost = cost_of_travel
                elif no_of_flights == minimum_end_flights:
                    if  cost_of_travel <= minimum_end_cost:
                        final_output =element
                        minimum_end_cost = cost_of_travel

            # now here i am going through each flight of city extracted 
            if self.cities[present_city] is not None :
                for flights in self.cities[present_city]:
                    # preventing from enetering same flight again
                    if flights_list[flights.flight_no] ==1:
                        continue
                    # here i check for all avlid conditions for that flight being in given intervala nd 20 minutes diffrence
                    if (flights.departure_time >= current_time + 20 or current_time ==t1) and flights.departure_time >= t1 and flights.arrival_time <=t2 :
                        
                        if flights_list[flights.flight_no]==0:
                            flights_list[flights.flight_no]=1
                          #inserting in heap  
                        traversing_heap.insert(city(flights.arrival_time,element.minimum_cost + flights.fare,element.number_flight +1,flights,element,flights.end_city))
        

       # now i got my final eleemnt and now i will traverse my compleet path backwards
        
        path =[]
        if final_output == None:
            return []
        else:
            while final_output is not None:
                if final_output.flight is not None :
                    path.append(final_output.flight)
                final_output= final_output.previous_object
        
        path.reverse()
        return path
    


class Node:
    def __init__(self, data):
        self.main_data = data
        self.next = None
# i have implemented queue using the linked list
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    

    # performs addition of element
    def enqueue(self, element):
        new_node = Node(element)

        if self.tail is None:
            self.length = self.length + 1
            self.head =  new_node
            self.tail =new_node
            return
        
        self.tail.next = new_node
        self.tail = new_node
        self.length = self.length + 1

    # it removes the very first element amd updates the hwead and return the value 
    
    def dequeue(self):
        if self.isEmpty():
            return "empty queue"
        
        temp=self.head
        self.head= self.head.next
        self.length= self.length -1
        if self.head is None:
            self.tail = None


        return temp.main_data

    def size(self):
        return self.length
  
    def isEmpty(self):
        return self.length == 0
    


class Heappq:
    def __init__(self, comparison_function, init_array):
       
        #comparison function
        self.comparison_function = comparison_function  
        self.heap = list(init_array)
        #calling self.build to form the hap from the array as array might not be in from of arranged heap
        self.build_heap()

    
    def build_heap(self):
     # Start from the last non-leaf node and heapify down to the root   
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self.heapify_down(i)

    def size(self):
        #returns number of elements in heap
        return len(self.heap)
    
    def heapify_down(self, index):
        #heapify down the elemnet at given index
        size = len(self.heap)
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        
         # Compare with left child
        if left < size and self.comparison_function(self.heap[left], self.heap[smallest]):
            smallest = left
        
        # Compare with right child
        if right < size and self.comparison_function(self.heap[right], self.heap[smallest]):
            smallest = right
        
        # If the smallest is not the current index, swap and continue heapifying down
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.heapify_down(smallest)
    
    def heapify_up(self, index):
       
        #heapify the element up at a given index
        parent = (index - 1) // 2
         # If the current element is smaller than its parent, swap them
        if index > 0 and self.comparison_function(self.heap[index], self.heap[parent]):
            # Swap the current element with its parent
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            # Heapify up recursively
            self.heapify_up(parent)
    
    def insert(self, value):
      
        #add the value at last of heap 
        self.heap.append(value)
        #shift the elemnt up to maintain the minimum property
        self.heapify_up(len(self.heap) - 1)
        
    
    def extract(self):
        
        
        #heap is empty
        if len(self.heap) == 0:
            return None 
        
        # the minimum element
        root = self.heap[0]
        
     #move element to last to remove it 
        self.heap[0] = self.heap[-1]
        self.heap.pop()  
        
        # Heapify down to maintain the heap
        self.heapify_down(0)
        
        return root
    
    def top(self):
        
        if len(self.heap) == 0:
            return None  
        
        return self.heap[0]
    
   
    def is_empty(self):
        return len(self.heap) == 0
    
    def print(self):
        print(self.heap)
