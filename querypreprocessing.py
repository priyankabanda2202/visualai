import spacy 
nlp = spacy.load("en_core_web_sm") 

# Create a set of stop words 
stop_words = spacy.lang.en.stop_words.STOP_WORDS 

# Define a function to remove stop words from a sentence 
def remove_stop_words(sentence): 
  # Parse the sentence using spaCy 
  doc = nlp(sentence) 
  
  # Use a list comprehension to remove stop words 
  filtered_tokens = [token for token in doc if not token.is_stop] 
  
  # Join the filtered tokens back into a sentence 
  return ' '.join([token.text for token in filtered_tokens])
def query_preprocessing(sentence):
    sentence=sentence.lower()


#sentence = " details by the Population Volume" 

    filtered_sentence = remove_stop_words(sentence) 
    print(filtered_sentence) 
    return filtered_sentence
# Output: "example sentence stop words."



# texts = ["Population_Volume","Provider_Status","Funding_ID","LPP_Claims","Prompt_Pay","State","Provider","Group","SubGroup","LOB","Member","Adj_Reason","Trend_Analysis_Claims_Volumes","Trend_Analysis_Amounts","LPP_Trend_Analysis_Amounts"]
# keyword  = 'trend analysis by claims volume '
# #i=-1
# d1={}
# l1=[]
# l2=[]
# # gives the count of `word in text`
# for i in range(len(texts)): 
# #    print(similar(keyword,texts[i]))
# #    d1.append(texts[i]:similar(keyword,texts[i]))
#     l1.append(similar(keyword,texts[i]))
#     l2.append(texts[i])
#     print(similar(keyword,texts[i]),texts[i])
# print(l1)
# print(l2)
# print(max(l1))