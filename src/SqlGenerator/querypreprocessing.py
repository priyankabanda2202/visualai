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
    filtered_sentence = remove_stop_words(sentence) 
    print(filtered_sentence) 
    return filtered_sentence

