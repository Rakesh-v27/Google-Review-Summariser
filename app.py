import gradio as gr
import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
from scraper import scrape_reviews

load_dotenv()
client = OpenAI()

def generate_summary_stream(url):
    chat = [{"role": "user", "content": f"URL received:\n{url}"}]
    yield chat

    chat.append({"role": "assistant", "content": "Step 1: Scraping reviews from Google Maps..."})
    yield chat

    csv_path = scrape_reviews(url)
    if not csv_path or not os.path.exists(csv_path):
        chat.append({"role": "assistant", "content": "Failed to scrape reviews. Please check the URL."})
        yield chat
        return

    df = pd.read_csv(csv_path)
    if df.empty:
        chat.append({"role": "assistant", "content": "No reviews found."})
        yield chat
        return

    chat.append({"role": "assistant", "content": f"Collected {len(df)} reviews."})
    chat.append({"role": "assistant", "content": "Step 2: Sending reviews to GPT-4 for summarisation..."})
    yield chat

    reviews_text = "\n".join(df["Review"].dropna().astype(str).tolist())
    prompt = f"""
You are a helpful assistant. Summarise the following customer reviews of a business Analysis into as markdown file:
- Strengths
- Weaknesses
- Common themes
- Anything unusual or noteworthy

Here are the reviews:

{reviews_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        chat.append({"role": "assistant", "content": "Summary generated:"})
        chat.append({"role": "assistant", "content": summary})
        yield chat
    except Exception as e:
        chat.append({"role": "assistant", "content": f"OpenAI API Error: {e}"})
        yield chat


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## Google Reviews Summariser")
    gr.Markdown("Paste a Google Maps link and get a AI powered summary of what people are saying.")

    chatbot = gr.Chatbot(label="📣 ReviewBot", height=500, type="messages")
    url_input = gr.Textbox(label="Paste Google Maps URL", placeholder="https://www.google.com/maps/place/...")
    submit_button = gr.Button("Summarise")

    submit_button.click(
        fn=generate_summary_stream,
        inputs=url_input,
        outputs=chatbot
    )

if __name__ == "__main__":
    demo.launch()
