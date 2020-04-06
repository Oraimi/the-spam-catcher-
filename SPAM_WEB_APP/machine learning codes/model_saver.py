import nltk
import pickle
import string
import warnings
import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

warnings.filterwarnings("ignore")
nltk.download('stopwords')


def mapper(txt):
  return [word for word in ''.join([char for char in txt if char not in string.punctuation]).split() if word.lower() not in stopwords.words('english')]


def main():
    df = pd.read_csv('C:\\Users\\Mr Ammonia\\Downloads\\emails.csv')
    keeper = pickle.load(open('dict', 'rb'))
    data = list()
    for index, row in tqdm(df.iterrows()):
        temp_row = [0] * len(keeper)
        for i in mapper(row.text):
            temp_row[keeper.index(i)] += 1
        data.append(temp_row)
    X_train, X_test, Y_train, Y_test = train_test_split(data, df.spam, test_size = 0.10, random_state = 0)
    classifiers = [['Logistic Regression :', LogisticRegression()],
                   ['Decision Tree Classification :', DecisionTreeClassifier()],
                   ['Gradient Boosting Classification :', GradientBoostingClassifier()],
                   ['Ada Boosting Classification :', AdaBoostClassifier()],
                   ['Extra Tree Classification :', ExtraTreesClassifier()],
                   ['K-Neighbors Classification :', KNeighborsClassifier()],
                   ['Support Vector Classification :', SVC()],
                   ['Gaussian Naive Bayes :', MultinomialNB()]]
    cla_pred = []
    for name, model in classifiers:
        try:
            model = model
            model.fit(X_train, Y_train)
            pickle.dump(model, open(name.split()[0], 'wb'))
            predictions = model.predict(X_test)
            cla_pred.append(accuracy_score(Y_test, predictions))
            print(name, accuracy_score(Y_test, predictions))
        except MemoryError:
            pass


if __name__ == '__main__':
    # main()
    print(pickle.load(open("C:\\Users\\Mr Ammonia\\Downloads\\MODEL.pk",'rb')).predict)