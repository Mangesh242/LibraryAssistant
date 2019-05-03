from textblob.classifiers import NaiveBayesClassifier
#strg = input()

def classify_v1(text):
    #<str> is passed to func 
    text = bc.basic_cleanning(text)  #returned value is in <list> format
    #print(text)
    if text != []:
        with open('train_dataset.csv') as csv_file:
            cl = NaiveBayesClassifier(csv_file,format="csv") 
            #cl = NaiveBayesClassifier() #pass dataset as list
            result = cl.classify(text)
            #print (type(result))  # <str> format 
            prob_dist = cl.prob_classify(text)
            pos_result = round(prob_dist.prob("pos"), 2) 
            neg_result =  round(prob_dist.prob("neg"), 2)
            
            return result
        
        
        
        
        
        
        
        
        
        
        