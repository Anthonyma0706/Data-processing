# Name: Anthony Ma
# ID: 260829600

import doctest

def which_delimiter(s):
    """
    (str) -> str

    Returns: the most commonly used delimiter in the input string;
    will be one of space/comma/tab
    if there is no space/comma/tab, we rasie a AssertionError exception

    >>> which_delimiter('0 1 2,3')
    ' '
    >>> which_delimiter('0 1,2,3')
    ','
    >>> which_delimiter('0\\t1,2\\t3')
    '\\t'
    >>> which_delimiter('11,2,2022.11.29,1982.1.24,femme,h3x1r7,morte,39,3 C,3')
    ','
    >>> which_delimiter('')
    Traceback (most recent call last):
    AssertionError: Should have at least one delimiter.
    """  
    sep_by_space = s.split(' ')
    sep_by_comma = s.split(',')
    sep_by_tab = s.split('\t')
    # put all of them into a dictionary to compare data
    d = {' ': len(sep_by_space), ',': len(sep_by_comma), '\t': len(sep_by_tab)}
    value_delimiter = max(d.values())
    if value_delimiter == 1: # the lowest number of string split will be 1
        # which is the case that no delimiter shows up,
        # the output will be the original string (len = 1)
        raise AssertionError ('Should have at least one delimiter.')
    for key in d:
        if d[key] == value_delimiter:
            return key # the key is the corresponding str that we need to return
#########################################
# create a helper function to concatenate the space between postal code
def part_is_postal_code(input_string):

    """
    (str) -> bool
    input a three char string and the pattern of it is digit letter digit
    >>> part_is_postal_code('1B7')
    True
    >>> part_is_postal_code('Inf')
    False
    """

    return input_string[0].isdecimal() and input_string[1].isalpha() and input_string[0].isdecimal()
        

def stage_one(input_filename, output_filename):
    """
    (None, None) -> int
    input a file and generate a new file with words written inside
    1. join the postal code if there is a space between them
    1. Change the most common delimiter to tab (if it is not already tab-delimited)
    2. Change all text to be upper case
    3. Change any / or . in the dates to hyphens (e.g. 2022/11/28 becomes 2022-11-28)
    Finally, Return an integer: how many lines were written to output filename
    >>> stage_one('stage1_input.txt', 'stage1.tsv')
    4
    """
    # since there is French, add encoding = ‘utf-8’ as a parameter to all calls to open,
    # so we can support the accents. 
    input_file = open(input_filename, 'r', encoding = 'utf-8') 
    out_file = open(output_filename, 'w+', encoding = 'utf-8') # need to read it too
    input_lines = input_file.readlines() # put everything into a list
    for line in input_lines: # loop through every element in the big list, line is str
     # concatenate postal code   
        if which_delimiter(line) == ' ':
            list_of_line = line.split(' ')
            # index 6 is the column that may have defect data, we deal with it
            if len(list_of_line) > 9 and (part_is_postal_code(list_of_line[6]) or \
               list_of_line[6][0] == 'a' or list_of_line[6][0] == 'A'):    
                list_of_line[5] = list_of_line[5] + list_of_line[6]
                del list_of_line[6]
                # bring it back
                line = ' '.join(list_of_line)
                    
        tab_line = line.replace(which_delimiter(line), '\t') # change the delimiter
        upper_line = tab_line.upper() # change to upper clase
        change_slash = upper_line.replace('/', '-')
        change_dot = change_slash.replace('.', '-')
        # write this final edited line into out_file       
        out_file.write(change_dot) 
    
    out_file.seek(0) # shift the file pointer to the beginning for counting
    num_lines_written = len(out_file.readlines()) # the lens is the #lines written
    # close the files
    input_file.close()
    out_file.close()
    return num_lines_written

def stage_two(input_filename, output_filename):
    """
    (None, None) -> int
    The changes to make to the data:
    1. All lines should have 9 columns
    2. Any lines with more than 9 columns should be cleaned so the line is now 9 columns.
    For example, in French the comma is used for decimal points,
    so the temperature ’39,2’ could have been broken into 39 and 2.
    
    Finally, Return an integer: how many lines were written to output filename

    >>> stage_one('stage2_input.txt', 'stage2.tsv')
    4
    """

    # since there is French, add encoding = ‘utf-8’ as a parameter to all calls to open,
    # so we can support the accents. 
    input_file = open(input_filename, 'r', encoding = 'utf-8') 
    out_file = open(output_filename, 'w+', encoding = 'utf-8')

    input_lines = input_file.readlines() # put everything into a list
    proper_list = [] # we then append all modified substring to this list
    for line in input_lines:
        raw_list = line.split('\t')
        if len(raw_list) > 9: # means we need to modify the columns
            # which means we have 10 columns in total
            # two cases: first, the first char of the nineth element starts with number
            first_char_nineth = raw_list[8][0]
            if first_char_nineth.isdecimal():
                # use isdecimal method to check this string (single char) contains digit
                # we use a dot to join them together
                raw_list[7] = raw_list[7] + '.' + raw_list[8]
            else: # simply concatenate
                raw_list[7] = raw_list[7] + raw_list[8]
            # then, delete the nineth element since we have already added it to 7th element  
            del raw_list[8]
            newstr = '\t'.join(raw_list)
            proper_list.append(newstr)
        else:
            proper_list.append(line)
            # the string is proper, just append it to the new big list

    for line in proper_list:
        out_file.write(line)

    out_file.seek(0) # shift the file pointer to the beginning for counting
    num_lines_written = len(out_file.readlines()) # the lens is the #lines written
    # close the files
    input_file.close()
    out_file.close()
    return num_lines_written           
                  
    
    
    
if __name__ == "__main__":
    doctest.testmod()    
