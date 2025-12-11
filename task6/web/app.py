from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST")
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    locale = request.values.get('locale', 'en_US')
    seed = request.values.get('seed', 'demo')
    batch_idx = int(request.values.get('batch_idx', 0))
    batch_size = int(request.values.get('batch_size', 10))

    if request.method == 'POST' and request.form.get('action') == 'next':
        batch_idx += 1

    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "SELECT * FROM generate_batch(%s,%s,%s,%s);",
            (locale, seed, batch_idx, batch_size)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        rows = []
        print("Error fetching data:", e)

    return render_template(
        'index.html',
        rows=rows,
        locale=locale,
        seed=seed,
        batch_idx=batch_idx,
        batch_size=batch_size
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)