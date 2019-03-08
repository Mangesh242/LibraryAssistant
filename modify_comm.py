import csv
import classifier_v1 as clf

stu_id = input()
book_id = input()
comment = input()

with open('book_comments_data.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    
    exists = False
    result = ''    
    pos = 0
    neg = 0    
    
    for w in reader:
        if book_id==w[0] and stu_id == w[1]:
            already_exists =  True
            break
    
    
    new_row = [book_id,stu_id,comment,result,pos,neg]
                
    if already_exists==True:
        with open('book_comments_data.csv','w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(new_row)
            csvFile.close()
            
csvFile.close()

