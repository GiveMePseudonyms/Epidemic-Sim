import tkinter
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from person import Person

class Simulation:
    def __init__(self):
        #tell mpl to use the tk backend to show figures in the tk window
        self.settings = {
            'max people': 1000,
        }

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
        self.WINDOW.mainloop()

    def create_widgets(self, widget_type):
        if widget_type == 'settings':
            self.lbl_spn_num_people = ttk.Label(self.settings_frame, text='Number of people')
            self.spn_num_people = ttk.Spinbox(self.settings_frame, from_=1, to=self.settings['max people'])

            self.lbl_number_of_infected = ttk.Label(self.settings_frame, text='Number of infected')
            self.spn_number_of_infected = ttk.Spinbox(self.settings_frame, from_=1, to=self.settings['max people'])

            self.btn_start = ttk.Button(self.WINDOW, text='Start', command=lambda: self.start())
            
            settings_widgets = [
                self.lbl_spn_num_people, self.spn_num_people,
                self.lbl_number_of_infected, self.spn_number_of_infected,
                self.btn_start,
            ]

            return settings_widgets

        if widget_type == 'action':
            self.lbl_spn_days_to_sim = ttk.Label(self.action_frame, text='Days to simulate')
            self.spn_days_to_sim = ttk.Spinbox(self.action_frame, from_=1, to=10)

            action_widgets = [
                self.lbl_spn_days_to_sim, self.spn_days_to_sim,
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
    
    def step(self, steps):
        for _ in range(1, steps + 1):
            print(f'step {_}')

    def show_data(self):
        data = {}
        for _ in range(0, 20):
            data[f'point {_}'] = _

        return data

    def start(self):
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
            person = Person(False, False, 1)
            self.people.append(person)
        
        for _ in range(0, num_infected):
            person = Person(False, True, 1)
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