# Explaining how you approached the solution
""" 
1. Importing all the required libraries like - Pandas, numpy, requests, re, string, beatifulsoup, nltk, nltk-tokenizer, nltk-stopwords

2. Data Extraction  - Iterate in using pandas Dataframe input.xlsx that having url_id and url. By using these url extract the information like title and article.
                      Title are stored in 'h1' tag and Article are stored in 'p' tag in with calss = "td-post-content tagdiv-type" and some
                      url's Tilte are stored in 'hi' but article is not stored in calss = "td-post-content tagdiv-type" so extract the p tag only
                      using the python module BeautifulSoup 

3. Data cleaning - clean article using the stopwords folder like if article having any word that word present in stopwords folder's text file 
                   remove it and also remove punctuation for better result.

4. Retrieveing information - for Retrieveing from text define function for - 
        1. Extracting Derived variables - using Master Dictionary folder that having two text files Positive words and Negative words
            Derived variables are positive score, negative score, polarity score and subjectivity score are
             - Positive Score = +1 for each word if found in the Positive Dictionary and then adding up all the values. 
                - Negative Score = -1 for each word if found in the Negative Dictionary and then adding up all the values. We multiply 
                                the score with -1 so that the score is a positive number.
                - Polarity Score = Calculate by using the formula and range is from -1 to +1 = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
                - Subjectivity Score = Calculate by using the formula and range is from -1 to +1 = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
        
        2. Analysis of Readability - using Gunning Fox index formula are
                - Average Sentence Length = the number of words / the number of sentences
                - complex words - Complex words are words in the text that contain more than two syllables
                - Percentage of Complex words = the number of complex words / the number of words
                - fog index - 0.4 * (average sentence length + percentage of complex words)

        3. Average Number of Words Per Sentence
                - The formula for calculating is:
                - Average Number of Words Per Sentence = the total number of words / the total number of sentences

        4. Complex Word Count
                Complex words are words in the text that contain more than two syllables.

        5. word count - 1. using nltk stopwords clean the text of article like if text having any word in stopwords remove is
                        2. remove punctuation form text 
                - After removing the stopwords and punctuation iterate in text and count words

        6. Syllable Count Per Word - check the word is not endwith "es" and "ed".
                                    - count the vowels "aeiou" present in the words using pyhton re module for each word

        7. Personal pronouns - count the word like “I,” “we,” “my,” “ours,” and “us” how many time present in the article
                                - do not count the words like "IT" and "US" it means Information Technology and United state
                                it is not pronouns words it is filed of computer science and country name  

        8. Average word length - Average Word Length is calculated by the formula:
                Sum of the total number of characters in each word of article / Total number of words in article

5. Function output - store all the output of the function in related lists
                        
. Output export - Using these related lists create an Dataframe that sotred output and exported using dataframe function to_csv 
"""

# Importing the important libraries 

import pandas as pd # use to create Dataframe that stores inputs of function and exports into CSV file
import numpy as np  # use only for returning the np.nan 
import requests     # use for establish connection with web or url 
import re           # use to finding patterns in text and spliting the text
import string       # use for text cleaning 
from bs4 import BeautifulSoup           # use for extacting data form web's or url's that inside its HTML

import nltk     # use for its method like stopwords and tokenizers
# Download NLTK resources stopwords
nltk.download('stopwords')      # having the list of stopwords that use to cleaning text
nltk.download('punkt_tab')
from nltk.corpus import stopwords # import the stopwords list 
from nltk.tokenize import word_tokenize # use for tokenize the words 

print("\nPackages are importing succesfully")

# This function is use for CONNECTING and EXTRACTING the Title and Article from url
def scraper(url):
    
    webpage = requests.get(url)                                                 # connecting with url using requests module
    extractor = BeautifulSoup(webpage.text,'html.parser')                              # defining the exteactor variable that store the HTML content of url using Beautifulsoup module

    # Check if the response status code is successful (200 OK)
    if webpage.status_code == 200:
        # Handling the error while extracting Title and Article
        try:                                                                        
            title = extractor.find_all('h1')[0].text                                # Storing the Title of webpage using Beautifulsoup method find_all that is in webpage's HTML h1
            article = extractor.find_all(class_="td-post-content tagdiv-type")      # Storing the Article of webpage using Beautifulsoup method find_all that is in div of calss "td-post-content tagdiv-type"
            article_text = article[0].text.strip()                                  # Retrieving the Article's text that Stored in article variable as string

        # if any error occurs in try block while extracting the Title and Article then this expect block run behalf of try block
        except:
            title = extractor.find_all('h1')[0].text                                # Storing the Title of webpage using Beautifulsoup method find_all that is in webpage's HTML h1
            paragraphs = extractor.find_all('p',class_=False)                       # Storing all the paragraphs of webpage's HTML where not including any class and its information in class using Beautifulsoup method find_all
            article_text = '\n'.join(paragraph.text for paragraph in paragraphs)    # Retrieving the Article's text that Stored in paragraphs variable as string

        return {'title':title,'article':article_text}                               # returning the Title and the Article of URL's webpage
    
    # if any other exception error while connecting the url handle in this else block
    else:
        return webpage.status_code              # returning the title as "Page not found!" and article as np.nan because webpage is not connected
    


# This function returns the dictionary of Derived Variable that is Positive Score, Negative Score, Polarity Score and Subjectivity Score of article
def extracting_Derived_Variables(text):

    # Convert text to lowercase if it's a string
    if isinstance(text, str):
        
        text_lower = text.lower()
         
        punctuation = string.punctuation                                             # Use string.punctuation to get all punctuation characters
        clean_text = text_lower.translate(str.maketrans('', '', punctuation))        # Use str.translate() to remove punctuation characters from text
        clean_words = word_tokenize(clean_text)                                      # tokenize the string using the nltk.tokenize method word_tokenize

        StopWords_Auditor = open('Stopwords\StopWords_Auditor.txt').read()                   # Creating the list of StopWords_Auditor that inside the folder stopwords
        StopWords_Currencies = open('Stopwords\StopWords_Currencies.txt').read()             # Creating the list of StopWords_Currencies that inside the folder stopwords
        StopWords_DatesandNumbers = open('Stopwords\StopWords_DatesandNumbers.txt').read()   # Creating the list of StopWords_DatesandNumbers that inside the folder stopwords
        StopWords_Generic = open('Stopwords\StopWords_Generic.txt').read()                   # Creating the list of StopWords_Generic that inside the folder stopwords
        StopWords_GenericLong = open('Stopwords\StopWords_GenericLong.txt').read()           # Creating the list of StopWords_GenericLong that inside the folder stopwords
        StopWords_Geographic = open('Stopwords\StopWords_Geographic.txt').read()             # Creating the list of StopWords_Geographic that inside the folder stopwords
        StopWords_Names = open('Stopwords\StopWords_Names.txt').read()                       # Creating the list of StopWords_Names that inside the folder stopwords

        # Creating the list of all stopwords with merge all the stopwords list variables
        list_of_stopwords = StopWords_Auditor + StopWords_Currencies + StopWords_DatesandNumbers + StopWords_Generic + StopWords_GenericLong + StopWords_Geographic + StopWords_Names
    
        positive_word = open('MasterDictionary/positive-words.txt','r').read().split()      # Creating the list of positive words that inside the folder MasterDictionary
        negative_word = open('MasterDictionary/negative-words.txt','r').read().split()      # Creating the list of negative words that inside the folder MasterDictionary

        
        # Creating the list of positive word in the article that inside the list of positive word and not inside in list of stopwords
        clean_txt_positive = [word for word in clean_words if word in positive_word and word not in list_of_stopwords]
    
        # Creating the list of negative word in the article that inside the list of negative word and not inside in list of stopwords
        clean_txt_negative = [word for word in clean_words if word in negative_word and word not in list_of_stopwords]
    
        # Calculate the Positive Score of the article 
        positive_score = sum(1 for word in clean_txt_positive if word in positive_word and word not in list_of_stopwords)
        # Calculate the Negative Score of the article
        negative_score = sum(1 for word in clean_txt_negative if word in negative_word and word not in list_of_stopwords)
        # Calculate the Polarity Score of the article
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        # Calculate the Subjectivity Score of the article
        subjectivity_score = (positive_score + abs(negative_score)) / (len(clean_text) + 0.000001)  
        
        return {'positive score':positive_score,'negative score':negative_score,'polarity score':polarity_score,'subjectivity score':subjectivity_score}


    # if it is not a string then return all variables is not Avilable
    else:
        return {'positive score':'Not Avilable','negative score':'Not Avilable',
                'polarity score':'Not Avilable','subjectivity score':'Not Avilable'}
    


# This function returns the dictionary of analysis of Readability Variable that is Average Sentence Length, Percentage Complex Words and Fog Index of the article
def analysis_of_Readability(text):

    # Convert text to lowercase if it's a string
    if isinstance(text, str):

        text_lower = text.lower()

        # Counting sentences
        sentences = re.split(r'[.!?]', text_lower)                      # Spliting the text for makeing the sentences as a list using re module fuction split
        num_sentences = len(sentences)                                  # counting the sentences that stored in sentences variable


        punctuations = string.punctuation                                                    # Creating the list of punctuation using srting punctuation method
        clean_punctuation_text = text_lower.translate(str.maketrans('', '', punctuations))   # Use str.translate() to remove punctuation characters from text
        clean_words = word_tokenize(clean_punctuation_text)                                  # Tokenize the text into words

        # Counting words
        num_words = len(clean_words)

        # Counting complex words
        complex_words = [word for word in clean_words if len(re.findall(r'[aeiouy]+', word)) > 2]         # Creating the list of complex words using pattern finding of re module function findall
        complex_word_count = sum(1 for word in complex_words if len(re.findall(r'[aeiouy]+', word)) > 2)  # counting the complex words that sotred complex words variable
        
        # Calculating average sentence length
        average_sentence_length = num_words / num_sentences 

        # Calculating percentage of complex words
        percentage_complex_words = (complex_word_count / num_words) * 100
        
        # Calculating Fog Index
        fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
        
        return {'average sentence length':average_sentence_length,'percentage complex words':percentage_complex_words,'fog index':fog_index}

    # if it is not a string then return all variables is not Avilable
    else:
        return {'average sentence length':'Not Avilable','percentage complex words':'Not Avilable','fog index':'Not Avilable'} 
            


# This function return the Average words per sentences in the article
def average_Number_of_Words_Per_Sentence(text):

    # Convert text to lowercase if it's a string
    if isinstance(text, str):

        text_lower = text.lower()

        punctuations = string.punctuation                                                    # Use string.punctuation to get all punctuation characters
        clean_punctuation_text = text_lower.translate(str.maketrans('', '', punctuations))   # Use str.translate() to remove punctuation characters from text
        clean_words = word_tokenize(clean_punctuation_text)                                  # Tokenize the text into words
        
        #counting words
        num_words = len(clean_words)

        # Counting sentences
        sentences = text_lower.split(".")        # Spliting the sentence with '.'dot 
        num_sentences = len(sentences)

        # Calculating the average word length
        avg_word = num_words/num_sentences
        
        return avg_word

    # if it is not a string then return not Avilable
    else:
        return 'Not Avilable'
    
    

# This function return the count of complex words in the article
def complex_Words_Count(text):

    # Convert text to lowercase if it's a string
    if isinstance(text, str):
        
        text_lower = text.lower()

        punctuations = string.punctuation                                                    # Use string.punctuation to get all punctuation characters
        clean_punctuation_text = text_lower.translate(str.maketrans('', '', punctuations))   # Use str.translate() to remove punctuation characters from text
        clean_words = word_tokenize(clean_punctuation_text)                                  # Tokenize the text into words using nltk.tokenize method word_tokenize
        
        # Find and count the complex words if the words with more than two syllables using pattern finding of re module function findall
        complex_count = sum(1 for word in clean_words if len(re.findall(r'[aeiouy]+',word)) > 2)

        return complex_count
    
    else:
        return 'Not Avilable'
    


# Function to count cleaned words in the article
def count_Cleaned_Words(text):

    # Convert text to lowercase if it's a string
    if isinstance(text, str):
        
        text_lower = text.lower()

        # string that removing 
        stop_words = set(stopwords.words('english')) # creating the set of stopwords using nltk.corpus method stopword

        punctuations = string.punctuation                                                    # Use string.punctuation to get all punctuation characters
        clean_punctuation_text = text_lower.translate(str.maketrans('', '', punctuations))   # Use str.translate() to remove punctuation characters from text
        clean_words = word_tokenize(clean_punctuation_text)                                  # Tokenize the text into words using nltk.tokenize method word_tokenize
        
        cleaned_words = [word for word in clean_words if word.lower() not in stop_words]

        # count of clean words
        count = len(cleaned_words)

        return count
        # if it is not a string then return Not avilable
    
    else:
        return 'Not Avilable'


# This function return the dictionary of count of syllables per words in the article
def count_Syllables_Per_Word(text):

    # Define a function to count syllables in a word
    def count_syllables(word):

        # Handling exceptions like words ending with "es" or "ed"
        if word.endswith("es") or word.endswith("ed"):
            return max(1, len(re.findall(r'[aeiouy]+', word.lower())) - 1) # counting the syllables of word 
        
        # If word is not having exceptions like words ending with "es" or "ed"
        else:
            return max(1, len(re.findall(r'[aeiouy]+', word.lower())))     # counting the syllables of word 
    
    # Convert text to lowercase if it's a string
    if isinstance(text, str):

        text_lower = text.lower()

        punctuations = string.punctuation                                                    # Use string.punctuation to get all punctuation characters
        clean_punctuation_text = text_lower.translate(str.maketrans('', '', punctuations))   # Use str.translate() to remove punctuation characters from text
        clean_words = word_tokenize(clean_punctuation_text)                                  # Tokenize the text into words

        # Count syllables for each word
        syllable_count = {word: count_syllables(word) for word in clean_words}               # counting the syllables of word using count_syllables function

        return syllable_count
        
    else:  # Handle the case when text is not a string
        return 'Not Available'
    


# This function return the count of personal pronoun in the article
def count_Personal_Pronouns(text):

    # Convert text to lowercase if it's a string
    if isinstance(text, str):
        # Define the pattern to match personal pronouns
        pattern = r'\b(?:I|we|my|ours|and|us)\b'

        # Find all matches of the pattern in the text
        matches = re.findall(pattern, text , flags=re.IGNORECASE)

        # Exclude instances where "US" and "IT" refers to the country name and information technology 
        matches = [match for match in matches if match != 'IT' and match != 'US']
        
        # Count the occurrences of personal pronouns
        count = len(matches)

        return count
    
    # if it is not the string then return not avilable
    else:
        return 'Not Avilable'
    


# This function return the Average word length in the article
def average_Word_Length(text):

    # Convert text to lowercase if it's a string
    if isinstance(text, str):

        text_lower = text.lower()

        punctuations = string.punctuation                                                    # Use string.punctuation to get all punctuation characters and creating the list of that
        clean_punctuation_text = text_lower.translate(str.maketrans('', '', punctuations))   # Use str.translate() to remove punctuation characters from text
        clean_words = word_tokenize(clean_punctuation_text)                                  # Tokenize the text into words using nlt.tokenizer method word tokenizer
        
        # count the total number of characters in each word
        total_characters = sum(len(word) for word in clean_words)
        
        # Count the total number of words
        total_words = len(clean_words)
        
        # Calculate the average word length
        average_word_length = total_characters / total_words 

        return average_word_length
    
    # if it is not a string then return not avilable
    else:
        return 'Not Avilable'
               

# main function
def main():

    # These lists are for storing the data that extract from web
    title = []                                  # this list store the title of the article
    article = []                                # this list store the article  
    filename = []                               # this list store the filename of the article

    # These lists are for storing the data that extract from webpage article 
    positive_score = []                         # list store the positive score of the article
    negative_score = []                         # list store the negative score of tha article
    polarity_score = []                         # list store the polarity score of tha article
    subjective_score = []                       # list store the subjective score of tha article
    avg_sentence_length = []                    # list store the avrage sentence lenght of tha article
    percentage_of_complex_words = []            # list store the precentage of complex word
    fog_index = []                              # list store the fog index of tha article
    avg_number_of_words_per_sentence = []       # list store the avrage number of words per sentence of tha article
    comples_word_count = []                     # list store the complex word count of tha article
    word_count = []                             # list store the word count of tha article
    syllables_per_word = []                     # list store the sullables per words of tha article
    personal_pronouns = []                      # list store the personal pronoun of tha article
    avg_word_length = []                        # list store the avreage word length of tha article



    # load data in dataframe for iteration 
    df_input = pd.read_excel('input.xlsx')
    
    for index,data in df_input.iterrows():                  # using Dataframe method iterrows for iteration 
        url_id, url = data.iloc[0], data.iloc[1]            # assign the data into variable
        webpage = scraper(url)                              # passing the url in the scraper function
        
        # if connection is not establish with url 
        if webpage == 404 :
            print("Data extaeacting error : ",url_id,"Connection Code :",webpage,"Webpage not found : ",url)    # Display the url_id and url of that webpage having problem
            webpage = {'title':'Page not found!','article':np.nan}                                              # Storing the title Page not found! and article as np.nan 


        filename.append(url_id)                  # Appending the filename in the list of filename
        title.append(webpage['title'])           # Appending the title in the list of title
        article.append(webpage['article'])       # Appending the article in the list of article


        # extracting_derived_variables using extracting_Derived_Variables function
        derived_variable = extracting_Derived_Variables(webpage['article'])         # the function return in the form of dictionary stored in variable 
        
        # Appending the values of dictionary variable into there related list 
        positive_score.append(derived_variable.get('positive score'))               # Appending the positive score in the positice score list
        negative_score.append(derived_variable.get('negative score'))               # Appending the negative score in the negative score list
        polarity_score.append(derived_variable.get('polarity score'))               # Appending the polarity score in the polarity score list
        subjective_score.append(derived_variable.get('subjectivity score'))         # Appending the subjective score in the subjective score list


        # analysi_of_Readability using analysi_of_Readability
        readability = analysis_of_Readability(webpage['article'])                           # the function return in the form of dictionary stored in variable 

        avg_sentence_length.append(readability.get('average sentence length'))              # Appending the average sentence length in the avg_sentence_length list
        percentage_of_complex_words.append(readability.get('percentage complex words'))     # Appending the percentage of complex words in the percentage_of_complex_words list
        fog_index.append(readability.get('fog index'))                                      # Appending the fog index in the fog_index list


        #average_Number_of_Words_Per_Sentence
        avg_number_of_words_per_sentence.append(average_Number_of_Words_Per_Sentence(webpage['article']))    # Appending the average number of words per sentence in the average_Number_of_Words_Per_Sentence list


        #comples_word_count
        comples_word_count.append(complex_Words_Count(webpage['article']))                                   # Appending the comples word count in the complex_Words_Count list


        # word_count
        word_count.append(count_Cleaned_Words(webpage['article']))                                           # Appending the word count in the count_Cleaned_Words list


        # syllables_per_word
        syllables_per_word.append(count_Syllables_Per_Word(webpage['article']))                              # Appending the syllables per words in the count_Syllables_Per_Word list


        # personal_pronouns
        personal_pronouns.append(count_Personal_Pronouns(webpage['article']))                                # Appending the personal pronoun count in the count_Personal_Pronouns list


        # avg_word_length
        avg_word_length.append(average_Word_Length(webpage['article']))                                      # Appending the average word lenght in the average_Word_Length list 


        print("Data extaeacting done :",url_id)

    print("\nInformation and variables are retrive succesfully")    
    # creating the dataframe with extracted information that stored in lists
    df_output = pd.DataFrame({'URL_ID':filename,'URL':title,'Article':article,'POSITIVE SCORE':positive_score,'NEGATIVE SCORE':negative_score,
                    'POLARITY SCORE':polarity_score,'SUBJECTIVE SCORE':subjective_score,'AVG SENTENCE LENGTH':avg_sentence_length,
                    'PERCENTAGE OF COMPLEX WORDS':percentage_of_complex_words,'FOG_INDEX':fog_index,'AVG NUMBER OF WORD PER SENTENCE':avg_number_of_words_per_sentence,
                    'COMPLES WORD COUNT':comples_word_count,'WORD COUNT':word_count,'SYLLABLE PER WORD':syllables_per_word,'PERSONAL PRONOUNS':personal_pronouns,
                    'AVG WORD LENGTH':avg_word_length})
    
    print("\nDataframe load from extrated data succesfully ")

    # Exporting the output as output.csv 
    df_output.to_csv('Output Data Structure updated 2.csv',index=False)

    print("\nOutput exported succesfully")
    
if __name__ == "__main__":
    main()
