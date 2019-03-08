
import csv
import classifier_v1 as clf

def review_(review):
    print(review)
    pos_result = clf.classify_v1(review) #string passed to this and O/p is also string
    print(pos_result)
            
    return pos_result

