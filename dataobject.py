class DataObject:
    def __init__(self):
        self.days = []
        self.total_infected = []
        self.total_healthy_vulnerable = []
        self.total_vaccinated = []
        self.total_recovered = []
        self.total_dead = []

        self.vac_enabled = []
        self.vac_disabled = []

        self.masks_enabled = []
        self.masks_disabled = []