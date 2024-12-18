# News-Research-Tool
This Gen AI tool allows users to conduct research by extracting content from news articles, processing the extracted information, and generating detailed, context-based responses to queries using Groq's powerful language model.


## Features

- **News Scraping**: Extracts text content from news articles via provided URLs.
- **Context Search**: Uses FAISS (Facebook AI Similarity Search) to find the most relevant context for a given research query.
- **Groq API Integration**: Utilizes Groq's Llama 3.1 model to generate detailed and structured answers based on the extracted content.
- **Easy Interface**: Powered by Streamlit for a user-friendly interface.

## Requirements

Before using this tool, ensure you have the following libraries installed:

- **Streamlit**: For the user interface.
- **Groq Python SDK**: For interfacing with the Groq API.
- **BeautifulSoup**: For web scraping.
- **faiss-cpu**: For efficient similarity search of document embeddings.
- **Sentence-Transformers**: For generating sentence embeddings.

### Install dependencies:

```bash
pip install streamlit
pip install groq
pip install beautifulsoup4
pip install faiss-cpu
pip install sentence-transformers
```

## Setup

### 1. **Groq API Key**
To use this tool, you'll need an API key from Groq. You can obtain it by signing up for an account at [Groq](https://www.groq.com/).

### 2. **Run the Application**

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/groq-news-research-tool.git
```

2. Navigate to the project directory:

```bash
cd groq-news-research-tool
```

3. Run the Streamlit application:

```bash
streamlit run app.py
```

This will launch a Streamlit app in your web browser.

### 3. **Using the Tool**
1. **Enter your Groq API Key**: Go to the sidebar and input your Groq API key.
2. **Provide News Article URLs**: Input up to 3 URLs of news articles you want to research.
3. **Enter a Research Question**: Type your question based on the content you want to research.
4. **Click "Conduct Research"**: The app will scrape the URLs, extract the content, search for the most relevant context, and use Groq's model to generate an informative answer to your query.

---

## Code Explanation

### 1. **NewsResearchTool Class**
The core of the application is the `NewsResearchTool` class, which handles:
- **Model loading** (`load_model`): Connects to Groq using the provided API key.
- **Web scraping** (`scrape_url`, `process_urls`): Extracts article text from provided URLs.
- **Context search** (`find_relevant_context`): Uses FAISS to find the most relevant document from the scraped articles.
- **Response generation** (`generate_response`): Uses Groq's Llama 3.1 model to generate a response based on the most relevant context.

### 2. **Main Streamlit Interface**
The interface is built with Streamlit:
- Sidebar for input configuration (API key, URLs, etc.)
- A button to initiate the research process
- Displays the research results and the most relevant article URL.

---

## Example Usage

1. Open the app in your browser by running the Streamlit server.
2. In the sidebar, input your **Groq API Key**.
3. Enter URLs of up to three news articles you'd like to research.
4. Type a specific question in the text input and press **"Conduct Research"**.
5. The app will show the answer based on the most relevant article and its source.

---

## Troubleshooting

### Error: "Groq API connection error"
- Ensure that the API key you entered is correct.
- Check your internet connection and retry.

### Error: "No relevant context found"
- This could happen if the scraped article content does not contain relevant information to answer the query. Try using different URLs.

### Error: "Groq client not initialized"
- Ensure that the API key is entered and Groq is connected before conducting research.

## Links used - 
I have used this 3 links to test the News Research Tool-
- https://www.moneycontrol.com/news/business/tata-motors-mahindra-gain-certificates-for-production-linked-payouts-11281691.html
- https://www.moneycontrol.com/news/business/tata-motors-launches-punch-icng-price-starts-at-rs-7-1-lakh-11098751.html
- https://www.moneycontrol.com/news/business/stocks/buy-tata-motors-target-of-rs-743-kr-choksey-11080811.html

---

## Contributing

If you want to contribute to this project, feel free to fork this repository, make your changes, and submit a pull request. Contributions, bug reports, and feature requests are always welcome!

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- **Groq** for providing powerful language models.
- **Sentence-Transformers** and **FAISS** for efficient document similarity search.
- **Streamlit** for creating the user interface.
- **BeautifulSoup** for web scraping.

---

### Screenshots

![image](https://github.com/user-attachments/assets/e9985fc9-3bd9-486c-a4c6-eb2e5d9e410b)
![image](https://github.com/user-attachments/assets/b45d48eb-0c4b-4ed9-9f44-8e77fa5841c3)



