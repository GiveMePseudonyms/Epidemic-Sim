class Location:
    def __init__(self):
        self.people = []
        self.total_location_infection_chance = 0

    def add_person(self, person):
        self.people.append(person)

    def calculate_total_infection_chance(self, virus_infectivity_rate):
        self.infected_people = []

        for person in self.people:
            if person.is_infected:
                self.infected_people.append(person)
        
        infectivity_list = []
        for person in self.infected_people:
            infectivity_list.append(person.calculate_infectivity(virus_infectivity_rate))

        self.total_location_infection_chance = sum(infectivity_list)