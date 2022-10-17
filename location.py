class Location:
    def __init__(self):
        self.people = []
        self.total_location_infection_chance, self.infectivity = 0, 0

    def add_person(self, person):
        self.people.append(person)

    def calculate_infectivity(self):
        self.infectivity = 0

        for person in self.people:
            self.infectivity += person.infectivity
        return

    def check_if_valid(self):
        has_infected, has_healthy = None, None
        for person in self.people:
            if person.is_infected:
                has_infected = True
            if not person.is_infected:
                has_healthy = True

            if has_healthy is True and has_healthy is True:
                for person in self.people: person.valid_location = True
                self.valid = True
                return
                
        for person in self.people: person.valid_location = False

        self.valid = False
        return