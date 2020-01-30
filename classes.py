from collections import deque

class boat:
    def __init__(self, boat_history_limit, boat_ident, first_reported_position):
        self.boat_history_limit = boat_history_limit
        self.identification = boat_ident
        self.latest_position_marker = 0

        if first_reported_position is None:
            self.boat_history = []
        else:
            self.boat_history = [first_reported_position]

    def update_position_history(self, reported_position):
        #the history buffer is full, need to remove oldest entry
        if len(self.boat_history) == self.boat_history_limit:
            #check if most recent is the last element
            self.boat_history.pop(0)

        self.boat_history.append(reported_position)



class base:
    def __init__(self, first_reported_position):
        self.position = first_reported_position

    def update_base_position(self, new_position):
        self.position = new_position
