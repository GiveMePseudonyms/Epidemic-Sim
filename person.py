class Person:
    def __init__(self, is_vaccinated, is_infected, is_masked):
        self.is_vaccinated = is_infected
        self.is_infected = is_infected
        self.is_masked = is_masked
        self.chance_of_infection = 0
        self.location = None

        self.infectivity = 0
        self.susceptibility = 0

    def infect(self):
        self.is_infected = True

    def calculate_infectivity(self, virus_infection_rate):
        prevention_measures = 1
        if self.is_masked:
            prevention_measures *= 0.1
        
        self.infectivity = virus_infection_rate * prevention_measures
        return self.infectivity

    def calculate_susceptibility(self, virus_infectivity):
        prevention_measures = 1
        if self.is_masked:
            prevention_measures *= 0.1
        
        self.susceptibility = virus_infectivity * prevention_measures
        return self.susceptibility