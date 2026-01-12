import sqlite3
import requests
import pandas as pd # keeping this just in case I need it later


class Library:
    def __init__(self,url="http://127.0.0.1:5000/api/books/",db_path='library.db'):
        self.url = url
        self.db_conn = self.setup_db(db_path)
        
    def setup_db(self,db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # keeping foreign keys on
        c.execute("PRAGMA foreign_keys = ON;")
        
        c.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT, 
            year INTEGER)''')
            
        c.execute('''CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT UNIQUE)''')
            
        c.execute('''CREATE TABLE IF NOT EXISTS book_author (
            book_id INTEGER,
            author_id INTEGER,
            FOREIGN KEY(book_id) REFERENCES books(id),
            FOREIGN KEY(author_id) REFERENCES authors(id))''')
            
        conn.commit()
        # conn.close()
        return conn

    def main(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()["data"]
            # testing with dummy data for now
            # data = [
            #     {
            #         "title": "Game of thrones",
            #         "author": ["Georgw R.R. Martin"], # typo in source
            #         "publication_year": 2001
            #     }
            # ]
            # conn = sqlite3.connect('library.db')
            c = self.db_conn.cursor()
            
            for item in data:
                print(f"Processing {item['title']}...")
                
                # insert book
                c.execute("INSERT INTO books (title, year) VALUES (?, ?)", (item['title'], item['publication_year']))
                book_id = c.lastrowid
                
                # handle authors
                for auth in item['author']:
                    # check if author exists
                    c.execute("SELECT id FROM authors WHERE name = ?", (auth,))
                    existing_auth = c.fetchone()
                    
                    if existing_auth:
                        auth_id = existing_auth[0]
                    else:
                        c.execute("INSERT INTO authors (name) VALUES (?)", (auth,))
                        auth_id = c.lastrowid
                    
                    # link them
                    c.execute("INSERT INTO book_author VALUES (?, ?)", (book_id, auth_id))

            self.db_conn.commit()
            print("Done.")
            
            # quick check
            dfbook = pd.read_sql("SELECT * FROM books ", self.db_conn)
            dfauthor = pd.read_sql("SELECT * FROM authors ", self.db_conn)
            dfAuthBook = pd.read_sql("SELECT * FROM book_author ", self.db_conn)
            print("-- Books -- \n",dfbook)
            print("-- Author -- \n",dfauthor)
            print("-- books_author -- \n",dfAuthBook)

        except Exception as e:
            print("Something went wrong:", e)
        finally:
            self.db_conn.close()

if __name__ == "__main__":
    # setup_db()
    # run_script()
    s = Library()
    s.main()