"""
This Module is to search -- "Domain name" --
- After Searching for book i.e. after query is fired by User, first task is to understand the 
query and find that which domain related query is asked....

Input --> Get the complete query in <String> format.
Output --> Return "Domain_name"  in <string> format .
"""


from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 


"""-----------------Remove stop Words function -->>----------------------------
"""
def remove_stopwords(word_list):
    processed_word_list = []
    for word in word_list:
        word = word.lower() 
        if word not in stopwords.words("english"):
            processed_word_list.append(word)
    return processed_word_list
##=============================================================================



"""-----------------find Domain------------------------------------------------
"""
def find_domain(input_string):
    # Tokenize the string :-
    word_tokens = word_tokenize(input_string)  #It will Return a <List>

    ## nOW CALL REMOVE STOP WORD Function
    tokens = remove_stopwords(word_tokens)  ##Its a <List> 
    
    tok_set =set(tokens) #converted into <Set>
    
    """
    --------------Read this dictionary from DataBase, from Flask --------------
    """
    
    di = {"c":["c","language","pointers","basic","simple","function","structure","basic","Programming"],
          "C++ Programming":["cpp","c++","inheritance","polymorphism","encapsulation","function","Programming"],
           "Operating System":["threading","operating","system","os","Programming","shell","script"],
           "Data Structures":["data","Structures","stack","queue","linklist","array","ds","graph","tree"],
           "Computer Architecture":["processes","computer","architecture","coa"],
           "Database Management System":["database","management","mongodb","sql","dbms","data","base","db","mysql"]
          }
    #--------------------------------------------------------------------------

    domain = ""  #Null String
    max_count = 0

    for key,val in di.items():
        domain_set = set(val)
        #print(domain_set)
        notfound = tok_set.isdisjoint(domain_set)
        #print(notfound)
        if not notfound:
            intersection_set = tok_set.intersection(domain_set)
            if len(intersection_set) > max_count: 
                max_count = len(intersection_set)
                domain = key
    
    if domain != "" :  
        return domain
    #else:  return 0
##=============================================================================







