import streamlit as st

from templates import display_folder_structure

from function import uml
from function import folder_structure_gen
from function import endpoint_gen
from function import user_feedback

import json
import os
import time
  
# create a language model that summarizes a meeting from transcripts and get the keypoints out of it

###### page config ###############################################################################################################################
st.set_page_config(
    page_title="yobo",
    page_icon="static/yobo_icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
)
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            body {margin-top: -20px;} /* Adjust this value as needed */
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


###### page header ###############################################################################################################################
st.markdown(
    """
    <h1 style='text-align: center;'>YOBO</h1>
    <h5 style='text-align: center;'>From UML Design to Repo Generation</h5>
    """,
    unsafe_allow_html=True
)

###### Body ###############################################################################################################################
ui_block, uml_block = st.columns([1, 1])

#### user inputs ########
with ui_block:
    st.subheader("Developer's idea")

    # developer's preference
    col1_lang, col2_lang = st.columns([3, 5])
    with col1_lang:
        st.write("")
        st.write('Preferred programming language?')
    with col2_lang:
        dev_pref_lang = st.selectbox('', ("No specific preference", "Python", "JavaScript", "Java", "Ruby", "C#", "Go", "PHP", "Swift", "TypeScript", "C++", "other"))
        if dev_pref_lang == "other":
            dev_pref_lang = st.text_input("")

    col1_ts, col2_ts = st.columns([3, 5])
    with col1_ts:
        st.write("")
        st.write("Preferred tech stack?")
    with col2_ts:
        dev_pref_ts = st.selectbox('', ("No specific preference",
                                                                    "MEAN (MongoDB, Express.js, Angular, Node.js)",
                                                                    "MERN (MongoDB, Express.js, React, Node.js)",
                                                                    "LAMP (Linux, Apache, MySQL, PHP/Python/Perl)",
                                                                    "Django (Python web framework with SQLite/PostgreSQL/MySQL)",
                                                                    "Ruby on Rails (Ruby web framework with SQLite/PostgreSQL/MySQL)",
                                                                    "ASP.NET (Microsoft's web framework with C# and SQL Server)",
                                                                    "Serverless (AWS Lambda, Azure Functions, Google Cloud Functions)",
                                                                    "JAMstack (JavaScript, APIs, Markup)",
                                                                    "PERN (PostgreSQL, Express.js, React, Node.js)",
                                                                    "Docker, Nginx, Flask, PostgreSQL (DNFP)",
                                                                    "Vue.js, Firebase, Firestore, Node.js (VFFN)",
                                                                    "MEVN (MongoDB, Express.js, Vue.js, Node.js)",
                                                                    "Laravel (PHP web framework with MySQL/PostgreSQL/SQLite)",
                                                                    "Spring Boot (Java web framework with Spring, Hibernate, and MySQL/PostgreSQL/Oracle)",
                                                                    "GraphQL, Apollo, React, Node.js (GARN)",
                                                                    "Flutter, Firebase, Cloud Firestore (FFCF)",
                                                                    "WordPress (PHP content management system with MySQL)",
                                                                    "Ionic, Angular, Firebase (IAF)",
                                                                    "Elastic Stack (Elasticsearch, Logstash, Kibana)",
                                                                    "Rust, Rocket (Rust web framework with PostgreSQL/MySQL)",
                                                                    "Phoenix (Elixir web framework with PostgreSQL/MySQL)",
                                                                    "Flask (Python micro web framework)",
                                                                    "Pyramid (Python web framework)",
                                                                    "FastAPI (Fast web framework for building APIs with Python)",
                                                                    "Dash (Python framework for building analytical web applications)",
                                                                    "Streamlit (Python library for building interactive web applications for data science)",
                                                                    "other"))
        if dev_pref_ts == "other":
            dev_pref_ts = st.text_input("")

    col1_db, col2_db = st.columns([3, 5])
    with col1_db:
        st.write("")
        st.write("Preferred database?")
    with col2_db:
        dev_pref_db = st.selectbox('', ("N/A", "MySQL", "MongoDB", "PostgreSQL", "SQLite", "Oracle", "Redis", "Cassandra", "Microsoft SQL Server",
                                                        "Amazon Aurora", "MariaDB", "Amazon DynamoDB", "Couchbase", "Firebase Realtime Database", "Google BigQuery", 
                                                        "InfluxDB", "Neo4j", "ArangoDB", "Apache HBase", "IBM Db2", "CouchDB", "No specific preference", "other"))
        if dev_pref_db == "other":
            dev_pref_db = st.text_input("")

    col1_integration, col2_integration = st.columns([3, 5])
    with col1_integration:
        st.write("")
        st.write("Add integration?")
    with col2_integration:
        dev_pref_integration = st.selectbox('', ("N/A","Stripe (Payment Gateway)", "PayPal (Payment Gateway)", "Braintree (Payment Gateway)",  "Google Maps API",
                                                        "Twitter API", "Facebook Graph API", "OAuth 2.0", "JSON Web Tokens (JWT)", "OpenID Connect", "Amazon Web Services (AWS)",
                                                        "Microsoft Azure", "Google Cloud Platform", "Salesforce API", "Twilio API", "Slack API", "Shopify API", "LinkedIn API",
                                                        "Mailchimp API", "Twitch API", "GitHub API", "more"))
        
        if dev_pref_integration == "more":
            dev_pref_integration = st.text_input("")


    dev_project_req = st.text_area("Tell me about your project"
                        , help = 'please include the description, key features, functionalities of your project'
                        , placeholder = 'create a language model that summarizes a meeting from transcripts and get the keypoints out of it ... '
                        , height = 300)
    
    text_len = len(dev_project_req.split())
    MAX_LEN = 50
    if text_len > MAX_LEN:
        st.warning(f"Exceeded character limit! maximum word is {MAX_LEN}.")
    else:
        pass
    
    submit_button = st.button("Submit")
    if submit_button and (text_len < MAX_LEN):
        with st.spinner(" (1/2) analyzing project requirements ..."):
            uml_dict = uml.generate_uml_code(dev_project_req, dev_pref_lang, dev_pref_ts, dev_pref_db, dev_pref_integration)
            st.session_state['uml_dict'] = uml_dict 
        with st.spinner(" (2/2) generating UML and Repo structure ..."):
            uml_dir_json = folder_structure_gen.folder_structure_gen(dev_project_req, uml_dict["uml_code"])
            st.session_state['uml_dir_json'] = uml_dir_json


with uml_block:
    st.subheader('UML Diagram')

    uml_dict = st.session_state.get('uml_dict', None) # retrieve uml_dict from session state
    if uml_dict is not None:
        st.write(uml_dict["comments"])
        st.image(image=uml_dict["url"]
                , width = 750)
        st.markdown(
            f'<a href="{uml_dict["url"]}" target="_blank"><input type="button" value="load uml"></a>',
            unsafe_allow_html=True
        )

    else:
        st.write("(example output) ... waiting for user description ...")
        st.image(image='static/uml_demo.png', width = 750)
    

# file structure 
st.subheader('Folder Structure')

uml_dict_session_state = st.session_state.get('uml_dir_json', None)
if uml_dict_session_state is not None:
    uml_dict_session_state = st.session_state.get('uml_dir_json', None)
    display_folder_structure.display_tree(uml_dict_session_state, ["root"])


    gen_pseudo_buttom = st.button("Approve folder structure and generate pseudo code")
    if gen_pseudo_buttom:
        with st.spinner("Generating pseudo code in repo ..."):
            pseudo_code_json = endpoint_gen.endpoint_generation(dev_project_req, uml_dict['uml_code'], uml_dict_session_state)
            st.session_state['pseudo_code_json'] = pseudo_code_json 
            msg_pseu_code = st.success("pseudo code successfully generated and imported ... ")
            time.sleep(2)
            msg_pseu_code.empty()
    
    pseudo_code_json = st.session_state.get('pseudo_code_json', None)


    if pseudo_code_json is not None:
        for i in range(len(pseudo_code_json["endpoints"])):
            # Only necessary for displaying directory.
            main_folder = pseudo_code_json["endpoints"][i]['file_path'].split('/')[0]
            if not uml_dict_session_state['root'].get(main_folder):
                uml_dict_session_state['root'][main_folder] = dict()
            file_name = pseudo_code_json["endpoints"][i]['file_path'].split('/')[1]
            code = pseudo_code_json["endpoints"][i]['contents']
            uml_dict_session_state['root'][main_folder][file_name] = code

        st.download_button(
            data=folder_structure_gen.download_repo(pseudo_code_json['endpoints']),
            label="Download Repository",
            file_name="generated_repo.zip",
            mime="application/zip",
            on_click=folder_structure_gen.download_repo,
            args=(pseudo_code_json['endpoints'],)
        )
        
    else:
        st.write("... start pseudo code generation ...")

else:
    st.write("(example output) ... waiting for user description ...")
    example_uml = """ 
        {"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}
                """
    data = json.loads('{"root": {"transcript_dataset": {"init.py": {}, "data_processing.py": {}, "tests": {"init.py": {}, "test_data_processing.py": {}}}, "language_model": {"init.py": {}, "model.py": {}, "preprocessing.py": {}, "tests": {"init.py": {}, "test_model.py": {}}}, "summarization_module": {"init.py": {}, "summarizer.py": {}, "tests": {"init.py": {}, "test_summarizer.py": {}}}, "key_point_extraction_module": {"init.py": {}, "extractor.py": {}, "tests": {"init.py": {}, "test_extractor.py": {}}}, "config": {"settings.py": {}}, "README.md": {}}}')
    display_folder_structure.display_tree(data, ["root"])

###### USER FEEDBACK FORM ###############################################################################################################################
with st.form(key='feedback_form'):
    feedback_str = st.text_input("We're better when we're hearing from you. Share your feedback, ask questions, or discuss opportunities. Let's connect and make great things happen!")
    submit_button = st.form_submit_button('Send')

    if submit_button:
        if feedback_str:
            try:
                user_feedback.submit_user_feedback(feedback_str)
                msg_user_feedback_success = st.success("Message sent successfully!")
                time.sleep(2)
                msg_user_feedback_success.empty()
            except Exception as e:
                msg_user_feedback_error = st.error(f"An error occurred: {str(e)}")
                time.sleep(2)
                msg_user_feedback_error.empty()
        else:
            st.error("Please provide some message before submitting!")