from agents.principal_agent import handle_user_query

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    bot_response = handle_user_query(user_msg)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
