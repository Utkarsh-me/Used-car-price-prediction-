from flask import Flask, request, jsonify, render_template
from supabase import create_client, Client
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Supabase credentials
SUPABASE_URL = "https://ivarjhpbeasabwwtmvnx.supabase.co"  # Add your Supabase URL here
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml2YXJqaHBiZWFzYWJ3d3Rtdm54Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzc4MjA3NDksImV4cCI6MjA1MzM5Njc0OX0.ZxUCDNIPBWLjJuN71fc7xlTdplOqNGRI2JPPpEjfW9U"  # Add your Supabase Service Role Key here

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load ML model
model = pickle.load(open('used_car.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('car_land.html')

@app.route("/predict", methods=['POST', 'GET'])
def predict():
    try :
        if request.method == "POST":
            brand = (request.form['brand'])
            year = (request.form['year'])
            price = (request.form['price'])
            kms = (request.form['kms'])
            fuel = (request.form['fuel'])
            seller = (request.form['seller'])
            transmission = (request.form['transmission'])
            owner = (request.form['owner'])
        
        # Prepare input data for the model
            arr = np.array([[brand,year, price, kms, fuel, seller, transmission, owner]])
            prediction = model.predict(arr)


            data = {
                'brand' : brand,
                'year' : year,
                'price' : price,
                'kms' : kms,
                'fuel' : fuel,
                'seller' : seller,
                'transmission' :transmission,
                'owner' : owner,
                'predicted_price': int(prediction[0])
            }
            response = supabase.table("used_car_price").insert(data).execute()

        return render_template('car_res.html', prediction=prediction)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)