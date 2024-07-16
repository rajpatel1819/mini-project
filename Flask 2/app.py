from flask import Flask, render_template, url_for, request, redirect, session
import pickle
import os
import re
app = Flask(__name__)
# Load your trained model
model=pickle.load(open('model.pkl','rb'))
@app.route('/')
def homepage():
    return render_template('index.html')
@app.route('/inner-page',methods=['GET'])
def show_form():
    return render_template('inner-page.html')
@app.route('/resultpage', methods=[ 'POST','GET'])


def predictionpage():
    if request.method == 'POST':  # Correct way to check if the request method is POST
        newsline = request.form["headline"]
        pred = [newsline]
        output = model.predict(pred)
        print(output)  # For debugging purposes

        # Determine the output message based on the prediction
        if output[0] == 2:
            output_msg = 'Upward movement in gold price'
        elif output[0] == 1:
            output_msg = 'Downward movement in gold price'
        elif output[0] == 3:
            output_msg = 'Steady movement in gold price'
        elif output[0] == 4:
            output_msg = 'This news headline is not related to gold news'
        else:
            output_msg = 'Prediction not found'

        return render_template('resultpage.html', output_msg=output_msg)

    # If GET request or no prediction made, render the template without output message
    return render_template('resultpage.html')

if __name__ == '__main__':
    app.run(debug=True)
