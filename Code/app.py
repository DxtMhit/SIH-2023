from flask import Flask, render_template, request, redirect, url_for
import csv
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Route for the home page
@app.route('/') 
def index():
    return render_template('index.html')

# Loading dataset for dropout rate analysis and plotting
data = pd.read_csv('DOR.csv')

# Route for the data input form
@app.route('/input_form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        phone_no = request.form['no']
        relation = request.form['relation']
        description = request.form['description']

        with open('student_data.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([name, age, gender, email, phone_no, relation, description])

        return redirect(url_for('form'))

    return render_template('input_form.html')

@app.route('/plot')
def plot2():
    #this will get list of all states for us
    states = data['State_UT'].unique()
    return render_template('plot.html', states=states)

# Route for generating bar graphs
@app.route('/plot', methods=['POST'])
def plot():
    selected_state = request.form['state']
    # this is to select a state
    state_data = data[data['State_UT'] == selected_state]
    plt.figure(figsize=(10, 6))
    plt.bar(state_data['year'], state_data['Primary_Total'])
    plt.xlabel('Year')
    plt.ylabel('Primary Dropout Rate')
    plt.title(f'Dropout Rate in {selected_state} (Primary Level)')
    plt.xticks(rotation=45)

    # Saving plot to BytesIO object
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_data = base64.b64encode(img_buffer.read()).decode('utf-8')
    states = data['State_UT'].unique()
    return render_template('plot.html', states=states, img_data=img_data)

# Route for the analysis page
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# Route for the FAQ Page
@app.route('/faqs')
def faq():
    return render_template('faqs.html')

# Route for the Policies page
@app.route('/policy')
def policy():
    return render_template('policies.html')

if __name__ == '__main__':
    app.run(debug=True)
