import numpy as np
from flask import Flask, request, jsonify, render_template

# Transformer Imports
from transformers import AutoTokenizer
import pickle

# 
app = Flask(__name__)
model = pickle.load(open('mai_model.pkl', 'rb'))
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")

@app.route('/reply', methods=['POST'])
def reply():
    
    data = request.get_json(force=True) 
    new_user_input_ids = tokenizer.encode(data["data"] + tokenizer.eos_token, return_tensors='pt')

    bot_input_ids = new_user_input_ids

    chat_history_ids = model.generate(
        bot_input_ids, max_length=200,
        pad_token_id=tokenizer.eos_token_id,  
        no_repeat_ngram_size=3,       
        do_sample=True, 
        top_k=100, 
        top_p=0.7,
        temperature = 0.8
    )

    x = "{}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))

    return jsonify(x)

if __name__ == "__main__":
    app.run(debug=True)