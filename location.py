class Location:
    def __init__(self):
        self.people = []
        self.total_location_infection_chance = 0
        self.infectivity = 0

    def add_person(self, person):
        self.people.append(person)

    def calculate_infectivity(self):
        self.infectivity = 0

        for person in self.people:
            if person.is_infected:
                self.infectivity += person.infectivity
        return