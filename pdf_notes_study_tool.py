# coding: utf-8
import PyPDF2
import sys
import re

#conda activate problem72
#conda deactivate problem72


'''
provide files in command line, put pdf in separate directory, provide path with *.pdf
as argument
extract text from pdf and writes to a "filename_text.txt" file

testcode instruction provided at the end

'''

#converts pdf into textfile
#header with filepath, followed by page number
#sections starting with "Page xx" then text, sections separated by newlines

def convert_txt(filename):

    global converted_files

    try:
        f = open(filename, 'r')
        f.close()
    except:
        print("Please provide a file that exists")
    
    
    pdf_object = open(filename, 'rb')
    pdf_Reader = PyPDF2.PdfFileReader(pdf_object)
    total_pages = int(pdf_Reader.numPages)

    f1=open(filename + '_text.txt', 'w')
    converted_files.append(filename + "_text.txt")
    f1.write('%s' % filename + '\n')

    f1.write('PagesTotal = ' + str(total_pages) + '\n')

    for i in range(total_pages):
        pageOBJ = pdf_Reader.getPage(i)
        f1.write("Page "+ str(i) +"\n")
        xx = pageOBJ.extractText()
        zz = xx.encode("ascii", 'ignore')
        f1.write(zz + "\n\n")

#removes punctuation
def remove_punc(word):
    punctuations = '''!()-[]{};:“'”"\"\,<>./?@#$%^&*_~'''
    no_punct_str = ""
    for char in word:
        if char not in punctuations:
            no_punct_str = no_punct_str + char
    return no_punct_str  

#takes filename argument, returns word frequency for each file
def wordfrequency(filename):
    glossary = {}

    f = open(filename, "r")

    #preparing the string
    for line in f:
        t = line.strip()
        x = str(t)
        y = x.lower()
        e = remove_punc(y)
        z = e.split(" ")    
        #looping through string that is now list of words, adding to glossary
        for j in z:
            try:
                glossary[j] += 1
            except KeyError:
                glossary[j] = 1
    
    t = open(filename + "_wordfreq.txt", "w")

    for key, value in glossary.items():
        t.write(str(key) + " - " + str(value) +" \n")
    
    t.close
    f.close
 
        
#take keyword as argument, return glossary
#glossary key = filename/filepath, value = list of page numbers with word match

def search_word(word):

    glossary1 ={}
    glossary_page_number=[]

    global converted_files

    for each in converted_files:
        f = open(each, 'r')
        for num, line in enumerate(f):
            t = line.strip()
            x = str(t)
            e = remove_punc(x)
            z = e.split(" ") 
            for i in range(len(z)):
                if z[i] == "Page": 
                    #an error might occur here if there is some line in some pdf that has "Page" ending the line, giving IndexError
                    #but this is pretty peculiar, and thus far, all the pdfs of lecture slides does not have this
                    glossary_page_number.append([num, z[i+1] ])

                if z[i] == word:
                    try:
                        glossary1[each].append(glossary_page_number[-1][1])
                    except KeyError:
                        glossary1[each] = []
                        glossary1[each].append(glossary_page_number[-1][1])
        f.close()
    

    return glossary1






def main():
    args = sys.argv[1:]

    global converted_files
    converted_files =[]

    if not args:
        print('Please provide input as filename/filepath')
        sys.exit(1)
    
    for each in args:
        convert_txt(each)

    
    
    for each in converted_files:
        wordfrequency(each)

    

    

if __name__ == '__main__':
    main()


#testcode instructions

#put pdf of lectures slides pdf in a folder
#run on command line % python problem7.py filepath_of_pdf_directory/*.pdf
#should create .txt files for each pdf file
#should also create a _wordfreq.txt file for each pdf file (list)
#alternatively, run main(), run convert_txt(filename/filepath)
#after doing these
#use method problem7.search_word("someword")
#or add line in this file code: output = search_word("someword")
#will return a glossary, that has keys = filepath/filename, value = list of pagenumbers that contain "someword"
