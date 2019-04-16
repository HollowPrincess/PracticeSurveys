import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


def print_top_words(model, feature_names, n_top_words):
    messageArr = []
    for topic_idx, topic in enumerate(model.components_):
        message = ""
        message += " ".join([feature_names[i]+'/'
                             for i in topic.argsort()[:-n_top_words - 1:-1]])    
        messageArr.append(message)
    return messageArr

def textProcessing(df,coursePortrait,textFields,n_components = 3,n_top_words = 10):    
    tfidf_vectorizer = TfidfVectorizer(lowercase=True,
                                       ngram_range=(2, 2),
                                       stop_words=['russian','english','chinese','japanese','arabic']) 
    
    textres=pd.DataFrame(columns=['курс','поле','количество отзывов','номер темы','тема'])
    
    for textField in textFields:
        frames = [df['курс'],df[textField]]
        textCorpus = pd.concat(frames,axis=1)
        textCorpus = textCorpus.dropna()
        
        for course in coursePortrait['курс']:
            currentTextCorpus=textCorpus.loc[textCorpus['курс'] == course][textField]
            responsesNum=currentTextCorpus.shape[0]
            if responsesNum>3:
                """
                newCorpus=[]
                tmpCorpus=[]
                for response in currentTextCorpus:
                    for word in response.split(' '):
                        tmpCorpus.append(morph.parse(word)[0].normal_form)
                newCorpus.append(" ".join(map(str,tmpCorpus)))
                currentTextCorpus=newCorpus
                """
                tfidf = tfidf_vectorizer.fit_transform(currentTextCorpus)
                
                #print("\n"+course)
                #print("\n Количество отзывов: "+str(responsesNum))
                """
                t0 = time()
                nmf = NMF(n_components=n_components).fit(tfidf)  
                nmftime+=(time() - t0)
                
                t0 = time()   
                lda = LatentDirichletAllocation(n_components=n_components).fit(tfidf)     
                ldatime+=(time() - t0)                
                """
                #t0 = time()   
                svd = TruncatedSVD(n_components=n_components).fit(tfidf)   
                #svdtime+=(time() - t0)
                tfidf_feature_names = tfidf_vectorizer.get_feature_names() 
                themesArr=print_top_words(svd, tfidf_feature_names, n_top_words)
                for i in range(n_components):
                    textres = textres.append({
                        'курс': course,
                        'поле':textField,
                        'количество отзывов':responsesNum,
                        'номер темы': i+1,
                        'тема': themesArr[i]
                    }, ignore_index=True)
    return textres