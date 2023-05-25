import streamlit as st
import pandas as pd
import openai
import json
openai.api_key = "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"
# def add_columns_to_csv(df):
#     # Add your logic to modify the DataFrame and add columns here
#     df['New Column 1'] = 'Some value'
#     df['New Column 2'] = [1, 2, 3, 4, 5]
#     return df
def gptcall(book):
  question = """
  1-What is the main idea or central theme of the book?
  This question helps readers understand the core concept or message that the author is conveying.

  2-What are the key lessons or insights from the book, list 10 key lessons?
  Summarize the main points and lessons learned to give readers a clear understanding of what they can take away from the book.

  3-How can the lessons from the book be applied in daily life, list 5 lessons?
  Provide practical examples and suggestions on how readers can implement the book's ideas and principles in their own lives.

  4-What are some counterarguments or points of disagreement regarding the book's content, list 10 points ?
  Present alternative perspectives or criticisms that exist surrounding the book's concepts or theories.

  5-Are there any real-life examples or case studies mentioned in the book, list 5 examples?
  Highlight any specific examples or stories that the author uses to support their arguments, demonstrating how the concepts have been applied in the real world.

  6-What are the potential benefits or positive outcomes of applying the book's teachings?
  Discuss the potential advantages, personal growth, or improvements that readers may experience by incorporating the book's principles into their lives.

  7-Are there any potential limitations or drawbacks to consider?
  Address any potential shortcomings or challenges that readers may face when attempting to apply the book's concepts, providing a balanced perspective
  """
  out = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "system", "content": "Act as an expert book reader and analyst, please provide detailed answers to the following seven questions, you need to create seven json keys for each question and data should be return with question number as key value. output sample {'1':answer 1, '2':answer 2, '3': answer 3}"},
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
    temp =  gptcall(book)
    print(temp)
    json_object = json.loads(temp)
    #json_object = json.loads(result)
    q1.append(json_object['1'])
    q2.append(json_object['2'])
    q3.append(json_object['3'])
    q4.append(json_object['4'])
    q5.append(json_object['5'])
    q6.append(json_object['6'])
    q7.append(json_object['7'])

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
