import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# Set page configuration
st.set_page_config(
    page_title="CoDApplication",
    layout="wide",
)

# Define helper functions for Chain of Draft (CoD) implementation
def chain_of_draft_arithmetic(input_question, draft_length=5):
    """
    Implements the Chain of Draft technique for arithmetic reasoning.
    Produces concise intermediate steps to solve the problem.
    """
    question_parts = input_question.split()
    try:
        if "lollipops" in question_parts:
            initial = int(question_parts[2])
            remaining = int(question_parts[-3])
            given = initial - remaining
            return f"{initial} - x = {remaining}; x = {given}", given
        return "Unsupported question format", None
    except:
        return "Error in processing the question", None

def generate_synthetic_data(num_samples=100):
    """
    Generates synthetic data for experimental setup.
    """
    data = []
    for _ in range(num_samples):
        initial = np.random.randint(10, 50)
        given = np.random.randint(1, initial)
        remaining = initial - given
        question = f"Q: A person had {initial} items. They gave away some items. Now they have {remaining} items. How many items did they give away?"
        data.append((question, given))
    return pd.DataFrame(data, columns=['Question', 'Answer'])

# Sidebar configuration
st.sidebar.header("Configuration")
mode = st.sidebar.selectbox("Select Mode", ["Experiment", "Comparison"])
num_samples = st.sidebar.slider("Number of Samples", 10, 500, 100)
draft_length = st.sidebar.slider("Draft Length (words)", 1, 10, 5)

# Main app layout
st.title("Chain of Draft Application")
st.markdown("""
This application demonstrates the Chain of Draft (CoD) technique for efficient reasoning in large language models.
""")

st.header("1. Chain of Draft Experimentation")
st.write("Experiment with the Chain of Draft technique using synthetic data.")

# Experiment section
if mode == "Experiment":
    st.subheader("Synthetic Data Generation")
    st.write("Generate synthetic questions for arithmetic reasoning.")
    data = generate_synthetic_data(num_samples)
    st.dataframe(data)

    st.subheader("Run Chain of Draft")
    results = []
    for question in data['Question']:
        draft, answer = chain_of_draft_arithmetic(question, draft_length)
        results.append((question, draft, answer))
    
    results_df = pd.DataFrame(results, columns=['Question', 'Draft', 'Computed Answer'])
    st.dataframe(results_df)

    st.subheader("Visualization")
    fig, ax = plt.subplots()
    ax.hist(results_df['Computed Answer'], bins=20, color='skyblue', edgecolor='black')
    ax.set_title('Distribution of Computed Answers')
    ax.set_xlabel('Answer')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

st.header("2. Comparison with Other Techniques")
st.write("Compare Chain of Draft with Chain of Thought and Standard prompting.")

# Comparison section
if mode == "Comparison":
    compare_data = generate_synthetic_data(num_samples)
    st.subheader("Comparison Data")
    st.dataframe(compare_data)

    st.subheader("Run Comparisons")
    comparison_results = []
    for question in compare_data['Question']:
        cod_draft, cod_answer = chain_of_draft_arithmetic(question, draft_length)
        cot_draft = "Detailed reasoning steps go here"  # Simulate CoT
        std_answer = "Direct answer goes here"  # Simulate Standard
        comparison_results.append((question, cod_draft, cod_answer, cot_draft, std_answer))

    comparison_df = pd.DataFrame(comparison_results, columns=['Question', 'CoD Draft', 'CoD Answer', 'CoT Draft', 'Standard Answer'])
    st.dataframe(comparison_df)

    st.subheader("Token Usage Comparison")
    token_usage = {
        'CoD': [len(d.split()) for d in comparison_df['CoD Draft']],
        'CoT': [50] * num_samples,  # Simulated token count for CoT
        'Standard': [10] * num_samples  # Simulated token count for Standard
    }
    token_df = pd.DataFrame(token_usage)
    st.line_chart(token_df)

    st.subheader("Download Results")
    st.download_button("Download Comparison Data", data=comparison_df.to_csv(), file_name="comparison_results.csv")

st.sidebar.info("Adjust parameters in the sidebar to see their effects on the application.")