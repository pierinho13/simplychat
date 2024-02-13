from flask import Flask, render_template, request, jsonify 
from openai import OpenAI

client = OpenAI(api_key='token') 

app = Flask(__name__, template_folder='templates')


# Conversation history
conversation_history = []

def format_message(message):
    return message.replace("\n", "<br>")

# OpenAI API Key 
def get_completion(prompt): 
	print(prompt) 

	conversation_history.append({"role": "user", "content": prompt})

	query = client.chat.completions.create(model="gpt-3.5-turbo-0125", 
	messages=conversation_history,
	max_tokens=1024, 
	n=1, 
	stop=None, 
	temperature=0.5) 

	conversation_history.append({"role": "assistant", "content": query.choices[0].message.content})
	print(query.choices[0].message) 
	response = query.choices[0].message.content 
	return format_message(response) 

@app.route("/", methods=['POST', 'GET']) 
def query_view(): 
	if request.method == 'POST': 
		print('step1') 
		prompt = request.form['prompt'] 
		response = get_completion(prompt) 
		print(response) 

		return jsonify({'response': response}) 
	return render_template('index.html') 


if __name__ == "__main__": 
	app.run(debug=True) 
