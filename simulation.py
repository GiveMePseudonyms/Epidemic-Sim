import tkinter
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from person import Person
from location import Location
import random
from ruleset import rules

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

        self.stats = {}

        self.WINDOW.mainloop()

    def create_widgets(self, widget_type):
        if widget_type == 'settings':   
            self.lbl_spn_num_people = ttk.Label(self.settings_frame, text='Number of people')
            self.spn_num_people = ttk.Spinbox(self.settings_frame, from_=1, to=rules['max people'])

            self.lbl_number_of_infected = ttk.Label(self.settings_frame, text='Number of infected')
            self.spn_number_of_infected = ttk.Spinbox(self.settings_frame, from_=1, to=rules['max people'])


            
            settings_widgets = [
                self.lbl_spn_num_people, self.spn_num_people,
                self.lbl_number_of_infected, self.spn_number_of_infected,
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

    def calculate_infection_chance(self, person, location_infection_chance, virus_infectivity):
        susceptibility = person.calculate_susceptibility(virus_infectivity)

        chance = location_infection_chance * susceptibility
        return chance

    def step(self, steps):
        self.initial_run = False

        for _ in range(1, steps + 1):    
            num_locations = rules['number of locations']
            locations_list = []

            for _ in range(0, num_locations):
                locations_list.append(Location())

            for person in self.people:
                location_index = random.randint(0, num_locations -1)
                locations_list[location_index].add_person(person)
                person.location = location_index
                #print(f'assigning person to location {location_index}')

            print(f'''There are {len(self.people)} total people, of which:''')

            for _ in range(0, len(locations_list)):
                print(f'{len(locations_list[_].people)} are in location {_}')

            for location in locations_list:
                location.calculate_total_infection_chance(rules['virus infectivity'])
                # print(f'There are {len(location.infected_people)} infected people in location {locations_list.index(location)}')

            for location in locations_list:
                for person in location.people:
                    if not person.is_infected:            
                        person.chance_of_infection = self.calculate_infection_chance(person, location.total_location_infection_chance, rules['virus infectivity'])
                        """
                        print(f'''Person:
                        Location: {person.location}
                        Vaccinated: {person.is_vaccinated}
                        Infected: {person.is_vaccinated}

                        Chance of infection: {person.chance_of_infection}
                        
                        ''')
                        """
                        if random.randint(0, 100) <= (100* person.chance_of_infection):
                            person.infect()
                            print(f'person at location location {person.location} infected!')
            
            total_infected = 0
            for person in self.people:
                if person.is_infected:
                    total_infected += 1
            
            print(f'{total_infected}/{len(self.people)} are infected.')

            self.stats[str(len(self.stats))] = total_infected

    def show_data(self):
        
        plt.plot(self.stats.keys(), self.stats.values())
        plt.title('Infected vs Days')
        plt.xlabel('Day')
        plt.ylabel('Number of infected')
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

        if self.initial_run:
            self.btn_start['text'] = 'Continue'
        
        self.step(days_to_sim)


if __name__ == '__main__':
    simulation = Simulation()