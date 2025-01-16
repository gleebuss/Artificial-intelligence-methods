import streamlit as st
import joblib
from sklearn.pipeline import Pipeline


def load_model(path: str = "./CourseWork/Models/"):
    full_path =  path + "pipeline_model_NB.joblib"
    return joblib.load(full_path)

def check_spam_message(pipeline: Pipeline, message: str):
    predictions, proba = pipeline.predict([message]), pipeline.predict_proba([message])
    if predictions[0] == 1:
        result = f"Это сообщение является спамом с вероятностью {proba[0][1] * 100:.2f}%"
    else:
        result = f"Это сообщение не является спамом с вероятностью {proba[0][0] * 100:.2f}%"
    return result, predictions[0]

def main():
    st.markdown("""<style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .stButton > button {
            display: block;
            margin: 0 auto;
            padding: 10px 40px;
            font-size: 16px;
            font-weight: bold;
            color: white;

            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;

    </style>""", unsafe_allow_html=True)

    pipeline = load_model()

    st.markdown('<div class="centered"><h1>Проверка сообщения на спам</h1></div>', unsafe_allow_html=True)

    user_message = st.text_area("", placeholder="Введите сообщение для проверки")

    if st.button("Проверить сообщение") and user_message.strip():
        result_message, prediction = check_spam_message(pipeline, user_message)
        if prediction == 0:
            st.success(f"{result_message}")
        else:
            st.error(f"{result_message}")
    else:
        st.warning("Пожалуйста, введите сообщение для проверки.")

if __name__ == "__main__":
    main()