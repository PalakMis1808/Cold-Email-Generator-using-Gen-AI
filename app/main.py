import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Custom CSS for styling
def add_custom_css():
    st.markdown("""
        <style>
        /* Custom styles for background, buttons, and more */
        body {
            background-color: #f0f2f6;
        }
        .stMarkdown h1 {
            font-family: 'Arial', sans-serif;
            color: #2b6cb0;
        }
        h2, h3, h4 {
            font-family: 'Arial', sans-serif;
            color: #2c5282;
        }
        input {
            border: 2px solid #2c5282 !important;
            background-color: #ffffff !important;
            color: #2b6cb0 !important;
        }
        .stButton button {
            background-color: #2b6cb0;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
        .stButton button:hover {
            background-color: #2c5282;
        }
        .stCode {
            background-color: #f9f9f9 !important;
            border-radius: 10px !important;
            font-family: 'Courier New', monospace;
        }
        .stExpander {
            background-color: #e2e8f0;
            border: 2px solid #2b6cb0 !important;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

def create_streamlit_app(llm, portfolio, clean_text):
    # Adding custom CSS
    add_custom_css()

    # App title and description
    st.title("📧 Cold Mail Generator")
    st.write("Generate personalized cold emails by analyzing job listings from a given URL.")

    # Input section
    with st.form(key="url_form"):
        url_input = st.text_input("Enter a Job Listing URL:", value="", placeholder="https://example.com/job-link")
        submit_button = st.form_submit_button(label="Generate Email")

    # Result section with URL validation
    if submit_button:
        if not url_input.strip():
            st.warning("⚠️ Please enter a valid URL before submitting.")
        else:
            with st.spinner("Generating your email..."):
                try:
                    # Load and process data
                    loader = WebBaseLoader([url_input])
                    data = clean_text(loader.load().pop().page_content)
                    
                    # Load portfolio and extract jobs
                    portfolio.load_portfolio()
                    jobs = llm.extract_jobs(data)

                    if not jobs:
                        st.warning("No job information could be extracted from the provided URL. Please check the URL or try a different one.")
                    else:
                        # Loop through the extracted jobs and generate emails
                        for job in jobs:
            
                            
                            # Extract skills for the job
                            skills = job.get('skills', [])
                            skill_list = ', '.join(skills) if skills else "Not specified"
                            
                            # Display job information simultaneously with email
                            st.markdown(f"**Skills Required:** {skill_list}")

                            # Generate email
                            links = portfolio.query_links(skills)
                            email = llm.write_mail(job, links)

                            # Display the generated email immediately
                            st.markdown("### Generated Email:")
                            st.code(email, language='markdown')

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
