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
        self.WINDOW.geometry('500x500+400+400')

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
            self.spn_num_people = ttk.Spinbox(self.settings_frame, from_=1, to=rules['max people'])

            self.lbl_number_of_infected = ttk.Label(self.settings_frame, text='Number of infected')
            self.spn_number_of_infected = ttk.Spinbox(self.settings_frame, from_=1, to=rules['max people'])

            self.lbl_number_of_locations = ttk.Label(self.settings_frame, text='Number of locations')
            self.spn_number_of_locations = ttk.Spinbox(self.settings_frame, from_=1, to=10000)
            
            settings_widgets = [
                self.lbl_spn_num_people, self.spn_num_people,
                self.lbl_number_of_infected, self.spn_number_of_infected,
                self.lbl_number_of_locations, self.spn_number_of_locations,
            ]

            return settings_widgets

        if widget_type == 'action':
            self.lbl_spn_days_to_sim = ttk.Label(self.action_frame, text='Days to simulate')
            self.spn_days_to_sim = ttk.Spinbox(self.action_frame, from_=1, to=10)

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

                for _ in range(0, num_locations):
                    locations_list.append(Location())

                for person in self.people:
                    location_index = random.randint(0, num_locations -1)
                    locations_list[location_index].add_person(person)
                    person.location = location_index
                    #print(f'assigning person to location {location_index}')

                #print(f'''There are {len(self.people)} total people, of which:''')

                #for _ in range(0, len(locations_list)):
                #  print(f'{len(locations_list[_].people)} are in location {_}')
                    
                for location in locations_list:
                    # a location is NOT valid is all people in it are infected or all people in it are healthy, since the outcome is deterministic in those cases
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
                                if random.randint(1, 100) <= chance_of_infection:
                                    person.infect()
                            else: pass
                    
                total_infected = 0
                total_healhty = 0
                total_vaccinated = 0
                for person in self.people:
                    if person.is_infected:
                        total_infected += 1
                    if not person.is_infected:
                        total_healhty += 1
                    if person.is_vaccinated:
                        total_vaccinated +=1
                
                print(f'{total_infected}/{total_healhty + total_infected} are infected.')


                self.stats.days.append(len(self.stats.days))
                self.stats.total_healthy.append(total_healhty)
                self.stats.total_infected.append(total_infected)
                self.stats.total_vaccinated.append(total_vaccinated)
            
        self.show_data()


    def show_data(self):
        palette = ['#b52b2b', '#2b72b5', '#4dbf6d']
        plt.stackplot(1, 1)
        plt.clf()
        plt.stackplot(self.stats.days, self.stats.total_infected, self.stats.total_healthy, self.stats.total_vaccinated, labels=['Total infected', 'Total healthy', 'Total Vaccinated'], colors=palette)
        plt.legend(loc='upper left')
        plt.show()

    def start(self):
        if self.initial_run:
            try:
                int(self.spn_num_people.get())
            except Exception as exc:
                self.throw_exception(exc, 'Number of people spinner.', 'Please enter an integer.')
                return

            try:
                int(self.spn_number_of_infected.get())
            except Exception as exc:
                self.throw_exception(exc, 'Number of infected spinner.', 'Please enter an integer.')
                return

            try:
                int(self.spn_number_of_locations.get())
            except Exception as exc:
                self.throw_exception(exc, 'Number of locations spinner.', 'Please enter an integer')
                return



            total_people = int(self.spn_num_people.get())
            num_infected = int(self.spn_number_of_infected.get())
            num_healhty = int(self.spn_num_people.get()) - num_infected

            if num_infected > total_people:
                self.throw_exception('Invalid data.', 'More infected than healthy people!', 'The number of infected must be lower than the total number of people!')
                return

            for _ in range(0, num_healhty):
                person = Person(is_vaccinated=False, is_infected=False, is_masked=False)
                self.people.append(person)
            
            for _ in range(0, num_infected):
                person = Person(is_vaccinated=False, is_infected=True, is_masked=False)
                self.people.append(person)

        #for person in self.people:
         #   print(f'Person created. Vaccinated: {person.is_vaccinated}. Infected: {person.is_infected}. Protection: {person.protection}.')

        try:
            days_to_sim = int(self.spn_days_to_sim.get())
        except Exception as exc:
            self.throw_exception(exc, 'Days to sim spinner.', 'Please enter an integer!')
            return

        try:
            int(self.spn_number_of_locations.get())
        except Exception as exc:
            self.throw_exception(exc, 'Number of locations spinner.', 'Please enter an integer')
            return

        rules['number of locations'] = int(self.spn_number_of_locations.get())

        if self.initial_run:
            self.btn_start['text'] = 'Continue'
            self.spn_num_people.config(state='disabled')
            self.spn_number_of_infected.config(state='disabled')
        
        self.step(days_to_sim)

if __name__ == '__main__':
    simulation = Simulation()