
import streamlit as st
import openai
import os

st.set_page_config(page_title="Resume Matcher LLM", page_icon="🧠")
st.title("🧠 Resume + Job Matcher using GPT")
st.write("Paste your resume and compare against available job descriptions.")

# Get OpenAI API key securely
api_key = st.text_input("Enter your OpenAI API Key:", type="password")
if api_key:
    openai.api_key = api_key

    resume = st.text_area("Paste your Resume Here", height=200)
    jobs = st.text_area("Paste Job Descriptions (separated by 3 dashes ---)", height=200)

    if st.button("Match"):
        if resume and jobs:
            job_list = jobs.split("---")
            prompt = f"Resume: {resume}\n\n"
            prompt += "Given the resume above, find the best job match and explain why from the following list:\n\n"

            for i, job in enumerate(job_list):
                prompt += f"Job {i+1}:\n{job.strip()}\n\n"

            prompt += "Respond with the most suitable job number and explain why it matches best."

            with st.spinner("Matching..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = response['choices'][0]['message']['content']
                    st.success("Match Found:")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter both resume and job descriptions.")
