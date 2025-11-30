from flask import Flask, request
from math import gcd

app = Flask(__name__)

def lcm(a,b):
    return abs(a*b)// gcd(a,b)

@app.get('/hire_manishrai_gmail_com')
def compute_lcm():
    x = request.args.get('x')
    y = request.args.get('y')

    try:
        x = int(x)
        y = int(y)
        if x < 0 or y < 0:
            return 'NaN'
    except:
        return 'NaN'
    
    return str(lcm(x,y))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
