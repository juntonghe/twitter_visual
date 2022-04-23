from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
import numpy

#data preprocessing
dataset = pd.read_csv('sentiment_result.csv', lineterminator='\n')
dataset = dataset[['text', 'predict_label']]
dataset.columns = ['text', 'predict_label']
label_0 = []
label_1 = []
label_2 = []
for index, row in dataset.iterrows():
    if row[1] == 0:
        label_0.append(row[0])
    elif row[1] == 1:
        label_1.append(row[0])
    elif row[1] == 2:
        label_2.append(row[0])

label_0 = ''.join(label_0)
label_1 = ''.join(label_1)
label_2 = ''.join(label_2)

#put words you do not want to display in a stopwords list
stopwords = ['t', 'https', 'co', 's'] + list(STOPWORDS)

#generate wordclouds
wordcloud = WordCloud(
    background_color='white',
    width=2000,
    height=1000,
    margin=10,
    max_words=150,
    stopwords=stopwords
)

wordcloud0 = wordcloud.generate(label_0)
plt.imshow(wordcloud0)
plt.title('negative sentiment wordcloud')
plt.axis('off')
plt.savefig('./negative.jpg')
plt.show()

wordcloud1 = wordcloud.generate(label_1)
plt.imshow(wordcloud1)
plt.title('neutral sentiment wordcloud')
plt.axis('off')
plt.savefig('./neutral.jpg')
plt.show()

wordcloud2 = wordcloud.generate(label_2)
plt.imshow(wordcloud2)
plt.title('positive sentiment wordcloud')
plt.axis('off')
plt.savefig('./positive.jpg')
plt.show()

