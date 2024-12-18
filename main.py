import os
import streamlit as st
from groq import Groq
from urllib.request import urlopen
from bs4 import BeautifulSoup
import traceback
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


class NewsResearchTool:
    def __init__(self):
        self.client = None
        # Use a lightweight, fast embedding model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

        # Embedding dimension (depends on the model)
        self.embedding_dim = 384

    def load_model(self, api_key):
        try:
            if not api_key:
                st.error("No API key provided")
                return False

            # Explicitly set the environment variable
            os.environ['GROQ_API_KEY'] = api_key

            # Initialize Groq client with the API key
            self.client = Groq(api_key=api_key)

            # Test the client by listing models
            models = self.client.models.list()
            st.success(f"Connected to Groq. Available models: {[model.id for model in models.data]}")

            return True
        except Exception as e:
            st.error(f"Groq API connection error: {str(e)}")
            st.error(traceback.format_exc())  # Print full traceback for detailed error info
            return False

    def scrape_url(self, url):
        try:
            page = urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            text = ' '.join([p.get_text() for p in soup.find_all('p')])
            return text
        except Exception as e:
            st.error(f"URL scraping error for {url}: {str(e)}")
            return ""

    def process_urls(self, urls):
        documents = [self.scrape_url(url) for url in urls if url]
        return [doc for doc in documents if doc]

    def find_relevant_context(self, documents, query):
        if not documents:
            return None, None

        try:
            # Create Faiss index
            index = faiss.IndexFlatL2(self.embedding_dim)

            # Embed documents
            doc_embeddings = []
            for doc in documents:
                embedding = self.embedder.encode(doc)
                doc_embeddings.append(embedding)

            # Convert to numpy array
            doc_embeddings_np = np.array(doc_embeddings).astype('float32')

            # Add embeddings to index
            index.add(doc_embeddings_np)

            # Embed query
            query_embedding = self.embedder.encode(query).astype('float32').reshape(1, -1)

            # Search for most similar document
            D, I = index.search(query_embedding, 1)

            # Get the index of the most relevant document
            most_relevant_index = I[0][0]

            return documents[most_relevant_index], most_relevant_index

        except Exception as e:
            st.error(f"Error finding relevant context: {e}")
            return documents[0] if documents else None, 0

    def generate_response(self, context, query):
        # Add more detailed error checking
        if not self.client:
            st.error("Groq client is not initialized. Please load the model first.")
            return "Groq client not initialized. Please load the model first."

        try:
            prompt = f"""
            Context: {context}

            Question: {query}

            Using the provided context, generate a comprehensive and detailed answer to the question. 
            Ensure your response is:
            - Directly based on the given context
            - Thorough and informative
            - Clearly structured

            Answer:
            """

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful research assistant that provides detailed answers based on given context."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama3-70b-8192",
                temperature=0.7,
                max_tokens=500,
                top_p=0.9
            )

            return chat_completion.choices[0].message.content.strip()

        except Exception as e:
            st.error(f"Error generating response: {e}")
            st.error(traceback.format_exc())  # Print full traceback
            return f"Error generating response: {str(e)}"


def main():
    st.set_page_config(page_title="Groq News Research Tool", page_icon="📰")
    st.title("🔍 Groq Llama 3.1 News Research Tool")

    # Initialize the tool before using
    tool = NewsResearchTool()

    st.sidebar.header("🔑 Groq API Configuration")
    api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

    st.sidebar.header("🌐 News Sources")
    urls = []
    for i in range(3):
        url = st.sidebar.text_input(f"News Article URL {i + 1}", key=f"url_{i}")
        if url:
            urls.append(url)

    # Modify the connection button to pass API key
    if st.sidebar.button("🚀 Connect to Groq"):
        with st.spinner("Connecting to Groq..."):
            # Pass the API key to load_model
            if tool.load_model(api_key):
                st.sidebar.success("Connected to Groq Successfully! 🎉")
            else:
                st.sidebar.error("Connection Failed. Check your API Key.")

    query = st.text_input("📝 Enter your research question")

    if st.button("🔬 Conduct Research"):
        # Validate inputs with more detailed checks
        if not api_key:
            st.warning("Please enter your Groq API Key")
            return

        if not urls:
            st.warning("Please enter at least one URL")
            return

        if not query:
            st.warning("Please enter a research question")
            return

        # Ensure model is loaded before research
        if not tool.client:
            # Try to load the model
            if not tool.load_model(api_key):
                st.error("Failed to initialize Groq client. Please check your API key.")
                return

        with st.spinner("Researching... (This might take a moment)"):
            documents = tool.process_urls(urls)

            if not documents:
                st.error("Could not extract content from the provided URLs")
                return

            # Find the most relevant context and its index
            relevant_context, relevant_index = tool.find_relevant_context(documents, query)

            if not relevant_context:
                st.error("No relevant context found")
                return

            response = tool.generate_response(relevant_context, query)

            st.header("🧠 Research Findings")
            st.write(response)

            st.subheader("📌 Source:")
            # Show only the most relevant source URL
            st.write(urls[relevant_index])


if __name__ == "__main__":
    main()