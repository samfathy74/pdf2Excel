import PyPDF2 as pypdf
import pandas as pd
from datetime import datetime
import re
import os

# ``` 
# Question No:n
# Question Contant?
# A.
# B.
# C.
# D.
# Answer:
# Explanation:
# ```

def readFile(filePath):
    try:
        with open(filePath, 'rb') as file:
            pdfFile = pypdf.PdfFileReader(file)
            pagesNum = pdfFile.numPages
            pagesContect=''
            print('reading file please wait...')
            
            for num in range(pagesNum):
                pagesContect+=pdfFile.getPage(pageNumber=num).extract_text().replace('\n', '')
            else : print('Successfully read PDF file..')
            return pagesContect
    except:
        print('enter corret path of pdf file')


# In[452]:
def extractQuestions(fileContent):
    qusetionNum = re.findall('Question No: ?\d', fileContent)

    questions = dict()

    for i, q in enumerate(qusetionNum):
        if q != qusetionNum[-1]:
            x = re.findall(f'(?=Question No: ?{i+1})(.*)(?= Question No: ?{i+2} )', fileContent)
            questions[i+1] = x
        else:
            x = re.findall(f'(?=Question No: ?{i+1})(.*)(?=.)', fileContent)
            questions[i+1] = x
    else : print('Successfully extraction text from PDF file..')
    return questions


# In[818]:
def prepareQuestion(questions):
    answer, explan, question, tempQ = [], [], [], []
    answerA, answerB, answerC, answerD = [],  [], [],  []

    for i, n in enumerate(questions.keys()):

        tempQ.append(str(re.findall(f'(?=\\bQuestion No\: ?{i+1})(.*)(?=\\bA\.)', str(questions[n]))).strip('[]'))
        question.append(re.compile(f'(Question No\: ?{i+1})').sub('', tempQ[i]).strip("'"))
        
        answer.append(re.findall(f'(?<=Answer\:)(.*)(?=Explanation\:)', str(questions[n])))
        explan.append(re.findall(f'(?<=\\bExplanation\:)(.*)', str(questions[n])))
        answerA.append(re.findall(f'(?<=\\bA\.)(.*)(?=\\bB\.)', str(questions[n])))
        answerB.append(re.findall(f'(?<=\\bB\.)(.*)(?=\\bC\.)', str(questions[n])))
        answerC.append(re.findall(f'(?<=\\bC\.)(.*)(?=\\bD\.)', str(questions[n])))
        answerD.append(re.findall(f'(?<=\\bD\.)(.*)(?=\\bAnswer\:)', str(questions[n])))
        
    return question, answer, explan, answerA, answerB, answerC, answerD


if __name__ == "__main__":
    path = input('Enter the path of PDF file: ')
    while True:
        if (os.path.exists(path) or os.path.isfile(path)) and (path.endswith('.pdf') or path.endswith('.PDF')):
            break
        else:
            path = input('Enter correct path of PDF file: ')
    
    # read file
    fileContant = readFile(path)    

    # extract all questions from file
    extactContant = extractQuestions(fileContant)
    
    # extract question, answer, explanation, answerA, answerB, answerC, answerD
    question, answer, explan, answerA, answerB, answerC, answerD = prepareQuestion(extactContant)

    # prepare data to parse into dataframe
    data = dict(
        {
            'Question':question,
            'answerA': [item for sublist in answerA for item in sublist],
            'answerB':[item for sublist in answerB for item in sublist],
            'answerC':[item for sublist in answerC for item in sublist],
            'answerD':[item for sublist in answerD for item in sublist],
            'Answer': [item for sublist in answer for item in sublist],
            'Explanation': [item for sublist in explan for item in sublist],
        }
    )

    
    # last step to convert data into dataframe
    name = str(datetime.now())[:20].replace(' ', '_').replace(':', '_')
    pd.DataFrame(data).to_csv(f'output_{name}.csv')
# %%
