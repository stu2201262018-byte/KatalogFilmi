from flask import Flask, jsonify
app = Flask(__name__)

movies = [
    {"id": 1, "title": "The Matrix", "year": 1999, "rating": 8.7},
    {"id": 2, "title": "Inception", "year": 2010, "rating": 8.8},
    {"id": 3, "title": "Interstellar", "year": 2014, "rating": 8.6}
]

@app.route("/api/movies")
def get_movies():
    return jsonify(movies)

if __name__ == "__main__":
    app.run(debug=True)
app.run(host="127.0.0.1", port=5000, debug=True)

