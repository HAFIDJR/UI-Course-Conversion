import re
import string
import nltk 
from nltk.tokenize import word_tokenize  # Tokenisasi teks
from nltk.corpus import stopwords
nltk.download('punkt_tab')
 # Import pustaka NLTK (Natural Language Toolkit).
nltk.download('punkt')  # Mengunduh dataset yang diperlukan untuk tokenisasi teks.
nltk.download('stopwords')



def cleaningText(text):
    text = re.sub(r"@[A-Za-z0-9]+", "", text)  # menghapus mention
    text = re.sub(r"#[A-Za-z0-9]+", "", text)  # menghapus hashtag
    text = re.sub(r"RT[\s]", "", text)  # menghapus RT
    text = re.sub(r"http\S+", "", text)  # menghapus link
    text = re.sub(r"[0-9]+", "", text)  # menghapus angka
    text = re.sub(r"[^\w\s]", " ", text)  # menghapus karakter selain huruf dan angka

    text = text.replace("\n", " ")  # mengganti baris baru dengan spasi
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )  # menghapus semua tanda baca
    text = text.strip(" ")  # menghapus karakter spasi dari kiri dan kanan teks
    return text


def casefoldingText(text):
    text = text.lower()
    return text


def tokenizingText(text):
    text = word_tokenize(text)
    return text


def filteringText(text):
    listStopwords = set(stopwords.words("indonesian"))
    listStopwords1 = set(stopwords.words("english"))
    listStopwords.update(listStopwords1)
    listStopwords.update(
        [
            "apa",
            "siapa",
            "mengapa",
            "bagaimana",
            "kapan",
            "dimana",
            "di mana",
            "berapa",
            "mampu",
            "dapat",
            "menjelaskan",
            "memahami",
            "mengerti",
            "mengetahui",
            "mengenal",
            "menguasai",
            "menyebutkan",
            "menjabarkan",
            "pengantar",
            "dasar",
            "tujuan",
            "materi",
            "pembelajaran",
            "pokok",
            "konsep",
            "mahasiswa",
            "diharapkan",
        ]
    )
    filtered = []
    for txt in text:
        if txt not in listStopwords:
            filtered.append(txt)
    text = filtered
    return text

def toSentence(list_words): # Mengubah daftar kata menjadi kalimat
    sentence = ' '.join(word for word in list_words)
    return sentence

def cleanText(text):
    if not text or not isinstance(text, str):
        return ""  # Handle input kosong/None

    # Step 1: Cleaning
    cleaned_text = cleaningText(text)

    # Step 2: Case Folding
    casefolded_text = casefoldingText(cleaned_text)

    # Step 3: Tokenizing
    tokens = tokenizingText(casefolded_text)

    # Step 4: Filtering (stopword removal, etc.)
    filtered_tokens = filteringText(tokens)
    text_clean = toSentence(filtered_tokens)

    # Step 5: Reconstruct to sentence (if needed)
    return text_clean
