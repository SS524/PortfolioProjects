from flask import Flask,render_template,request,jsonify
app=Flask(__name__)
import pickle
import json
import numpy as np
__locations = None
__data_columns = None
__model = None

@app.route('/',methods=['GET'])
def Home():
    return render_template('app.html')

def get_estimated_price(bhk,sqft,location):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = bhk
    x[1] = sqft
    if loc_index>=0:
        x[loc_index] = 1

    return round(__model.predict([x])[0],2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    with open("./columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[2:]  # first 2 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open('./kolkata_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    bhk = int(request.form['bhk'])
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    load_saved_artifacts()

    output=get_estimated_price(bhk,total_sqft,location)
    return render_template('app.html',prediction_text="You Can Buy The Flat at {} ₹".format(output))

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    load_saved_artifacts()
    app.run()

