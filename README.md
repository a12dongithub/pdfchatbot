# pdfchatbot
PDF Reader Chat Bot

# Features
PDF Upload
PDF Text Extractor
Previous Conversation Also Taken in consideration when giving an output
For very large PDFs with text size > 4000, embedding matching used. Doc2Vec embeddings are used to find out embedding vectors and top 10 paragraphs ( each paragraph contains 10 sentences ) with highest cosine similarity with the query are fed in as external information from the PDF to the LLM model.
# How to run
Please Install the following Dependencies

Django
openai
gensim
nltk
pypdf2
scikit-learn
transformers
torch

Run 
python manage.py runserver 
in terminal after going in directory
Wait after uploading
Also wait after first message
When running first time it takes extra extra long due to some extra dependencies that are downloaded on runtime

# Screen Shots
https://prnt.sc/UWF34MaYMLey
https://prnt.sc/B324lJvqii0I

#Future Works
Use better models : 
  doc2vec ( slightly trained ) -> to use pre-trained embeddings such as bert or gpt. ( Could not use a pre trained model as laptop couldn't handle and bert took too long to give output)
  gpt3 -> gpt4

Frontend Improvements : 
  Better UI
  Loading When waiting for response
  Cannot chat while waiting for response
  PDF Showing while chatting


  
