import random

class Person:
    def __init__(self, is_vaccinated, is_infected, is_masked, rules):

        self.is_vaccinated = is_vaccinated
        self.is_infected = is_infected
        if self.is_infected:
            self.infect(rules)

        self.is_masked = is_masked
        self.chance_of_infection = 0
        self.location = None

        self.infectivity = 0
        self.susceptibility = 0

        self.days_since_infection = 0

        self.is_recovered = False
        self.days_since_recovery = 0
        self.valid_location = True

        self.is_dead = False

    def infect(self, rules):
        self.is_infected = True
        self.is_recovered = False
        self.days_since_infection = 0

        rule_infection_duration = rules['infection duration']
        rule_infection_duration_variance = rules['infection duration variance']
        
        infection_duration = random.randint(rule_infection_duration - rule_infection_duration_variance, 
                                            rule_infection_duration + rule_infection_duration_variance)
        while infection_duration <= 0:
            infection_duration = random.randint(rule_infection_duration - rule_infection_duration_variance, 
                                                rule_infection_duration + rule_infection_duration_variance)
        
        self.infection_duration = infection_duration

    def vaccinate(self):
        self.days_since_vaccination = 0
        self.days_since_recovery = 0
        self.is_recovered = False
        self.is_vaccinated = True
    
    def unvaccinate(self):
        self.is_vaccinated = False

    def recover(self, rules):
        self.is_infected = False
        self.is_recovered = True
        self.days_since_recovery = 0

        rule_post_recovery_immunity_period = rules['post-recovery immunity period']
        rule_post_recovery_immunity_period_variance = rules['post-recovery immunity period variance']

        recovery_immunity_period = random.randint(rule_post_recovery_immunity_period - rule_post_recovery_immunity_period_variance,
                                                    rule_post_recovery_immunity_period + rule_post_recovery_immunity_period_variance)
        
        while recovery_immunity_period <=0:
                recovery_immunity_period = random.randint(rule_post_recovery_immunity_period - rule_post_recovery_immunity_period_variance,
                                                            rule_post_recovery_immunity_period + rule_post_recovery_immunity_period_variance)

        self.recovery_immunity_period = recovery_immunity_period

    def die(self):
        self.is_dead = True

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
    
    def calculate_susceptibility(self, rules):
        if self.is_infected and self.days_since_infection <= self.infection_duration:
            self.susceptibility = 0
            return

        if self.is_infected and self.days_since_infection > self.infection_duration:
            self.susceptibility = 0
            return

        if self.is_recovered and self.days_since_recovery <= self.recovery_immunity_period:
            self.susceptibility = 0
            return

        if self.is_recovered and self.days_since_recovery > self.recovery_immunity_period:
            self.days_since_recovery = 0
            self.is_recovered = False

        prevention_measures = 1
        if self.is_masked:
            prevention_measures *= rules['face mask efficacy']

        if self.is_vaccinated:
            prevention_measures *= rules['vaccination efficacy']
        
        self.susceptibility = float(rules['virus infectivity'] * prevention_measures)

    def progress_infection(self, rules):
        if self.is_infected and self.days_since_infection <= self.infection_duration:
            self.days_since_infection += 1
            self.susceptibility = 0
            return

        if self.is_infected and self.days_since_infection > self.infection_duration:
            if random.randint(1, 100) <= rules['mortality %']:
                self.die()
                return
            else:
                self.recover(rules)
                self.susceptibility = 0
                return

        if self.is_recovered and self.days_since_recovery <= self.recovery_immunity_period:
            self.days_since_recovery += 1
            self.susceptibility = 0
            return

        if self.is_recovered and self.days_since_recovery > self.recovery_immunity_period:
            self.days_since_recovery = 0
            self.is_recovered = False

    def progress_vaccination(self):
        pass