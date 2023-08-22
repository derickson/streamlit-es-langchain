import streamlit as st


from langchain_llama import Llama2LLM
from langchain import LLMChain, ConversationChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory


## Initialize chat history
if "memory_llama" not in st.session_state:
    st.session_state.memory_llama =  ConversationBufferWindowMemory(ai_prefix="Cher", k=5)

## Header with a clear memory button
col1, col2 = st.columns([3,1])
with col1:
    st.title('🦜🔗 talking to a 🦙')
with col2:
    if st.button("Clear Memory"):
        st.session_state.memory_llama.clear()

## Create conversational LLM Chain for Llama2
if "conversation_llama" not in st.session_state:
    llm = Llama2LLM()
    template = """<s>[INST] <<SYS>>
You are a helpful AI Chat assistant. Respond in markdown format without emojis. Answer concisely and don't make up answers. If you don't know the answer just say I don't know. 
<</SYS>>
Chat History: {history}

{input} [/INST] """
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
    st.session_state.conversation_llama = ConversationChain(
        prompt=PROMPT,
        llm=llm,
        verbose=True,
        memory=st.session_state.memory_llama,
    )
    

## When a new human chat is received
def chatExchange(humanInput):
    return st.session_state.conversation_llama.run(humanInput)

## The Chat input at the bottom of the screen
if prompt := st.chat_input("What is up?"):
    chatExchange(prompt)
    
# Display chat messages from history on app rerun
for message in st.session_state.memory_llama.buffer_as_messages:
    with st.chat_message("user" if message.type == 'human' else 'assistant' ):
        st.markdown(message.content)
    