from flask import Flask, render_template, request
from models import *

from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///store.db')
Session = sessionmaker(bind=engine)


app = Flask(__name__)

@app.route("/")
def hello_world():
    session = Session()
    product = session.query(Product).all()
    product = product+product+product+product
    return render_template("index.html", product=product)

@app.route("/add_product")
def add_product():
    session = Session()
    tg_id = request.args.get('tg_id')
    p_id = request.args.get('p_id')
    print(tg_id, p_id)
    if p_id != None and tg_id != None:
        try:
            basket = Basket(tg_id=tg_id, product_id=p_id)
            session.add(basket)
            session.commit()
            return "true"
        except Exception as e:
            pass
        
    return "false"
    
    #product = session.query(Product).all()
    #product = product+product+product+product
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=50100, debug=True, ssl_context=("cert.pem", "key.pem"))