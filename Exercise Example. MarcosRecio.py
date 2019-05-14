"""
Data Wrangling Exercise Example
Candidate: Marcos Recio
"""
import pandas as pd

ict_data = pd.read_excel("./wrangling_exercise/data/ict_dashboard.xlsx")

"""
print(ict_data.columns)   As the columns are given already in the Jupyter Notebook
                            we do not need to check the names, but it is useful in any case.
"""

ict_data = ict_data[["Original planned end date","Planned end date","Department","Original total estimated expenditure","Revised total estimated expenditure","Investment objectives"]]
"""
Other ways to do it
ict_data.columns = ["Original planned end date","Revised end date","Department","Original total estimated expenditure","Revised total estimated expenditure","Investment objectives"]

"""
ict_data.rename(columns = {"Planned end date": "Revised end date"}, inplace = True)
ict_data["Original planned end date"], ict_data["Revised end date"] = pd.to_datetime(ict_data["Original planned end date"], format='%Y.%m.%d'), pd.to_datetime(ict_data["Revised end date"], format='%Y.%m.%d')

ict_data["Change in end date expectation"] = ict_data["Original planned end date"] - ict_data["Revised end date"]
ict_data["Change in expenditure expectation"] = ict_data["Original total estimated expenditure"] - ict_data["Revised total estimated expenditure"]

ict_data = ict_data[["Department","Investment objectives", "Change in end date expectation","Change in expenditure expectation"]]

ict_data["Change in end date expectation"] = (ict_data["Change in end date expectation"]/pd.Timedelta(1, unit='d')).astype('Int64')

ict_data.dropna(inplace = True)


# Defining a simple variable for the counting task 
count = 0

# lambda x : 'TASK3MAP' if len(x) > 2 and (x[0]>='A' and x[-1]<='Z') and x == x.upper() and x != 'ICT' else x

#Defining just for every word (checking that is a string and satisfies several conditions)
def f(word):
    global count
    """
    We want to have A, IT, HR ... ICT and other 2 letter acronyms or ICT that does not refer to the task target
    The counter automatically counts every instance without the use of string.count() method and string.replace()
    """
    # Checking if word's last item is a comma to avoid the comma with recursion
    if word == str(word) and word[-1] == ',':
        return f(word[0:-1])
    
    # Checking acronyms inside parentheses/brackets
    elif word == str(word) and word[0] == '(' and word[-1] == ')':
        return '(' +f(word[1:-1])+')'
    # Average ACRONYM and conditions to satisfy     
    elif word == str(word) and len(word) >2 and word[0]>='A' and word[-1]<='Z' and word == word.upper() and word != 'ICT':
            count += 1
            word = "TASK3MAP"
            return word     
    else:
        return word
    
# As every entry can be more than one item, we need to split the entry and use the function that we created before    
def rep(entry):
    val = ''
    if entry == str(entry):
        for i in entry.split():
            val += f(i) + ' '    
    return val
"""
 Use of Series.apply() with lambda function to just apply to the Column (Serie) that we are working with, in this case, "Investment objectives"
 In this case, Series.apply() works better than iterate elementwise througout
"""
ict_data["Investment objectives"] = ict_data["Investment objectives"].apply(lambda x: rep(x))

# Printing how many acronyms are in total in the column 'Investment objectives'
print(str(count) +" acronyms in 'Investment objectives' entries")


def vector(dataserie):
    """
    First we define an array or list to know the discrete values and the total number d
    to know the length of the vectors
    """
    discrete_vals = []
    # We check how many diferent values are there (discrete number of them instead of total entries)
    for entry in dataserie:
        if entry in discrete_vals:
            continue
        else:
            discrete_vals.append(entry)
            
    # General case. Creating a vector of zeros with number d as discrete_vals        
    zerovector = [0]*len(discrete_vals)
    
    # Here we open an array or list to create all the one-hot vectors
    vectors = []
    
    # A dictionary to attach every discrete value as a dictkey to its vector as the dictvalue 
    vectdict = {}
    
    # Creating one-hot vectors 
    for i in range(len(discrete_vals)):
        zerovector[i] = 1
        vectors.append(zerovector)
        vectdict[discrete_vals[i]] = zerovector    # Other way to do it is dict(zip(discrete_vals,vectors)) after having vectors
        zerovector = [0]*len(discrete_vals)        # Reassignment for zerovector

    #D = dict(zip(discrete_vals,vectors))    
    return dataserie.map(vectdict)

# Setting the Serie with vectors as the Serie in the DataFrame
ict_data["Department"] = vector(ict_data["Department"])

# Checking that the DataFrame is as it should be
#print(ict_data)
"""
coun = 0
for i in ict_data["Investment objectives"]:
    coun += i.count("TASK3MAP")
    #print(i)
print(coun)
"""
