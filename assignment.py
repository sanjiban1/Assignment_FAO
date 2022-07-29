
import sys
import csv 
import json
# Deserialize from collections import defaultdict
from collections import defaultdict

# Creates a class assignment for this disease.
class Assignment:
    # Initialize a new file.
    def __init__(self, filename, outputname):
        self.filename = filename
        self.outputname = outputname
        self.headers = []
        self.input_data = []
        self.disease_list = []

    # Read a csv file and store headers.
    def read_file(self):
        file = open(self.filename)
        csvreader = csv.reader(file)
        self.headers = next(csvreader)
        # Appends each row to the input_data.
        for row in csvreader:
                self.input_data.append(row)


    # Read the disease_list. csv file.
    def read_disease_file(self):
        file = open("disease_list.csv")
        csvreader = csv.reader(file)
        next(csvreader)
        # Adds the disease to the disease list.
        for row in csvreader:
                self.disease_list.append(row)


    # Parse the data into a dictionary.
    def parse_data(self):
        # Returns a dict with all location - wise cases.
        total_cases = 0
        location_wise_cases = defaultdict(int)
        flag = False
        # Returns a Species dict containing all of the input data.
        for data in self.input_data:
            # Sets the SPECIES_INDEX from the headers.
            if len(data) == len(self.headers):
                SPECIES_INDEX = 2
                MORTALITY_INDEX = 5
                TOTAL_CASES_INDEX = 6
                LOCATION_INDEX = 7
            else:
                SPECIES_INDEX = -6
                MORTALITY_INDEX = -3
                TOTAL_CASES_INDEX = -2
                LOCATION_INDEX = -1
                flag = True

            # Returns a sorted list of location - wise cases.
            total_cases += int(data[TOTAL_CASES_INDEX])
            location_wise_cases[data[LOCATION_INDEX]] += int(data[MORTALITY_INDEX])

        # Sorts the location - wise cases in alphabetical order.
        location_wise_sorted = sorted(location_wise_cases.keys())

        # Create a corrupted. json file.
        if flag:
            dotindex = self.outputname.rfind('.')
            filename = self.outputname[:dotindex] + "_corrupted.json"
        else:
            filename = self.outputname

        # Saves the total number of reported cases and deaths reported at each location
        self.save_output({
            "total number of reported cases is": total_cases,
            "total number of deaths reported at each location": {k: location_wise_cases[k] for k in location_wise_sorted}
        }, filename)

    # Read the disease file and parse advanced data.
    
    def advanced_data(self):
        self.read_disease_file()
        total_cases = 0
        total_cats = 0
        disease_wise_cases = defaultdict(int)
        # Returns a tuple containing the SPECIES_INDEX of the response.
        for data in self.input_data:
            if len(data) == len(self.headers):
                SPECIES_INDEX = 2
                TOTAL_CASES_INDEX = 6
                LOCATION_INDEX = 7
                DISEASE_INDEX = 4
                MORTALITY_INDEX = 5
            else:
                SPECIES_INDEX = -6
                TOTAL_CASES_INDEX = -2
                LOCATION_INDEX = -1
                DISEASE_INDEX = -4
                MORTALITY_INDEX = -3

            # Calculate the disease - wise cases for a village.
            disease_wise_cases[data[DISEASE_INDEX]] += int(data[MORTALITY_INDEX])
            if data[LOCATION_INDEX].startswith("Village"):
                total_cases += 1
                if data[SPECIES_INDEX] == "cat":
                    total_cats += int(data[TOTAL_CASES_INDEX])

        # Save the disease list to a JSON file.
        disease_names = sorted(self.disease_list, key = lambda item: item[1])
        dotindex = self.outputname.rfind('.')
        filename = self.outputname[:dotindex] + "_advanced.json"
        self.save_output({name: disease_wise_cases[did] for did, name in disease_names}, filename)
        

    # Save the data to a file.
    def save_output(self, data, filename):
        json_object = json.dumps(data, indent=4)
        
        
        # Write a json object to a file
        with open(filename, "w") as outfile:
            outfile.write(json_object)


# Sets the input and output file names.
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

# Reads the input file and parses the advanced data.
assignment = Assignment(input_file_name, output_file_name)
assignment.read_file()
assignment.parse_data()
assignment.advanced_data()
