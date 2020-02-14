# Name: Anthony Ma
# ID: 260829600
import doctest
import datetime
import matplotlib.pyplot as plt
import numpy as np
from initial_clean import *

def date_diff(first_date, second_date):
    """
    (str, str) -> int
    Input: two strings representing dates in ISO format (eg. 2019-11-29)
    Returns: how many days apart the two dates are, as an integer
    If the first date is earlier than the second date,
    the number should be positive; otherwise the number should be negative

    >>> date_diff('2019-10-31', '2019-11-2')
    2
    >>> date_diff('2019-10-31', '2019-11-30')
    30
    >>> date_diff('2019-2-20', '2019-12-30')
    313
    >>> date_diff('2018-10-31', '2000-11-2')
    -6572
    """
    # cast into lists first
    list1 = first_date.split('-')
    list2 = second_date.split('-')
    # input all the strings as integers into the method datetime.date for comparison
    date1 = datetime.date(int(list1[0]), int(list1[1]), int(list1[2]))
    date2 = datetime.date(int(list2[0]), int(list2[1]), int(list2[2]))

    str_difference = str(date2 - date1) # this is a string now, loop through it
    
    if str_difference[0] == '-': # if the difference is negative
        new_difference = str_difference[1:] # we remove the first minus sign first
    else:
        new_difference = str_difference

    for i, char in enumerate(new_difference):
        # use this method since the integers and 'days' are separated by a space,
        # we find this space
                    
        if not char.isdecimal():
    # this string contains the first integers at the beginning of the date object
            str_with_int = new_difference[:i]    # slice the string to get str with an integer
            break # finish editing the string, out of the loop
        
    if str_difference[0] == '-': 
        return -int(str_with_int)
    else:    
        return int(str_with_int)

def get_age(first_date, second_date):
    """
    (str, str) -> int
    Input: two strings representing dates in ISO format (eg. 2019-11-29)
    Returns: how many complete years apart the two dates are, as an integer
    Assume one year is 365.2425 days
    If the first date is earlier than the second date, the number should be positive;
    otherwise the number should be negative

    >>> get_age('2018-10-31', '2019-11-2')
    1
    >>> get_age('2018-10-31', '2000-11-2')
    -17
    """
    # call the date_diff function above
    # use int to round the decimals to zero
    return int(date_diff(first_date, second_date) / 365.2425)

def stage_three(input_filename, output_filename):
    """
    1. Replace the date of each record with the date diff of that date and the index date
    2. Replace the date of birth with age at the time of the index date
    3. Replace the status with one of I, R and D. (Representing Infected, Recovered, and Dead;
    the French words are infecté(e), récupéré(e) and mort(e).)

    Return: a dictionary. The keys are each day of the pandemic (integer).
    The values are a dictionary, with how many people are in each state on that day.
    >>> stage_three('stage2.txt', 'stage3.txt')
    {0: {'I': 1, 'D': 0, 'R': 0}, 1: {'I': 2, 'D': 1, 'R': 0}}

    """
    input_file = open(input_filename, 'r', encoding = 'utf-8') 
    out_file = open(output_filename, 'w+', encoding = 'utf-8')

    input_lines = input_file.readlines()
    first_substring = input_lines[0]
    index_date = first_substring.split('\t')[2] # at index 2 is the date of record (entry)

    newlist = []
    for line in input_lines:
        change_record = line.split('\t')
        change_record[2] = str(date_diff(index_date, change_record[2]))
        # change date of birth to ages
        change_record[3] = str(get_age(change_record[3], index_date))
        # change status of I,R,D
        if change_record[6][0] == 'I':
            change_record[6] = 'I' # increment values in dict
        elif change_record[6][0] == 'R':
            change_record[6] = 'R'
        elif change_record[6][0] == 'M' or change_record[6][0] == 'D':
            change_record[6] = 'D'
         
        # back to string
        new_substring = '\t'.join(change_record)
        newlist.append(new_substring)

    # write in the newfile
    for line in newlist:
        out_file.write(line) 
  
    big_dict = {} # make an empty dict, put all subdict inside
    i = 0
    for line in newlist:
        i+=1
        sub_dict = {'I': 0, 'D': 0, 'R': 0}
        listform = line.split('\t')
        try:
            if listform[2] not in big_dict:
                sub_dict[listform[6]] += 1
                big_dict[listform[2]] = sub_dict # initialize it
            else: # when there is already a subdict created,
                # we access its value (which is the subdict we need to increment on)
                dict_nested = big_dict[listform[2]] # increment on this
                dict_nested[listform[6]] += 1
                big_dict[listform[2]] = dict_nested # change the values big dict
                # where the values is the nested dict
        except KeyError:
            print("line", i)

    # now we have the big_dict but all keys here are strings, we just need to cast keys into integer
    edited_dict = {}
    for keys in big_dict:
        edited_dict[int(keys)] = big_dict[keys]
                     
    input_file.close()
    out_file.close()        
    return edited_dict

def plot_time_series(dict_of_dict):
    """
    (dict) -> list
    Input: a dictionary of dictionaries, formatted as the return value of Stage Three
    Return: a list of lists, where each sublist represents each day of the pandemic.
    Each sublist [how many people infected, how many people recovered, how many people dead]

    >>> d = stage_three('stage2.tsv', 'stage3.tsv')
    >>> plot_time_series(d)
    [[1, 0, 0], [2, 0, 1]]
    """
    biglist = []
    for keys in dict_of_dict:
        sub_dict = dict_of_dict[keys]
        sub_list = []
        sub_list.append(sub_dict['I'])
        sub_list.append(sub_dict['R'])
        sub_list.append(sub_dict['D'])
        biglist.append(sub_list)
    
    output_array = np.array(biglist)
    I = output_array[:, 0]
    R = output_array[:, 1]
    D = output_array[:, 2]
      
    plt.xlabel("Days into Pandemic")
    plt.ylabel("Number of People")
    plt.title('Time series of early pandemic, by Anthony Ma')
    
    plt.plot(I, 'b', label = 'Infected')
    plt.plot(R, 'g', label = 'Recovered')
    plt.plot(D, 'm', label = 'Dead')
    plt.legend()   
    plt.savefig("time_series.png")

    return biglist

if __name__ == "__main__":
    doctest.testmod()
       
    
