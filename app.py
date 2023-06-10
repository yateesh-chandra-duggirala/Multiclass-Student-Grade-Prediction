from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
import pandas as pd
import joblib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Load the trained model
model = joblib.load('./model/GradeClassifier.pkl')

# Define the home route
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for serving static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'static'), filename)


# Define the certificate route
@app.route('/certificate')
def certificate():
    gender = request.args.get('gender')
    name = request.args.get('name')
    year = request.args.get('year')
    gpa = request.args.get('gpa')
    marks = request.args.get('marks')
    grade = request.args.get('grade')
    prediction = request.args.get('prediction')

    return render_template('certification.html', gender=gender, name=name, year=year, gpa=gpa, marks=marks, grade=grade, prediction=prediction)

# Define the error route
@app.route('/error')
def error():
    gender = request.args.get('gender')
    name = request.args.get('name')

    return render_template('error.html', gender = gender, name = name)

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve the input values from the form
    year = request.form['year']
    credit_hour = request.form['credit_hour']
    gpa = request.form['gpa']
    grade = request.form['grade']
    total_marks = request.form['total_marks']
    student_id = request.form['student_id']
    gender = request.form['gender']
    
    # Create a pandas DataFrame with the input values
    input_data = pd.DataFrame({
        'Year': [year],
        'Credit Hour': [credit_hour],
        'Grade Pointer Average': [gpa],
        'Grade': [grade],
        'Total Marks': [total_marks]
        # Add the other attributes here
    })

    # Make the prediction
    prediction = model.predict(input_data)

    # Store the student ID in the session
    session['student_id'] = student_id
    session['gender'] = gender
    grade = int(request.form['grade'])


    # Render the result template with the predicted output and student ID
    return render_template('result.html', prediction=prediction, gender = gender, student_id=student_id, grade = grade)

if __name__ == '__main__':
    app.run(debug=True)
