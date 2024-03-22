import sys
import pandas as pd
import re


#----------------------#
#read commmand line arguments to argumentList
try:

    argumentList = sys.argv[1:]

except Exception:
    print ("Error Reading from file:")



#List of functions
def function1(df):
    #Extract columns with missing values
    print(df.columns[df.isnull().any()].to_list())  
 
def function2(df):
    #Count the number of lines with missing data
    null_count = pd.isnull(df).sum()                #count nulls in each column
    is_null = null_count > 0                        #true/false series describing if that column had nulls
    print(null_count[is_null])                      #print number of lines (>0) with missing data 

def function3(df, method, output):
    #Fill in the missing value using mean, median (for numeric properties) 
    # and mode (for the categorical attribute).
    
    categories = df.select_dtypes(include=['object']).columns           #list of categorical attributes  
    number = df.select_dtypes(include=['number']).columns               #list of numeric attributes 

    #if method is different from mean or median, input again
    if method != "mean" and method != "median":
        print("using mean, median (for numeric properties) and mode (for the categorical attribute)")
        return
    
    #fill missing values
    for col in categories:
        df[col].fillna(df[col].mode()[0], inplace=True)
    for col in number:
        if method == "mean":
            df.fillna(df.mean(numeric_only=True).round(1), inplace=True)
        elif method == "median":
            df.fillna(df.median(numeric_only=True).round(1), inplace=True)
    
    #save datafram to file csv
    df.to_csv(output)
    print("Saved to", output)

def function4(df, percent, output):
    #Deleting rows containing more than a particular number of missing values 
    # (Example: delete rows with the number of missing values is more than 50% of the number of attributes)

    new_df = df.copy()              #copy df to new_df
    ncol = len(new_df.columns)      #number of attributes  
    new_df= new_df[new_df.isnull().sum(axis=1) < int(percent)/100*ncol]     #delete

    new_df.to_csv(output)           #save to csv  
    print("Saved to", output)

def function5(df, percent, output):
    #Deleting columns containing more than a particular number of missing values 
    #(Example: delete columns with the number of missing values is more than 50% of the number of samples).

    new_df = df.copy()              #copy df to new_df
    new_df = new_df[new_df.columns[new_df.isnull().mean() < int(percent) / 100]]    #delete

    new_df.to_csv(output)           #save to csv
    print("Saved to", output)

def function6(df, output):
    # Delete duplicate samples
    df_dup_removed = df.drop_duplicates()       

    df_dup_removed.to_csv(output)    #save to csv
    print(df_dup_removed)
    print("Saved to", output)
    
def function7(df, col):
    #Normalize a numeric attribute using min-max and Z-score methods.
    min_max = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    z_score= (df[col] - df[col].mean()) / df[col].std()

    #create dataframe df_normm from 2 list min_max and z-score to print
    df_norm = pd.DataFrame(list(zip(min_max, z_score)), columns=['Min-max', 'Z-score'])
    print(df_norm)

def function8(df, cal, col1, col2):
    #Performing addition, subtraction, multiplication, and division between two numerical attributes
    newcol = col1 + " " + cal + " " + col2
    if cal == "add":
        df[newcol]= df[col1] + df[col2]
    elif cal == "sub":
        df[newcol]= df[col1] - df[col2]
    elif cal == "mul":
        df[newcol]= df[col1] * df[col2]
    elif cal == "div":
        df[newcol]= df[col1] / df[col2]
    else: 
        print(" Try again")
        return

    print(df[newcol])


############
#----Handling command line arguments----#

n = len(argumentList)       #number of arguments

#list of syntax
listHelp = ["Function 1: python preprocessing.py <datafilename.csv> <function>",
            "Function 2: python preprocessing.py <datafilename.csv> <function>",
            "Function 3: python preprocessing.py <datafilename.csv> <function> --m <'mean'/'median'/'mode'> --out <outputfilename.csv>",
            "Function 4: python preprocessing.py <datafilename.csv> <function> --x <percent> --out <outputfilename.csv>",
            "Function 5: python preprocessing.py <datafilename.csv> <function> --x <percent> --out <outputfilename>.csv",
            "Function 6: python preprocessing.py <datafilename.csv> <function> --out <outputfilename.csv>",
            "Function 7: python preprocessing.py <datafilename.csv> <function> --col <column>",
            "Function 8: python preprocessing.py <datafilename.csv> <function> --cal <calculation> --col1 <column1> --col2 <column2>"]

#print list of syntax when argument is --h or --help
if argumentList[0] == "--h" or argumentList[0] == "--help":
    for h in listHelp:
        print(h)

#read arguments
else: 
    data_filename = argumentList[0]     #data file name
    df = pd.read_csv(data_filename)     #read file data to dataframe


    func = int(re.sub('[^0-9]', '', argumentList[1]))       #what function is user want to test

    #read the argument corresponding to each function
    if func == 1:
        function1(df)

    elif func == 2:
        function2(df)

    elif func == 3:
        method = argumentList[3]
        output = argumentList[5]
        function3(df, method, output)

    elif func == 4:
        percent = argumentList[3]
        output = argumentList[5]
        function4(df, percent, output)

    elif func == 5:
        percent = argumentList[3]
        output = argumentList[5]
        function5(df, percent, output)

    elif func == 6:
        output = argumentList[3]
        function6(df, output)

    elif func == 7:
        col = argumentList[3]
        function7(df, col)

    elif func == 8:
        cal = argumentList[3]
        col1 = argumentList[5]
        col2 = argumentList[7]
        function8(df, cal, col1, col2)

    else: print("Try again")        #print when syntax error