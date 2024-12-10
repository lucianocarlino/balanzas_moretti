class Scale:
    def __init__(self, id, address):
        self.linea = None
        self.id = id
        self.packages = []
        self.address = address
        #weights [[date_time, package_id, initial_weight, final_weight]]
        self.weights = []

    def asign_line(self, linea):
        self.linea = linea

    def add_package(self, package):
        self.packages.append(package)

    def remove_package(self, package):
        self.packages.remove(package)

    def edit_package(self, package, id):
        self.packages[self.packages.index(id)] = package

    def add_weight(self, weight):
        self.weights.append(weight)
    
    def get_weight(self, index=-1):
        return self.weights[index]
    
    def get_weights(self):
        return self.weights
    
    def __str__(self):
        return f"Scale {self.id} in Line {self.linea}"
