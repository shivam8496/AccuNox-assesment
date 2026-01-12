from flask import Flask, jsonify

app = Flask(__name__)

# Sample Data: List of 15 books
books = [
    {
        "id": 1, 
        "title": "The Great Gatsby", 
        "author": ["F. Scott Fitzgerald"], 
        "publication_year": 1925
    },
    {
        "id": 2, 
        "title": "To Kill a Mockingbird", 
        "author": ["Harper Lee"], 
        "publication_year": 1960
    },
    {
        "id": 3, 
        "title": "1984", 
        "author": ["George Orwell"], 
        "publication_year": 1949
    },
    {
        "id": 4, 
        "title": "Pride and Prejudice", 
        "author": ["Jane Austen"], 
        "publication_year": 1813
    },
    {
        "id": 5, 
        "title": "The Catcher in the Rye", 
        "author": ["J.D. Salinger"], 
        "publication_year": 1951
    },
    {
        "id": 6, 
        "title": "The Hobbit", 
        "author": ["J.R.R. Tolkien", "Alan Lee"], # Added Illustrator
        "publication_year": 1937
    },
    {
        "id": 7, 
        "title": "Fahrenheit 451", 
        "author": ["Ray Bradbury"], 
        "publication_year": 1953
    },
    {
        "id": 8, 
        "title": "Moby Dick", 
        "author": ["Herman Melville"], 
        "publication_year": 1851
    },
    {
        "id": 9, 
        "title": "War and Peace", 
        "author": ["Leo Tolstoy", "Louise Maude"], # Added Translator
        "publication_year": 1869
    },
    {
        "id": 10, 
        "title": "The Alchemist", 
        "author": ["Paulo Coelho", "Alan R. Clarke"], # Added Translator
        "publication_year": 1988
    },
    {
        "id": 11, 
        "title": "The Da Vinci Code", 
        "author": ["Dan Brown"], 
        "publication_year": 2003
    },
    {
        "id": 12, 
        "title": "The Hunger Games", 
        "author": ["Suzanne Collins"], 
        "publication_year": 2008
    },
    {
        "id": 13, 
        "title": "Harry Potter and the Sorcerer's Stone", 
        "author": ["J.K. Rowling"], 
        "publication_year": 1997
    },
    {
        "id": 14, 
        "title": "The Kite Runner", 
        "author": ["Khaled Hosseini"], 
        "publication_year": 2003
    },
    {
        "id": 15, 
        "title": "Life of Pi", 
        "author": ["Yann Martel"], 
        "publication_year": 2001
    }
]

# Sample Data: List of Students
students = [
                {"id": 101, "name": "Alice", "scores": {"Math": 90, "Science": 85, "English": 88, "History": 92}},
                {"id": 102, "name": "Bob", "scores": {"Math": 75, "Science": 80, "English": 70, "History": 65}},
                {"id": 103, "name": "Charlie", "scores": {"Math": 60, "Science": 95, "English": 80, "History": 78}},
                {"id": 104, "name": "Diana", "scores": {"Math": 95, "Science": 98, "English": 92, "History": 88}},
                {"id": 105, "name": "Evan", "scores": {"Math": 55, "Science": 60, "English": 45, "History": 50}},
                {"id": 105, "name": "Shivam", "scores": {"Math": 100, "Science": 100, "English": 100, "History": 100}}
            ]

@app.route('/api/books/', methods=['GET'])
def get_books():
    """Returns the list of books in JSON format."""
    return jsonify({
        "status": "success",
        "count": len(books),
        "data": books
    })
@app.route('/api/students/',methods=['GET'])
def get_data():
    return jsonify({
        "status":"success",
        "count":len(books),
        "data":students
    })

if __name__ == '__main__':
    # Running in debug mode for easier testing
    app.run(debug=True)