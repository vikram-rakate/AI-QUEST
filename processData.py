import sys
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def process_data(data):
    df = pd.DataFrame(data)
    
    required_columns = ['questionTitle', 'questionBody', 'questionTags', 'answer']
    if not all(column in df.columns for column in required_columns):
        print("Data is missing required columns.")
        return None

    df["text"] = df["questionTitle"] + " " + df["questionBody"]
    
    df["answer_text"] = df["answer"].apply(lambda x: " ".join([a["answerBody"] for a in x]) if x else "")
    
    return df

def build_similarity_model(df):
    tfidf_questions = TfidfVectorizer(max_features=5000)
    tfidf_answers = TfidfVectorizer(max_features=5000)
    
    question_vectors = tfidf_questions.fit_transform(df["text"])
    answer_vectors = tfidf_answers.fit_transform(df["answer_text"])
    
    joblib.dump(tfidf_questions, "tfidf_questions_vectorizer.pkl")
    joblib.dump(tfidf_answers, "tfidf_answers_vectorizer.pkl")
    joblib.dump(question_vectors, "question_vectors.pkl")
    joblib.dump(answer_vectors, "answer_vectors.pkl")
    joblib.dump(df, "qa_dataframe.pkl")
    
    print("Similarity model built and saved successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data = json.loads(sys.argv[1])
        df = process_data(data)
        
        if df is not None:
            build_similarity_model(df)
    else:
        print("No data received.")
