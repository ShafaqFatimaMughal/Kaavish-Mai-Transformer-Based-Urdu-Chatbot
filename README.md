# Mai: A Transformer-based Roman Urdu and English Chatbot for Menstrual Health and Hygiene

Mai is a final year project by Habib University students Shafaq Fatima Mughal, Shayan Aamir, Ayesha Syed, and Umema Zehra. The project aims to provide a solution for menstrual health and hygiene related issues by creating a transformer-based chatbot that can understand both Roman Urdu and English languages.

The chatbot is trained on various datasets from different sources such as Hello Clue, Flo, Always, Kaggle, Reddit, and locally collected data from stakeholders and doctors that were concatenated into `Datasets/Self-Curated/English/self-curated.csv`. The primary transformer model used for this project is DialoGPT small from Hugging Face.
- English Dataset Link: https://www.kaggle.com/datasets/shafaqfatimamughal/english-menstrual-health-and-hygiene-chatbot  

The English dataset was then trasliterated to Roman Urdu `Datasets/Self-Curated/Urdu/self-curated.csv` using Google Translate and iJunoon. But the DialoGPT small was pre-trained on some general conversation datasets in Roman Urdu from Kaggle `Datasets/General-Conversation/general-conversation-roman-urdu.csv`.  
- Roman Urdu Dataset Link: https://www.kaggle.com/datasets/shafaqfatimamughal/roman-urdu-menstrual-health-and-hygiene-chatbot

The chatbot is trained and downloaded as a pickle file, and an API is created to get a reply from the fine-tuned model. The API is deployed on GCP (Google Cloud Platform), and the deployed model is consumed via a Flutter app.
- Link: https://github.com/ShafaqFatimaMughal/Kaavish-Mai-Chatbot-Deployment 

The Flutter app stores user data in a Firebase database, providing an easy-to-use and secure solution for users to interact with the chatbot. 
- Link: https://github.com/ayesha-syed/mai_chatbot 
