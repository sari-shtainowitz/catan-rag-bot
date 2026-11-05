import truststore
truststore.inject_into_ssl()

from design import CSS, HEADER
import gradio as gr
import os
import chromadb
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, Document, VectorStoreIndex, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.google_genai import GoogleGenAI

# טעינת המפתח מהקובץ .env
load_dotenv()

# 1. טעינת כל הקבצים מהתיקייה data
documents = SimpleDirectoryReader("data").load_data()
print("מספר קבצים שנטענו:", len(documents))

# 2. חלוקה לקטעים לפי נושאים (בכל שורה ריקה)
chunks = []
for doc in documents:
    sections = doc.text.split("\n\n")
    for section in sections:
        section = section.strip()
        if "\n" in section:
            chunks.append(Document(text=section, metadata=doc.metadata))
print("מספר קטעים:", len(chunks))

# 3. טעינת מודל הווקטורים
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# 4. חיבור ל-ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="catan_rules",
    metadata={"hnsw:space": "cosine"},
)
vector_store = ChromaVectorStore(chroma_collection=collection)

# 5. שמירת הקטעים (רק אם ה-DB עדיין ריק)
if collection.count() == 0:
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex(chunks, storage_context=storage_context, embed_model=embed_model)
    print("הקטעים נשמרו ב-ChromaDB")
else:
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
    print("ה-DB כבר מלא, טוענים ממנו")

# 6. חיבור למודל התשובות (Gemini)
llm = GoogleGenAI(
    model="gemini-flash-lite-latest",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

SYSTEM_PROMPT = (
    "את עוזרת שעונה על שאלות לגבי חוקי המשחק קטאן. "
    "עני רק על סמך קטעי החוקים שקיבלת. "
    "אם התשובה לא מופיעה בהם, אמרי שאינך יודעת. "
    "עני בעברית, בקצרה ובבהירות."
)

chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    llm=llm,
    similarity_top_k=3,
    system_prompt=SYSTEM_PROMPT,
    verbose=True,
)

# 7. ממשק צ'אט בדפדפן
def respond(message, history):
    response = chat_engine.chat(message)
    return str(response)

with gr.Blocks() as demo:
    gr.HTML(HEADER)
    gr.ChatInterface(
        fn=respond,
        chatbot=gr.Chatbot(rtl=True, height="70vh", show_label=False, elem_classes="catan-chat"),
        textbox=gr.Textbox(rtl=True, placeholder="כתבי הודעה...", elem_classes="catan-input"),
    )

demo.launch(css=CSS)



