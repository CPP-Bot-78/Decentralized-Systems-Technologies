import csv
import itertools
import random
import os


def create_education_dictionary(n):
    education_dict = {}
    # Η απόλυτη διαδρομή του script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # Συνδυάζουμε την απόλυτη διαδορμή με το όνομα του αρχείου CSV που περιέχει τους επιστήμονες
    CSV_PATH = os.path.join(script_directory, '../computer_scientists_data.csv')
    with open(CSV_PATH, 'r', encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            education_values = eval(row['Education'])
            awards = int(row['#Awards'])
            surname = row['Surname']

            for education_value in education_values:
                education_str = education_value.strip("'\"")  # Remove excess quotes
                # If the education key is not in the dictionary, add it
                if education_str not in education_dict:
                    education_dict[education_str] = [(surname, awards)]
                else:
                    # If it already exists, add it to the existing list
                    education_dict[education_str].append((surname, awards))

    # Remove scientists with an empty education
    education_dict.pop('', None)

    # Ανακατεύει τα περιεχόμενα του dictionary
    education_dict = list(education_dict.items())
    random.shuffle(education_dict)
    education_dict = dict(education_dict)

    # Κρατάει μόνο τα n πρώτα στοιχεία του dictionary 
    education_dict = dict(itertools.islice(education_dict.items(), n))
    '''
    for key, value in education_dictionary.items():
        print(f"Education: {key}")
        print(f"Scientists/Awards: {value}")
        print()
    '''
    return education_dict

