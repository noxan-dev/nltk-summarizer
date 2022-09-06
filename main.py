import requests
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from re import sub
import heapq
import bs4 as bs


def online_parser(user_url):
    url = user_url

    scrapper = requests.get(url)
    parsed_article = bs.BeautifulSoup(scrapper.text, 'html.parser')
    paragraph = parsed_article.find_all('p')

    online_data = ''

    for p in paragraph:
        online_data += p.text

    return online_data


print('Welcome to my NLTK summarizer. With this program You\'ll be able to summarize your files or online sources')
print('Now choose which resource you\'d like to summarize from.')

choice_loop = True

while choice_loop:
    user_resource = input('Type "online" or "file": ').lower()
    if user_resource == 'online':
        user_url_input = input('Please enter a URL: ')
        online_data = online_parser(user_url_input)
        file_data = online_data
        choice_loop = False
    elif user_resource == 'file':
        user_file = input('Please make sure the file is in the "files" folder and enter the file name, with the ext: ')
        with open(f'files/{user_file}', encoding="utf8") as file:
            file_data = file.read().replace('\n', ' ').lower()
        choice_loop = False
    else:
        print('Please type the correct option.')

file_data = sub(r'\[[0-9]*\]', ' ', file_data)
file_data = sub(r'\s+', ' ', file_data)

formatted_file_data = sub('[^a-zA-Z]', ' ', file_data)
formatted_file_data = sub(r'\s+', ' ', formatted_file_data)

sentence_list = sent_tokenize(file_data)

stop_words = stopwords.words('english')

word_frequencies = {}

for word in word_tokenize(formatted_file_data):
    if word not in stop_words:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = word_frequencies[word] / maximum_frequency

sentence_score = {}

for sentence in sentence_list:
    for word in word_tokenize(sentence.lower()):
        if word in word_frequencies.keys():
            if len(sentence.split(' ')) < 30:
                if sentence not in sentence_score.keys():
                    sentence_score[sentence] = word_frequencies[word]
                else:
                    sentence_score[sentence] += word_frequencies[word]

summary_sentence = heapq.nlargest(7, sentence_score, key=sentence_score.get)

summary = ' '.join(summary_sentence)

print(summary)

print('\n')

while True:
    again = input('Would you like to summarize another file? "Y" for yes, "N" for no: ').lower()

    if again == 'y':
        choice_loop = True
    elif again == 'n':
        print('Please come again!')
    else:
        print('Please input the correct option')
