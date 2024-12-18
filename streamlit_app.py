import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Corenet-X Chatbot..🎈")
st.write("Simple Chatbot that deals with Conet-X Queries. ")
st.write("Developed by: Unni(BCA)")
st.write("Type a keyword related to buildings.")
st.write("Examples: What's new?, Green Mark, What's in 2025 etc.")

context = """
            [Building and Construction Authority (BCA), Singapore Building Regulations, and CORENET-X Submission Requirements]
            [The Building and Construction Authority leads the CORENET-X project in collaboration with other agencies and industry leaders in the building sector.]
            [Other Government Agencies that support the CORENET-X project are URA, LTA, NEA, NParks, PUB, SCDF, and SLA.]
            [Under the new Regulatory Approval process for Building Works (RABW), the conventional 20+ approval touchpoints are streamlined into 3 key sequential submission gateways, providing a more efficient process for project teams.]
            CORENET-X Overview:
            CORENET-X is a multi-agency digital platform developed by BCA and URA, supported by GovTech. It allows Qualified Persons 
            (QPs) to submit coordinated BIM models for regulatory approval, streamlining the approval process to three gateways: Design, 
            Construction, and Completion. CORENET-X aims to minimize conflicts, delays, and redundant works in the construction industry.
            
            New Regulatory Approval Process:
            The Regulatory Approval process for Building Works (RABW) replaces the conventional 20+ approval touchpoints with three 
            sequential submission gateways, enhancing coordination and efficiency in project approvals. This process facilitates joint 
            submissions from QPs, aligned with multiple agencies’ statutory requirements.
            
            CORENET-X User Journey:
            Project teams collaborate on a common data environment, enabling real-time design review, conflict detection, and resolution 
            before construction. The streamlined approval gateways promote a more integrated approach to project submissions.
            
            BIM Data and Compliance:
            CORENET-X supports BIM submissions and mandates IFC-SG standards, assisting in compliance documentation. Non-BIM 
            supplementary documents can also accompany submissions, providing flexibility for diverse project requirements.
            
            Agile Development and Phased Onboarding:
            CORENET-X is being implemented in phases, with mandatory submissions starting from April 1, 2025, for new projects. The 
            system will integrate further updates progressively, reflecting its agile development approach.
        """
# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.text_input("OpenAI API Key", type="password")

openai_api_key = st.secrets["openai"]["secret_key"]
client = OpenAI(api_key=openai_api_key)

if not client:
    st.info("API Key is missing.", icon="🗝️")
else:

    # OpenAI client already exists
    # client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": context+prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
