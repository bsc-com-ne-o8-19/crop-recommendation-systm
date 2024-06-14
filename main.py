import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

try:
    model_pipeline = joblib.load('main','r')
except FileNotFoundError:
    print("Model file not found. Please check the file path.")
    model_pipeline = None

district_data = {
    "Chiradzulu": {
        "humidity": "70",
        "temperature": "25",
        "zinc": "2.7",
        "iron": "60.5",
        "carbon": "17.2",
        "magnesium": "180.3",
        "aluminium": "163",
        "calcium": "896.8",
        "depth": "200",
        "stoniness": "1.7",
        "rainfall": "387.60"
    },
    "Zomba": {
        "humidity": "60",
        "temperature": "23.5",
        "zinc": "1.7",
        "iron": "80.5",
        "carbon": "26.3",
        "magnesium": "199.3",
        "aluminium": "147.5",
        "calcium": "811.5",
        "depth": "200",
        "stoniness": "1.5",
        "rainfall": "906"
    },
    "Blantyre": {
        "humidity": "80",
        "temperature": "27.5",
        "zinc": "2.3",
        "iron": "89",
        "carbon": "29",
        "magnesium": "243.7",
        "aluminium": "89",
        "calcium": "896.8",
        "depth": "200",
        "stoniness": "0.3",
        "rainfall": "834"
    },
    "Thyolo": {
        "humidity": "70",
        "temperature": "25",
        "zinc": "2.7",
        "iron": "60.5",
        "carbon": "17.2",
        "magnesium": "180.3",
        "aluminium": "163",
        "calcium": "896.8",
        "depth": "200",
        "stoniness": "1.7",
        "rainfall": "387.60"
    },
    "Chikwawa": {
        "humidity": "60",
        "temperature": "23.5",
        "zinc": "1.7",
        "iron": "80.5",
        "carbon": "26.3",
        "magnesium": "199.3",
        "aluminium": "147.5",
        "calcium": "811.5",
        "depth": "200",
        "stoniness": "1.5",
        "rainfall": "906"
    }
}

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/district-data')
def get_district_data():
    return jsonify(district_data)

@app.route('/about')
def about():
    about_text = """Our system integrates advanced soil analysis techniques with sophisticated crop recommendation algorithms to provide tailored guidance to farmers. By analyzing soil composition, nutrient levels, and environmental factors, we deliver personalized recommendations for crop selection."""
    return render_template('about.html', about_text=about_text)

@app.route('/Help')
def help():
    contact_info = {
        'telephone': '+265881401065',
        'email': 'croprecommendation@gmail.com'
    }
    return render_template('Help.html', contact_info=contact_info)

@app.route('/predict', methods=['POST'])
def predict():
    if model_pipeline is None:
        return "Model is not loaded, cannot perform predictions"
    
    try:
        features = [
            float(request.form['Nitrogen']),
            float(request.form['Phosphorus']),
            float(request.form['Potassium']),
            float(request.form['Temperature']),
            float(request.form['humidity']),
            float(request.form['pH']),
            float(request.form['rainfall']),
            float(request.form['ZINC']),
            float(request.form['IRON']),
            float(request.form['CARBON']),
            float(request.form['MAGNESIUM']),
            float(request.form['ALUMINIUM']),
            float(request.form['CALCIUM']),
            float(request.form['DEPTH']),
            float(request.form['STONINESS'])
          
        ]
        
         

        prediction = model_pipeline.predict([features])
        probabilities = model_pipeline.predict_proba([features])[0]
        crops = model_pipeline.classes_

        best_crop_index = np.where(crops == prediction[0])[0][0]
        best_crop_probability = probabilities[best_crop_index]

        top_indices = probabilities.argsort()[::-1]
        top_indices = [index for index in top_indices if index != best_crop_index]

        alternatives = [(crops[i], "{:.2%}".format(probabilities[i])) for i in top_indices[:2]]

        return render_template('predict.html', prediction=prediction[0], prediction_probability="{:.2%}".format(best_crop_probability), alternatives=alternatives, all_crops=crops)
    except Exception as e:
        return str(e)

@app.route('/adjustments', methods=['POST'])
def adjustments():
    crop = request.form['crop_choice']
    if crop in nutrient_adjustments:
        adjustments = nutrient_adjustments[crop]
        return render_template('adjustments.html', crop=crop, adjustments=adjustments)
    else:
        return f"No nutrient adjustment information available for {crop}."

if __name__ == '__main__':
    app.run(debug=True)
