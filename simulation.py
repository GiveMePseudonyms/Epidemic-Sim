import tkinter
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from person import Person
from location import Location
import random
from ruleset import rules
import math
from dataobject import DataObject

class Simulation:
    def __init__(self):
        self.WINDOW = tkinter.Tk()
        self.WINDOW.title('Simulation')
        self.WINDOW.geometry('500x700+800+400')

        padx = 20
        pady = 20

        self.settings_frame = tkinter.Frame(self.WINDOW)
        self.settings_frame.grid(column=0, row=0, padx=padx, pady=pady)

        self.graph_frame = tkinter.Frame(self.WINDOW)
        self.graph_frame.grid(column=1, row=0, padx=padx, pady=pady)
        
        self.pad_frame = tkinter.Frame(self.WINDOW)
        self.pad_frame.grid(column=0, row=2, pady=20, padx=padx)
        
        self.action_frame  = tkinter.Frame(self.WINDOW)
        self.action_frame.grid(column=0, row=3, padx=padx)

        self.padding = ttk.Label(self.pad_frame ,text='')

        self.settings_widgets = self.create_widgets('settings')
        for widget in self.settings_widgets:
            widget.grid(column=0, row=self.settings_widgets.index(widget))

        self.action_widgets = self.create_widgets('action')
        for widget in self.action_widgets:
            widget.pack(anchor=tkinter.S)

        self.initial_run = True

        self.people = []

        self.stats = DataObject()

        self.WINDOW.mainloop()

    def create_widgets(self, widget_type):
        if widget_type == 'settings':   
            self.lbl_spn_num_people = ttk.Label(self.settings_frame, text='Number of people')
            self.entry_num_people = ttk.Entry(self.settings_frame)

            self.lbl_number_of_infected = ttk.Label(self.settings_frame, text='Number of infected')
            self.entry_number_of_infected = ttk.Entry(self.settings_frame)

            self.lbl_number_of_locations = ttk.Label(self.settings_frame, text='Number of locations')
            self.entry_number_of_locations = ttk.Entry(self.settings_frame)

            self.lbl_scale_virus_infectivity = ttk.Label(self.settings_frame, text='Virus infectivity')
            self.scale_virus_infectivity = tkinter.Scale(self.settings_frame, from_=0, to=100, orient=tkinter.HORIZONTAL, length=200)

            self.lbl_post_recover_immunity_period = ttk.Label(self.settings_frame, text='Post-recovery immunity period')
            self.entry_post_recovery_immunity_period = ttk.Entry(self.settings_frame)

            self.lbl_post_recovery_immunity_period_variance = ttk.Label(self.settings_frame, text='Post-recovery immunity period variance')
            self.spn_post_recovery_immunity_period_variance = ttk.Spinbox(self.settings_frame, from_=0, to=20)

            self.lbl_infection_duration = ttk.Label(self.settings_frame, text='Infection duration')
            self.entry_infection_duration = ttk.Entry(self.settings_frame)

            self.lbl_infection_duration_variance = ttk.Label(self.settings_frame, text='Infection duration variance')
            self.spn_infection_duration_variance = ttk.Spinbox(self.settings_frame, from_=0, to=20)
            
            settings_widgets = [
                self.lbl_spn_num_people, self.entry_num_people,
                self.lbl_number_of_infected, self.entry_number_of_infected,
                self.lbl_number_of_locations, self.entry_number_of_locations,
                self.lbl_scale_virus_infectivity, self.scale_virus_infectivity,
                self.lbl_post_recover_immunity_period, self.entry_post_recovery_immunity_period,
                self.lbl_post_recovery_immunity_period_variance, self.spn_post_recovery_immunity_period_variance,
                self.lbl_infection_duration, self.entry_infection_duration,
                self.lbl_infection_duration_variance, self.spn_infection_duration_variance,
            ]
            return settings_widgets

        if widget_type == 'action':
            self.lbl_spn_days_to_sim = ttk.Label(self.action_frame, text='Days to simulate')
            self.spn_days_to_sim = ttk.Spinbox(self.action_frame, from_=1, to=99999)

            self.btn_show_data = ttk.Button(self.action_frame, text='Show data', command=lambda: self.show_data())

            self.btn_start = ttk.Button(self.action_frame, text='Start', command=lambda: self.start())

            action_widgets = [
                self.lbl_spn_days_to_sim, self.spn_days_to_sim,
                self.btn_show_data,
                self.btn_start,
            ]
            
            return action_widgets

    def throw_exception(self, exception, source, remedy):
        print(
            f"""Error thrown:

            Source: {source}

            Error: {exception}

            Remedy: {remedy}

            """
        )

        messagebox.showwarning(title='Error!', 
        message=f'''
                Error raised from: {source}

                Error: {str(exception)}

                {remedy}
                ''')

    def calculate_chance_of_infection(self, person, location):
        return float(person.susceptibility * location.infectivity * 100)

    def step(self, steps):
        self.initial_run = False
        for _ in range(1, steps + 1):
            total_infected = 0

            for person in self.people:
                if person.is_infected:
                    total_infected += 1
            if total_infected != 0:

                num_locations = rules['number of locations']
                locations_list = []

                for x in range(0, num_locations):
                    locations_list.append(Location())

                for person in self.people:
                    location_index = random.randint(0, num_locations -1)
                    locations_list[location_index].add_person(person)
                    person.location = location_index
                    
                for location in locations_list:
                    # a location is NOT valid is all people in it are infected or all people in it are healthy, 
                    # since the outcome is deterministic in those cases
                    location.check_if_valid()

                for person in self.people:
                    if person.valid_location:
                        person.calculate_infectivity(rules)
                        person.calculate_susceptibility(rules)
                    else:
                        if person.is_infected:
                            person.progress_infection(rules)

                for location in locations_list:
                    if location.valid:
                        location.calculate_infectivity()

                for location in locations_list:
                    if location.valid:
                        for person in location.people:
                            if person.susceptibility > 0:
                                chance_of_infection = self.calculate_chance_of_infection(person, location)
                                rnd = random.uniform(1, 100)
                                if rnd <= chance_of_infection:
                                    person.infect(rules)
                            else: pass
                    
                total_infected = 0
                total_healhty = 0
                total_vaccinated = 0
                total_recovered = 0
                for person in self.people:
                    if person.is_infected:
                        total_infected += 1
                    if not person.is_infected and not person.is_recovered:
                        total_healhty += 1
                    if person.is_recovered:
                        total_recovered += 1
                    if person.is_vaccinated:
                        total_vaccinated += 1

                print(f'Day{len(self.stats.days)}: {total_infected}/{len(self.people)} are infected.')

                self.stats.days.append(len(self.stats.days))
                self.stats.total_healthy.append(total_healhty)
                self.stats.total_infected.append(total_infected)
                self.stats.total_recovered.append(total_recovered)
                self.stats.total_vaccinated.append(total_vaccinated)
            
        self.show_data()

    def show_data(self):
        palette = ['#b52b2b', '#2b72b5', '#4dbf6d', '#e3fa95']
        plt.stackplot(1, 1)
        plt.clf()
        plt.stackplot(
            self.stats.days, self.stats.total_infected, self.stats.total_healthy, self.stats.total_vaccinated, self.stats.total_recovered,
            labels=['Total Infected', 'Total Healthy & Vulerable', 'Total Vaccinated', 'Total Recovered Immune'],
            colors=palette)
        plt.title('Epidemic Sim')
        plt.legend(loc='upper left')
        plt.show()

    def validate_options(self):
        try:
            int(self.entry_num_people.get())
        except Exception as exc:
            self.throw_exception(exc, 'Number of people spinner.', 'Please enter an integer.')
            return False

        try:
            int(self.entry_number_of_infected.get())
        except Exception as exc:
            self.throw_exception(exc, 'Number of infected spinner.', 'Please enter an integer.')
            return False

        if int(self.entry_number_of_infected.get()) > int(self.entry_num_people.get()):
            self.throw_exception('Invalid data.', 
                                'More infected than healthy people!', 
                                'The number of infected must be lower than the total number of people!')
            return False

        try:
            int(self.entry_number_of_locations.get())
        except Exception as exc:
            self.throw_exception(exc, 'Number of locations spinner.', 'Please enter an integer.')
            return False
        
        try:
            days_to_sim = int(self.spn_days_to_sim.get())
        except Exception as exc:
            self.throw_exception(exc, 'Days to sim spinner.', 'Please enter an integer.')
            return False

        try:
            int(self.entry_number_of_locations.get())
        except Exception as exc:
            self.throw_exception(exc, 'Number of locations spinner.', 'Please enter an integer.')
            return False

        try:
            int(self.scale_virus_infectivity.get())
        except Exception as exc:
            self.throw_exception(exc, 
                                'Virus infectivity scale.', 
                                'Please select an integer... Not even sure how you broke this setting...')

        try:
            int(self.entry_infection_duration.get())
        except Exception as exc:
            self.throw_exception(exc, 'Infection duration.', 'Please enter an integer.')
            return False

        try:
            int(self.entry_post_recovery_immunity_period.get())
        except Exception as exc:
            self.throw_exception(exc, 'Post-recovery immunity period.', 'Please enter an integer.')
            return False

        try:
            int(self.spn_infection_duration_variance.get())
        except Exception as exc:
            self.throw_exception(exc, 'Infection duration variance spinner', 'Please enter an integer.')
            return False

        try:
            int(self.spn_post_recovery_immunity_period_variance.get())
        except Exception as exc:
            self.throw_exception(exc, 'Post-recover immunity period variance spinner', 'Please enter an integer.')

        return True


    def start(self):
        if self.validate_options():
            total_people = int(self.entry_num_people.get())
            num_infected = int(self.entry_number_of_infected.get())
            num_healhty = total_people - num_infected

            if self.initial_run:
                for _ in range(0, num_healhty):
                    person = Person(is_vaccinated=False, is_infected=False, is_masked=False, rules=rules)
                    self.people.append(person)
                
                for _ in range(0, num_infected):
                    person = Person(is_vaccinated=False, is_infected=True, is_masked=False, rules=rules)
                    self.people.append(person)

                self.btn_start['text'] = 'Continue'
                self.entry_num_people.config(state='disabled')
                self.entry_number_of_infected.config(state='disabled')
                self.initial_run = False

            rules['number of locations'] = int(self.entry_number_of_locations.get())
            rules['virus infectivity'] = float(self.scale_virus_infectivity.get()/100)
            rules['infection duration'] = int(self.entry_infection_duration.get())
            rules['infection duration variance'] = int(self.spn_infection_duration_variance.get())
            rules['post-recovery immunity period'] = int(self.entry_post_recovery_immunity_period.get())
            rules['post-recovery immunity period variance'] = int(self.spn_post_recovery_immunity_period_variance.get())

            days_to_sim = int(self.spn_days_to_sim.get())
            self.step(days_to_sim)

if __name__ == '__main__':
    simulation = Simulation()