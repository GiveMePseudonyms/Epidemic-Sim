class Person:
    def __init__(self, is_vaccinated, is_infected, is_masked):
        self.is_vaccinated = is_vaccinated
        self.is_infected = is_infected
        self.is_masked = is_masked
        self.chance_of_infection = 0
        self.location = None

        self.infectivity = 0
        self.susceptibility = 0

        self.days_since_infection = 0

        self.is_recovered = False
        self.days_since_recovery = 0
        self.valid_location = True

    def infect(self):
        self.is_infected = True
        self.is_recovered = False
        self.days_since_infection = 0

    def recover(self):
        self.is_infected = False
        self.is_recovered = True
        self.days_since_recovery = 0

    def calculate_infectivity(self, rules):
        if not self.is_infected:
            self.infectivity = 0
            return

        if self.is_infected:
            prevention_measures = 1
            if self.is_masked:
                prevention_measures *= rules['face mask efficacy']
            
            self.infectivity = float(rules['virus infectivity'] * prevention_measures)
            return
    
    def progress_infection(self, rules):
        if self.is_infected and self.days_since_infection <= rules['infection duration']:
            self.days_since_infection += 1
            self.susceptibility = 0
            return

        if self.is_infected and self.days_since_infection > rules['infection duration']:
            self.recover()
            self.susceptibility = 0
            return

        if self.is_recovered and self.days_since_recovery <= rules['post-recovery immunity period']:
            self.days_since_recovery += 1
            self.susceptibility = 0
            return

        if self.is_recovered and self.days_since_recovery > rules['post-recovery immunity period']:
            self.days_since_recovery = 0
            self.is_recovered = False

    def calculate_susceptibility(self, rules):
        if self.is_infected and self.days_since_infection <= rules['infection duration']:
            self.days_since_infection += 1
            self.susceptibility = 0
            return

        if self.is_infected and self.days_since_infection > rules['infection duration']:
            self.recover()
            self.susceptibility = 0
            return

        if self.is_recovered and self.days_since_recovery <= rules['post-recovery immunity period']:
            self.days_since_recovery += 1
            self.susceptibility = 0
            return

        if self.is_recovered and self.days_since_recovery > rules['post-recovery immunity period']:
            self.days_since_recovery = 0
            self.is_recovered = False

        prevention_measures = 1
        if self.is_masked:
            prevention_measures *= rules['face mask efficacy']

        if self.is_vaccinated:
            prevention_measures *= rules['vaccination efficacy']
        
        self.susceptibility = float(rules['virus infectivity'] * prevention_measures)