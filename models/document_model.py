import re
from transformers import BartTokenizer, BartForConditionalGeneration, pipeline
import pdfplumber
import docx

# Initialize BART tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
summarizer = pipeline('summarization', model=model, tokenizer=tokenizer)
question_answerer = pipeline("question-answering")

def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def extract_text_from_docx(file):
    text = ""
    try:
        doc = docx.Document(file)
        text = "\n".join([para.text for para in doc.paragraphs if para.text])
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
    return text

def remove_urls(text):
    """Remove URLs from the given text."""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(url_pattern, '', text)

def summarize_text(text, detail_level="brief"):
    try:
        max_input_length = 1024
        text_chunks = [text[i:i + max_input_length] for i in range(0, len(text), max_input_length)]
        
        summaries = []
        for chunk in text_chunks:
            if detail_level == "detailed":
                max_length = 1000
                min_length = 500
            else:  # brief
                max_length = 500
                min_length = 250

            summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        
        summary_text = " ".join(summaries)
        return remove_urls(summary_text)
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return "Error summarizing text."

def answer_question(context, question):
    try:
        # Improved context handling by breaking context into chunks
        context_chunks = [context[i:i + 512] for i in range(0, len(context), 512)]
        answers = []
        
        for chunk in context_chunks:
            result = question_answerer(question=question, context=chunk)
            answers.append((result['score'], result['answer']))
        
        # Select the best answer based on the highest score
        best_answer = max(answers, key=lambda x: x[0])[1]
        return best_answer
    except Exception as e:
        print(f"Error answering question: {e}")
        return "Error answering question."

