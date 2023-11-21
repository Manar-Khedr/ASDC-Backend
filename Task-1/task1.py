'''
RUN CURL COMMAND:
curl -X POST -F "id=12" -F "file=@Task-1.xlsx" http://127.0.0.1:5000/upload_and_get_data
'''

# Imports
from flask import Flask, request, jsonify
import pandas as pd

# Initially empty DataFrame
df=None

app = Flask(__name__)

#where the excel file and given id request will be sent
@app.route('/upload_and_get_data', methods=['POST','GET'])
def upload_file():
    try:
        # Get the request ID
        requested_id = request.form.get('id')
        if not requested_id:
            return jsonify("No ID in request")

        # Check if file is requested
        if 'file' not in request.files:
            return jsonify('No file in the request')

        # Store the file received
        file = request.files['file']

        # If the user added an empty file request
        if file.filename == '':
            return jsonify('No file selected')

        # Make sure it is an excel file extension (.xlsx)
        if file and file.filename.endswith(".xlsx"):

            # Add the requested file in an "uploads" folder to ensure it is received
            upload_folder = 'uploads'
            file.save(f'{upload_folder}/{file.filename}')

            #Initialize the DataFrame with the file received
            global df
            df=pd.read_excel(file)

            # Print the df in terminal
            print(df)
            #Print requested id in terminal
            print("ID:",requested_id)
            print(type(requested_id))

            # Get the raw data from the file using the requested ID
            result = df[df['ID'] == int(requested_id)].to_dict(orient='records')
            print(result)

            if not result:
                return jsonify('ID not found'), 404

            return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)



