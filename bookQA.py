import streamlit as st
import pandas as pd
import openai
import os
import json
qlist = ['What is the main idea or central theme of the book?',
       'What are the key lessons or insights from the book, list 10 key lessons?',
       'How can the lessons from the book be applied in daily life, list 5 lessons?',
       'What are some counterarguments or points of disagreement regarding the books content, list 10 points ?',
       'Are there any real-life examples or case studies mentioned in the book, list 5 examples?',
       'What are the potential benefits or positive outcomes of applying the books teachings?',
       'Are there any potential limitations or drawbacks to consider?']
with st.sidebar:
        
        #os.environ['OPENAI_API_KEY'] = st.text_input('Your OpenAI API KEY', type="password")
        openai.api_key = st.text_input('Your OpenAI API KEY', type="password")

def gptcall(book, question):
 
  out = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "system", "content": "Act as an expert book reader and analyst, please provide detailed answers to the following question"},
          {"role": "user", "content": question},
          {"role": "user", "content": book}
      ]
  )

  res = out['choices'][0]['message']['content']
  #print(out['choices'][0]['message']['content'])
  return res


def readdata(df):

  q1,q2,q3,q4,q5,q6,q7 = [],[],[],[],[],[],[]

  for book in df['BookName']:

    for i in range(len(qlist)):
      res = gptcall(book, qlist[i])
      if i == 0:
        q1.append(res)
      elif i == 1:
        q2.append(res)
      elif i == 2:
        q3.append(res)
      elif i == 3:
        q4.append(res)
      elif i == 4:
        q5.append(res)
      elif i == 5:
        q6.append(res)
      elif i == 6:
        q7.append(res)
      


  df['Q1'] = q1
  df['Q2'] = q2
  df['Q3'] = q3
  df['Q4'] = q4
  df['Q5'] = q5
  df['Q6'] = q6
  df['Q7'] = q7

  return df

def main():
    st.title("Question from Books")

    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        st.write("Original CSV:")
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        modified_df = readdata(df)

        st.write("Modified CSV:")
        st.dataframe(modified_df)

        # Download button
        csv_file = modified_df.to_csv(index=False)
        st.download_button(
            label="Download Updated CSV",
            data=csv_file,
            file_name='modified_csv.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
