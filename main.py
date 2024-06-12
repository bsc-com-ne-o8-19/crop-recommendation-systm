import joblib
import numpy
from flask import Flask, render_template, request, session,redirect

app = Flask(__name__)
#loading the model
model = joblib.load('main','r')

nutrient_adjustments = {
    'Wheat': {'Nitrogen': '+20', 'Phosphorus': '+0', 'Potassium': '+10'},
    'Corn': {'Nitrogen': '+30', 'Phosphorus': '+5', 'Potassium': '+0'},
}

def predict_crops_with_alternatives(input_features, n_alternatives=2):

    
    # Predict probabilities for each class
    probabilities = model.predict_proba([input_features])[0]
    
    # Get the index and probability of the top prediction (best crop)
    best_crop_index = probabilities.argmax()
    best_crop = model.classes_[best_crop_index]
    best_crop_probability = probabilities[best_crop_index]
    
    # Exclude the best crop and get the next best alternatives along with their probabilities
    probabilities[best_crop_index] = 0  # Exclude best crop from alternatives
    alternatives_indices = probabilities.argsort()[-n_alternatives:][::-1]  # Indices of the best alternatives
    alternative_crops = [(model.classes_[i], probabilities[i]) for i in alternatives_indices if probabilities[i] > 0]
    
    return best_crop, best_crop_probability, alternative_crops

@app.route('/')
def home():
    return render_template('Home.html')
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

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('predict_form.html')
    elif request.method == 'POST':
        if model is None:
            return "Model is not loaded, cannot perform predictions"
        
        try:
            # Extracting form data
            Nitrogen = float(request.form['Nitrogen'])
            Phosphorus = float(request.form['Phosphorus'])
            Potassium = float(request.form['Potassium'])
            Temperature = float(request.form['Temperature'])
            pH = float(request.form['pH'])

            # Predicting crop
            features = [Nitrogen, Phosphorus, Potassium, Temperature, pH]
            prediction = model.predict([features])
            probabilities = model.predict_proba([features])[0]
            crops = model.classes_

            # Find the index of the best predicted crop to show its probability
            best_crop_index = numpy.where(crops == prediction[0])[0][0]
            best_crop_probability = probabilities[best_crop_index]

            # Sort the probabilities and exclude the best crop from alternatives
            top_indices = probabilities.argsort()[::-1]  # sort indices by highest probability
            top_indices = [index for index in top_indices if index != best_crop_index]  # remove best crop index

            # Get top 3 alternatives, ensuring we don't include the best crop
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
