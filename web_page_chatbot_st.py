"""
Purpose:
    Web_Page Chatbot
"""

# Python imports
import os

# 3rd party imports
import streamlit as st
import ai_utils
import openai

from ingest import embedding

openai.api_key = os.environ["OPENAI_API_KEY"]


def message_func(text, is_user=False):
    """
    This function is used to display the messages in the chatbot UI.

    Parameters:
    text (str): The text to be displayed.
    is_user (bool): Whether the message is from the user or the chatbot.
    key (str): The key to be used for the message.
    avatar_style (str): The style of the avatar to be used.
    """
    if is_user:
        avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairSides&accessoriesType=Blank&hairColor=BrownDark&facialHairType=BeardMedium&facialHairColor=BrownDark&clotheType=BlazerSweater&eyeType=Default&eyebrowType=FlatNatural&mouthType=Default&skinColor=Black"
        message_alignment = "flex-end"
        message_bg_color = "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)"
        avatar_class = "user-avatar"
        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%;">
                        {text}
                    </div>
                            <img src="{avatar_url}" class="{avatar_class}" alt="avatar" height="50px" />

                </div>
                """,
            unsafe_allow_html=True,
        )
    else:
        avatar_url = "https://avataaars.io/?avatarStyle=Transparent&topType=LongHairBigHair&accessoriesType=Prescription01&hairColor=Platinum&facialHairType=Blank&clotheType=GraphicShirt&clotheColor=Red&graphicType=Bear&eyeType=Default&eyebrowType=RaisedExcited&mouthType=Smile&skinColor=Brown'"
        message_alignment = "flex-start"
        message_bg_color = "#71797E"
        avatar_class = "bot-avatar"
        st.write(
            f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px; justify-content: {message_alignment};">
                    <img src="{avatar_url}" class="{avatar_class}" alt="avatar" height="50px" />
                    <div style="background: {message_bg_color}; color: white; border-radius: 20px; padding: 10px; margin-right: 5px; max-width: 75%;">
                        {text} \n </div>
                </div>
                """,
            unsafe_allow_html=True,
        )


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "docs" not in st.session_state:
    st.session_state["docs"] = []

st.set_page_config(
    page_title="Web_Page Chatbot",
    page_icon="Chatbot",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        "Report a bug": "https://github.com/luanluandehaobaoman/webpage_chatbot",
        "About": """The purpose of this chatbot is to provide users with answers and resources related to the given web page.
            """,
    },
)


@st.cache_resource
def load_chain():
    """
    Load the chain from the local file system

    Returns:
        chain (Chain): The chain object

    """
    return ai_utils.setup_chain()



def sidebar() -> None:
    """
    Purpose:
        Shows the side bar
    Args:
        N/A
    Returns:
        N/A
    """

    st.sidebar.image(
        "https://cdn.technologyadvice.com/wp-content/uploads/2018/02/friendly-chatbot-700x408.jpg",
        use_column_width=True,
    )

    st.sidebar.markdown(
        "Web Page Chatbot，powered by ChatGPT."
    )


def app() -> None:
    """
    Purpose:
        Controls the app flow
    Args:
        N/A
    Returns:
        N/A
    """

    # Spin up the sidebar
    sidebar()
    # Get the sitemap URLs from the user

    sitemap_url_list = st.text_area("Enter the sitemap URLs (comma-separated):").split(',')

    # Button to start the embedding process
    start_button = st.button("Start Embedding")

    if start_button and sitemap_url_list[0]:  # Check if the user has entered any URLs and clicked the button
        # Load the content and create embeddings
        st.write(sitemap_url_list)
        embedding(sitemap_url_list)
        # embedding("https://zh.wikipedia.org/wiki/2023%E5%B9%B4%E4%B8%96%E7%95%8C%E4%B8%80%E7%BA%A7%E6%96%B9%E7%A8%8B%E5%BC%8F%E9%94%A6%E6%A0%87%E8%B5%9B")
    #
    # # Check if the embeddings exist
    if os.path.exists("local_index"):
    #     # Load the chain with the created embeddings
        chain = load_chain()

    with st.container():
        # Load chat history
        for index, chat in enumerate(st.session_state["chat_history"]):
            message_func(chat[0], True)
            message_func(chat[1], False)

            with st.expander("Resources"):
                for doc in st.session_state["docs"][index]:
                    st.write(doc.metadata["source"])
                    st.write(doc.page_content)

        with st.form(key="my_form", clear_on_submit=True):
            query = st.text_input(
                "Query: ",
                key="input",
                value="",
                placeholder="Type your query here...",
                label_visibility="hidden",
            )
            submit_button = st.form_submit_button(label="Submit")
        col1, col2 = st.columns([1, 3.2])
        reset_button = col1.button("Reset Chat History")

    if submit_button:
        with st.spinner("Generating..."):
            result = chain(
                {"question": query, "chat_history": st.session_state["chat_history"]}
            )
            st.session_state["chat_history"].append(
                (result["question"], result["answer"])
            )
            st.session_state["docs"].append(result["source_documents"])
            st.experimental_rerun()  # Add Chat to UI

    if reset_button:
        st.session_state["chat_history"] = []
        st.session_state["docs"] = []
        st.experimental_rerun()


def main() -> None:
    """
    Purpose:
        Controls the flow of the streamlit app
    Args:
        N/A
    Returns:
        N/A
    """




    # Start the streamlit app
    st.title("Web Page Chatbot")
    st.subheader("Paste url and start chatting")

    app()


if __name__ == "__main__":
    main()
