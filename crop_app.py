import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

def predict_crops_with_alternatives(input_features, n_alternatives=2):
    # Load the trained model
    model = joblib.load('crop_app','r')
    
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

@app.route('/predict')
def prediction():
    return render_template('predict.html')

@app.route('/form', methods=["POST"])
def form_handler():
    # Extract form data
    Nitrogen = float(request.form['Nitrogen'])
    Phosphorus = float(request.form['Phosphorus'])
    Potassium = float(request.form['Potassium'])
    Temperature = float(request.form['Temperature'])
    pH = float(request.form['pH'])
     
    values = [Nitrogen, Phosphorus, Potassium, Temperature, pH]
    
    if pH > 0 and pH <= 14 and Temperature < 70 and Temperature> 0:
        best_crop, best_crop_probability, alternative_crops = predict_crops_with_alternatives(values)
        # Passing both the best crop and alternatives to the template
        return render_template('prediction.html', best_crop=best_crop, best_crop_probability=best_crop_probability, alternatives=alternative_crops)
    else:
        return "Sorry... Error in entered values in the form. Please check the values and fill it again."

if __name__ == '__main__':
    app.run(debug=True)
