from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    about_text = """Our system integrates advanced soil analysis techniques with sophisticated crop recommendation algorithms to provide tailored guidance to farmers. By analyzing soil composition, nutrient levels, and environmental factors, we deliver personalized recommendations for crop selection, fertilization, irrigation, and pest management."""
    return about_text


@app.route('/Help')
def help():
    contact_info = {
        'telephone': '+265881401065',
        'email': 'croprecommendation@gmail.com'
    }
    return render_template('Help.html', contact_info=contact_info)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        return redirect(url_for('home')) 
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
