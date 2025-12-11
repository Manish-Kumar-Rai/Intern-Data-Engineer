from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

# Load environment variables from .env locally
load_dotenv()

app = Flask(__name__)

def get_conn():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise Exception("DATABASE_URL environment variable not set")
    return psycopg2.connect(db_url)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Read query parameters or form inputs
    locale = request.values.get('locale', 'en_US')
    seed = request.values.get('seed', 'demo')
    batch_idx = int(request.values.get('batch_idx', 0))
    batch_size = int(request.values.get('batch_size', 10))

    # Handle "Next Batch" button
    if request.method == 'POST' and request.form.get('action') == 'next':
        batch_idx += 1

    rows = []
    try:
        # Connect to database and fetch generated batch
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            "SELECT * FROM generate_batch(%s, %s, %s, %s);",
            (locale, seed, batch_idx, batch_size)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error fetching data:", e)

    # Render HTML template
    return render_template(
        'index.html',
        rows=rows,
        locale=locale,
        seed=seed,
        batch_idx=batch_idx,
        batch_size=batch_size
    )

if __name__ == '__main__':
    # Use port 5000 locally; Render overrides $PORT automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
