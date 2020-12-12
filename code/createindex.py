"""
This file contains your code to create the inverted index. Besides implementing and using the predefined tokenization function (text2tokens), there are no restrictions in how you organize this file.
predefined functions if available.
"""
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import lxml.html as ET
import invertedindex as idx
import re
import os
import time
import datetime

porst = PorterStemmer()

def text2tokens(text):
    """
    lowercasing, stopword removal, stemming
    :param text: a text string
    :return: a tokenized string with preprocessing (e.g. stemming, stopword removal, ...) applied
    """
    lower = text.casefold()
    tokens = ""
    for word in lower.split():
        if word in stopwords.words('english'):
            continue
        alphaNumOnly = re.sub(r'[^a-zA-Z0-9 ]', '', word)
        token = porst.stem(alphaNumOnly)
        tokens += token + " "

    return tokens

testindex = idx.InvertedIndex()
tree = ET.parse('dev-set/1.xml')


data = 'The Detroit College of Medicine was founded in 1868 in a building on Woodward Avenue. The Michigan College of Medicine was incorporated in 1879 and offered classes in the former Hotel Hesse at the intersection of Gratiot Avenue, Madison Avenue and St. Antoine Street. In 1885, the two schools merged to form the Detroit College of Medicine and occupied the former Michigan College of Medicine building. The college was reorganized and refinanced as the Detroit College of Medicine and Surgery in 1913, and five-years later, came under control of the Detroit Board of Education. In 1933, the Board of Education joined the Detroit College of Medicine and Surgery with the colleges of Liberal Arts, Education, Engineering, Pharmacy, and the Graduate School to form an institution of higher education called the Colleges of the City of Detroit. This was renamed Wayne University in 1934 and became a state-chartered institution, Wayne State University, in 1956.[3] The dean is Dr. Mark E. Schweitzer. '
tok = text2tokens(data)
for elmt in tok.split(" "): 
    testindex.add(elmt, 123)
print(testindex)


# articles = tree.xpath('//article')
# artCount = len(articles)
# counter = 1
# startTime = time.time()
# for a in articles:
#     if(counter > 3):
#         continue
#     artID = a.xpath('header/id/text()')[0]
#     contentstring = a.xpath('header/title/text()')[0] + a.xpath('bdy/text()')[0]
#     tokenstring = text2tokens(contentstring)
#     for tk in tokenstring.split(" "):
#         testindex.add(tk,artID)
#     perc = round((counter/artCount)*100)
#     os.system('cls')
#     print("Working on article " + str(counter) + " of " + str(artCount) +"...   (" + str(perc) + "% done)")
#     counter += 1

# print(testindex)

# print("Done. Execution Time: " + str(datetime.timedelta(seconds=round(time.time() - startTime))))
