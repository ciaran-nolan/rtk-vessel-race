class boat:
    def __init__(self, boat_history_limit, boat_ident, first_reported_position):
        self.boat_history_limit = boat_history_limit
        self.identification = boat_ident
        self.boat_history = [first_reported_position]


class base:
    def __init__(self, first_reported_position):
        self.position = first_reported_position

    def update_base_position(self, new_position):
        self.position = new_position
