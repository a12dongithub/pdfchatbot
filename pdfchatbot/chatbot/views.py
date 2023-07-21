from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from .models import Chat
from PyPDF2 import PdfReader
from django.utils import timezone
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('punkt')
openai_api_key = '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'
openai.api_key = openai_api_key

s = "" # string that contains all the pdf data
listOfMessages = [] #contains all the past history of chatting

def ask_openai(message): #Asking from ChatGPT
    print(len((embedding_match(message))))
    listOfMessages.append({"role" : "user", "content" : message})
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages=
            [{"role": "system", "content": "You are an helpful assistant. Answer the questions using your knowledge base and following information {}. If you do not know the answer to a question, you truthfully say I do not know.".format(embedding_match(message))}] +
            listOfMessages
        
    )
    answer = response.choices[0].message.content.strip()
    listOfMessages.append({"role" : "assistant", "content" : answer})
    return answer

def group_sentences(sentences, n):
    """Group sentences into paragraphs of n sentences each."""
    return [' '.join(sentences[i:i+n]) for i in range(0, len(sentences), n)]

def embedding_match(query): #Finding the top 10 paragraphs to be sent into the input since the input can be too large
    # For short PDFs we can just retrieve the file itself
    if(len(s) < 4000):
        return s
    
    top_n = 10
    # Split the text data into sentences
    sentences = sent_tokenize(s)

    # Group the sentences into paragraphs of 20 sentences each
    paragraphs = group_sentences(sentences, 20)

    # Prepare training data in the format required by Doc2Vec
    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(paragraphs)]

    # Train a Doc2Vec model
    model = Doc2Vec(documents, vector_size=50, window=2, min_count=1, workers=4)

    # Calculate a vector for the query
    query_vector = model.infer_vector(word_tokenize(query))

    # Compute the cosine similarity between the query vector and the vectors of all paragraphs
    similarities = []
    for i, paragraph in enumerate(paragraphs):
        paragraph_vector = model.docvecs[i]
        similarity = cosine_similarity([query_vector], [paragraph_vector])[0][0]
        similarities.append((similarity, paragraph))

    # Sort the paragraphs by their similarity to the query
    similarities.sort(key=lambda x: x[0], reverse=True)

    # Return the top n paragraphs
    return [paragraph for similarity, paragraph in similarities[:top_n]]

def chatbot(request):
    # Chat bot function that conntects to the frontend
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        chat = Chat( message=message, response=response, created_at=timezone.now())
        return JsonResponse({'response': response})
    return render(request, 'chatbot.html', {'chats': "HEY"})

def upload(request):
    # Upload function that is used to upload
    global s
    if request.method == 'POST':
        file = request.FILES['pdf-upload']
        reader = PdfReader(file)
        for pg in reader.pages:
            text = pg.extract_text() 
            s += text
        return JsonResponse({'message': 'File uploaded successfully', 'filename': file.name, 'filesize': file.size})
    else:
        return render(request,'upload.html')