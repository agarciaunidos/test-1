import streamlit as st
import boto3
import json

# Initialize the Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name=st.secrets["REGION"],
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
)

# Streamlit app
st.title("AI Chat App with AWS Bedrock")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call Bedrock API
    try:
        response = bedrock.invoke_model(
            modelId='anthropic.claude-v2',  # Replace with your preferred model
            body=json.dumps({
                "prompt": f"Human: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 300,
                "temperature": 0.7,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"]
            })
        )
        
        response_body = json.loads(response['body'].read())
        ai_response = response_body['completion']

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add a sidebar with instructions
st.sidebar.title("Instructions")
st.sidebar.write("""
1. Enter your AWS credentials as environment variables or in your AWS config file.
2. Make sure you have the necessary permissions to use Amazon Bedrock.
3. Adjust the `region_name` and `modelId` if needed.
4. Deploy this app to Streamlit Cloud.
5. Start chatting with the AI!
""")
