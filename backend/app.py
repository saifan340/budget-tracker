from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app) 

VALID_TYPES = ['income', 'expense']

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

# --GET /transactions ----------------------------
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

# --POST /transaction ----------------------------
@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    
    #--validation--
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'type' not in data or not data['type']:
        return jsonify({'error': 'type is required'}), 400
    
    if data['type'] not in VALID_TYPES:
        return jsonify({'error': f'type must be one of {VALID_TYPES}'}), 400
    
    if 'amount' not in data or data['amount'] is None:
        return jsonify({'error': 'amount is required'}), 400
    
    if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        return jsonify({'error': 'amount must be a positive number'}), 400
    
    if 'catagory' not in data or not data['category']:
        return jsonify({'error': 'category is required'}), 400
    # --- end validation --
    
    
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

# --- Delete /transactions/<id> -----------------
@app.route('/transactions/<int:id>', methods =['DELETE'])
def delete_transaction(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # check if transaction exists first 
    c.execute('SELECT id FROM transactions WHERE id = ?', (id,))
    transaction = c.fetchone()
    
    if not transaction:
        conn.close()
        return jsonify({'error': 'Transaction not found'}), 404
    
    
    c.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'transaction deleted!'})
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)
    
    


    
    


