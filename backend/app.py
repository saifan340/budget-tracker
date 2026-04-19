from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app) 

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS transactions (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  type TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT,
                  description TEXT,
                  date TEXT NOT NULL
                  )
                ''')
    conn.commit()
    conn.close()

# retrieve all transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    
    transactions = []
    for row in rows:
        transactions.append({
            'id': row[0],
            'type': row[1],
            'amount': row[2],
            'category':row[3],
            'description': row[4],
            'date': row[5]
        })
    return jsonify(transactions)

# add new transaction
@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO transactions (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        data['type'],
        data['amount'],
        data['category'],
        data.get('description', ''),
        datetime.now().strftime('%Y-%m-%d')
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Transation gespeichert!'}), 201

# delete transaction
@app.route('/transactions/<int:id>', methods =['DELETE'])
def delete_transaction(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ?', (int(id),))
    conn.commit()
    conn.close()
    return jsonify({'message': 'transaction deleted!'})
if __name__ == '__main__':
    init_db()
    #yapp.run(debug=True)
    app.run(debug=True, port=8000)
    
    


    
    


