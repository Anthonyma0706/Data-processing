# Name: Anthony Ma
# ID: 260829600

import doctest
import matplotlib.pyplot as plt
import numpy as np

def update_gender(sex_gender):
        """
        (str) -> str

        change the various input to only three types of genders

        >>> update_gender('FEMME')
        'F'
        >>> update_gender('FEMALE')
        'F'
        >>> update_gender('F')
        'F'
        >>> update_gender('WOMAN')
        'F'
        >>> update_gender('GIRL')
        'F'
        
        >>> update_gender('HOMME')
        'M'
        >>> update_gender('BOY')
        'M'
        >>> update_gender('MAN')
        'M'
        >>> update_gender('MALE')
        'M'
        >>> update_gender('M')
        'M'

        >>> update_gender('NON-BINARY')
        'X'
        >>> update_gender('NON-BINAIRE')
        'X'
        >>> update_gender('X')
        'X'
        >>> update_gender('GENDERQUEER')
        'X'
        """
        # for female:
        if sex_gender[0] == 'F' or sex_gender[0] == 'W' or sex_gender == 'GIRL':
            return 'F'
        elif sex_gender[0] == 'H' or sex_gender == 'BOY' or sex_gender[0] == 'M':
            return 'M'
        else:
            return 'X'


def update_postal(postal):
    """
    (str) -> str

    update the postal code to its first three characters of the patient’s postal code
    If they do not have a valid postal code (e.g. ‘N.A.’), use ‘000’.
    A valid Montreal postal code should start with H, then a number, then a letter.
    (You do not have to validate the characters after the first three).

    >>> update_postal('H1L 4W3')
    'H1L'
    >>> update_postal('N-A-')
    '000'
    >>> update_postal('NON APPLICABLE')
    '000'
    >>> update_postal('H3M')
    'H3M'
    >>> update_postal('HHH')
    '000'
    >>> update_postal('01011')
    '000'
    """
    valid_first_three = postal[0] == 'H' and postal[1].isdecimal() and postal[2].isalpha()

    if not valid_first_three:
        return '000'
    else:
        return postal[:3]

def update_temp(temps):
    """
    (str) -> list
    Note: in French, the comma is used for decimal points.
    The input could be in Fahrenheit, so convert any temperature above 45 to Celsius.
    Round it to two decimals.
    If you get a string which does not contain a number (e.g. ‘N.A.’ because the
    patient died), record this as 0.

    return a list of floats

    >>> update_temp('38-9 C')
    [38.9]
    >>> update_temp('104,5') # convert F to C
    [40.28]
    >>> update_temp('102.2C') # convert F to C
    [39.0]
    >>> update_temp('40,54 C')
    [40.54]
    >>> update_temp('39')
    [39.0]
    >>> update_temp('N-A')
    [0]
    >>> update_temp('NONAPPLICABLE')
    [0]
    
    
    """
    # if NA:
    if temps[0] == 'N':
        return [0] # still a list
   
    else: # not NA
         # 1. convert - and , to decimal point .
        temps_hyphen_changed = temps.replace('-', '.')
        temps_comma_changed = temps_hyphen_changed.replace(',', '.')
        for i, char in enumerate(temps_comma_changed):
                # when it's not a digit, we slice the string
            if char != '.' and not char.isdecimal(): 
                temps_comma_changed = temps_comma_changed[:i]
                break # REMEMBER TO GET OUT!
            
        # for Fahrenheit, if temp above 45 Celsius, convert
        if float(temps_comma_changed) > 45:
            celcius_value = (float(temps_comma_changed) - 32) * 5 / 9
            temps_comma_changed = str(round(celcius_value, 2))
    
    newlist = []
    newlist.append(float(temps_comma_changed))
    
    return newlist
    
    
    


class Patient:
    
    def __init__(self, num, day_diagnosed, age, sex_gender, postal, state, temps, days_symptomatic):
        self.num = int(num) # int
        self.day_diagnosed = int(day_diagnosed) # int
        self.age = int(age) # int
        self.sex_gender = update_gender(sex_gender) # string: either M, F, or X
        self.postal = update_postal(postal) # str
        self.state = state # str
        self.temps = update_temp(temps) # list of floats
        self.days_symptomatic = int(days_symptomatic) #int

    def __str__(self):
        """
        Return a string of the following attributes,
        separated by tabs: self.num, self.age, self.sex gender, self.postal,
        self.day diagnosed, self.state, self.days symptomatic,
        then all the temperatures observed separated by semi-colons

        >>> p = Patient('0', '0', '42', 'Woman', 'H3Z2B5', 'I', '102.2', '12')
        >>> str(p)
        '0\\t42\\tF\\tH3Z\\t0\\tI\\t12\\t39.0'
        """
        temp_value = ''
        if len(self.temps) == 1: # for the case that an object is initialized, only one temp inside list
            temp_value = str(self.temps[0])
        else: # for multiple data inside the temp
            list_contain_str = []
            for e in self.temps:
                list_contain_str.append(str(e))
                
            temp_value = ';'.join(list_contain_str)
            
        list_of_attributes = [str(self.num), str(self.age), self.sex_gender, self.postal, \
        str(self.day_diagnosed), self.state, str(self.days_symptomatic), temp_value]

        return '\t'.join(list_of_attributes)
    
    def update(self, other):
        """
        other is another newer object, i.e established after this 'self object'
        if other has the same object’s number, sex/gender and postal code.
        – Update the days the patient is symptomatic to the newer one
        – Update the state of the patient to the newer one
        – Append the new temperature observed about the patient. You can assume the other
        Patient has only one temperature stored in their temps.

        >>> p = Patient('0', '0', '42', 'GIRL', 'H3Z2B5', 'I', '102.2', '12')
        >>> p1 = Patient('0', '1', '42', 'F', 'H3Z', 'I', '40,0', '13')
        >>> p.update(p1)
        >>> str(p)
        '0\\t42\\tF\\tH3Z\\t0\\tI\\t13\\t39.0;40.0'

         """
        correct = self.num == other.num and self.sex_gender == other.sex_gender and self.postal == other.postal
        if not correct:
            raise AssertionError ('num/sex gender/postal are not the same.')
        else:
            self.days_symptomatic = other.days_symptomatic
            self.state = other.state
            new_temp = other.temps[0] # append this to the old list
            self.temps.append(new_temp)



def stage_four(input_filename, output_filename):
    """
    Create a new Patient object for each line
    Keep (and return) a dictionary of all the patients:
    – Use the patient’s number (as int) for the key, and the Patient objects for the values.
    – Whenever you see a new entry for an existing patient,
    update the existing Patient object rather than overwrite it.
    Write to the output file: every Patient converted to a string,
    sorted by patient number (separated by new lines)
    """
    input_file = open(input_filename, 'r', encoding = 'utf-8') 
    out_file = open(output_filename, 'w+', encoding = 'utf-8')
    input_lines = input_file.readlines() # a very big list containing strings
    count = 0
    dict_patient = {}
    new_list_to_sort = []
    for line in input_lines:
        info = line.split('\t') # a list containing 9 elements (information of patient)
        p = Patient(info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8])
        #return str(p)
        # info[1] is the patient number
        
        if info[1] not in dict_patient: # not in, we initialize it
            dict_patient[info[1]] = p
                  
        else: # if in, we update the value to be the updated version of p
            old_p = dict_patient[info[1]]
            old_p.update(p) # update object
            dict_patient[info[1]] = old_p

    for i in range(4000): # actually 3011 is the max
        if str(i) in dict_patient: # there is some patient number missing, so we expand the range of i
            # and if string format of i exist in dictionary, that means the number is in the data file
            # we write it to the new file.
            str_to_write = str(dict_patient[str(i)])
            out_file.write(str_to_write + '\n')

    input_file.close()
    out_file.close()
        
    return dict_patient    
            

def round_age(x, base=5):
    """
    (int) -> int
    round number to the nearest 5
    >>> round_age(23)
    25
    >>> round_age(21)
    20
    """
    return base * round(x/base)

def fatality_by_age(dict_patient):
    """
    Input: a dictionary of Patient objects
    Goal: plot the probability of fatality versus age
    round patients’ ages to the nearest 5 (e.g 23 becomes 25)
    """
    # 1. round patients’ ages to the nearest 5 (e.g 23 becomes 25)
   
    dict_of_age = {}
    for key in dict_patient:
        p = dict_patient[key]
        # update the age of p (round it)
        p.age = round_age(p.age)

        
        if p.age not in dict_of_age: # initialize it         
            death = 0
            recovered = 0
            if p.state == 'D':
                death += 1
            elif p.state == 'R':
                recovered += 1
            list_of_recover_and_death = [death, recovered]     
            dict_of_age[p.age] = list_of_recover_and_death
        else:
            if p.state == 'D':
                dict_of_age[p.age] = [dict_of_age[p.age][0] + 1, dict_of_age[p.age][1]]
            elif p.state == 'R':
                dict_of_age[p.age] = [dict_of_age[p.age][0], dict_of_age[p.age][1] + 1]
                # if it's I, we don't count
    
    # 2. calculate probability, use the list (value of dictionary) to calculate
    dict_of_probab = {}
    for key in dict_of_age:
        info = dict_of_age[key]
        denominator = (info[0] + info[1])
        if denominator == 0:
                probability = 1 # if zero div, we make prob as 1
        else:
                probability = info[0] / (info[0] + info[1])
        dict_of_probab[key] = probability
        
    # sort the dictionary keys to the list, also we need it to get array for plotting graph
    list_of_ordered_age = sorted(dict_of_probab)
    list_of_prob = []
    for key in list_of_ordered_age:
        list_of_prob.append(dict_of_probab[key])

    x_coord = np.array(list_of_ordered_age)
    y_coord = np.array(list_of_prob)

    plt.ylim((0, 1.2))
    plt.xlabel("Age")
    plt.ylabel("Deaths / (Deaths+Recoveries)")
    plt.title('Probabilty of death vs age by Anthony Ma')

    plt.plot(x_coord, y_coord)

    plt.savefig("fatality_by_age.png")

    
    return list_of_prob
        

if __name__ == "__main__":
    doctest.testmod()
    #dict_patient = stage_four('three_260829600.txt', 'four_260829600.txt')
    #print(fatality_by_age(dict_patient))
    # my text file converted after stage 3
   
      
