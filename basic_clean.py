
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
#from textblob import TextBlob

# it will take comment as input 
def basic_cleanning(text):   
    cl_text = clean_text(text)
    
    filtered_str = rm_stop_wd(cl_text)
    return filtered_str


"""
# =======================================================Data Cleaning ====================================================
"""

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[“]','"',text)
    text = re.sub(r'[”]','"',text)
    text = re.sub(r'[’]',"'",text)
    text=re.sub(r"i'm","i am", text)
    text=re.sub(r"he's","he is", text)
    text=re.sub(r"don't","do not", text)
    text=re.sub(r"it's","it is", text)
    text=re.sub(r"she's","she is", text)
    text=re.sub(r"that's","that is", text)
    text=re.sub(r"where's","where is", text)
    text=re.sub(r"what's","what is", text)
    text=re.sub(r"shouldn't","should not", text)
    text=re.sub(r"mustn't","must not", text)
    text=re.sub(r"shan't","shall not", text)
    text=re.sub(r"aren't","are not", text)
    text=re.sub(r"didn't","did not", text)
    text=re.sub(r"haven't","have not", text)    
    text=re.sub(r"needn't","need not", text)  
    text=re.sub(r"doesn't","does not", text)  
    text=re.sub(r"couldn't","could not", text)  
    text=re.sub(r"won't","will not", text)  
    text=re.sub(r"mightn't","might not", text) 
    text=re.sub(r"isn't","is not", text) 
    text=re.sub(r"hadn't","had not", text) 
    text=re.sub(r"wouldn't","would not", text) 
    text=re.sub(r"hasn't","has not", text) 
    text=re.sub(r"wasn't","was not", text) 
    text=re.sub(r"weren't","were not", text)
    text = re.sub(r'[;“”’–,./:"''{}|\`~!@#$%^&*()-+_=]',"",text)
    text = re.sub(r'[\[\]]','',text)
    return text

"""
# =====================+========== Remove stop words from Comments============================================================== 
"""

def rm_stop_wd(clean_string):
    stop_words = set(stopwords.words('english')) 
    # we need following words in commensts so we are removing it from original stop word List 
    remove_from_stop_words = ["not","shouldn't","don't","mustn't","shan't","aren't","didn't","haven't","needn't",         "doesn't","couldn't","won't","mightn't","isn't","hadn't","wouldn't","hasn't","wasn't","weren't"]
    # print(stop_words) by defalut stop words..
    for w in remove_from_stop_words:
        if w in stop_words:
            stop_words.remove(w)
    
    #print(stop_words) # List of Stop words that we need...
    # Tokenization
    word_tokens = word_tokenize(clean_string) 
    filtered_token = []  #answer 
    garbage =[] #testing purpose
    
    for w in word_tokens:
        if w not in stop_words:
            filtered_token.append(w)
        else:
            garbage.append(w) 

    #print(garbage)  #testing Purpose     
    #print(filtered_sentence)  

    return filtered_token     #list of tokens is returned


"""
# =====================+========== Spelling Checking ============================================================= 
"""

"""
# =====================+==========Optional-  Lemmi==========================================================================
"""
"""
# =====================+==========Language Detection============================================================ 
"""
#from textblob import TextBlob
#b = TextBlob("वाईट ") #argument must be "string"
#print(b.detect_language())






