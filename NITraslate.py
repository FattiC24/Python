import urllib.request
import re
import nltk
from inscriptis import get_text
from nltk import word_tokenize, sent_tokenize
from googletrans import Translator

translator = Translator()

#nltk.download()

cadena = """NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 
corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, 
and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.
Thanks to a hands-on guide introducing programming fundamentals alongside topics in computational linguistics, plus comprehensive API documentation, 
NLTK is suitable for linguists, engineers, students, educators, researchers, and industry users alike. NLTK is available for Windows, Mac OS X, and Linux. 
Best of all, NLTK is a free, open source, community-driven project.
NLTK has been called a wonderful tool for teaching, and working in, computational linguistics using Python, and an amazing library to play with natural language."""
#enlace = "https://es.wikipedia.org/wiki/Python"
#html = urllib.request.urlopen(enlace).read().decode('utf-8')
text = get_text(cadena)

print("############################################")

#Removing square brackets and extra spaces
formatted_article_text = re.sub('[^a-zA-z]', ' ', text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(text)
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

#CALCULA LA FRASE QUE MAS SE REPITE
sentence_scores ={}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 20:
                if sent not in  sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

#REALIZA EL RESUMEN CON LAS MEJORES FRASES
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)

summary = translator.translate(summary, dest='es').text
print(summary)
print("*********************************")