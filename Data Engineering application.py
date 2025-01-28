
from flask import Flask, request, render_template_string, send_file
import pandas as pd
import os
import threading
from werkzeug.serving import make_server

app = Flask(__name__)
UPLOAD_FOLDER = '/home/banupr15/preprocess/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML templates with CSS for styling and layout
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Excel File</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            width: 100%;
            max-width: 400px;
            padding: 20px;
            background-color: white;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        h1 {
            font-size: 1.5em;
            color: #333;
        }
        form {
            margin-top: 15px;
        }
        input[type="file"] {
            margin: 10px 0;
            padding: 8px;
        }
        input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 1em;
            border-radius: 5px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload Excel File</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="Upload">
        </form>
    </div>
</body>
</html>
"""

select_columns_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Select Columns</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            width: 100%;
            max-width: 500px;
            padding: 20px;
            background-color: white;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        h1 {
            font-size: 1.5em;
            color: #333;
        }
        form {
            margin-top: 15px;
            text-align: left;
        }
        input[type="checkbox"] {
            margin-right: 10px;
        }
        input[type="submit"] {
            margin-top: 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 1em;
            border-radius: 5px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Select Columns for Analysis</h1>
        <form action="/select_identifier" method="post">
            <input type="hidden" name="filename" value="{{ filename }}">
            {% for column in columns %}
                <label><input type="checkbox" name="columns" value="{{ column }}">{{ column }}</label><br>
            {% endfor %}
            <input type="submit" value="Next">
        </form>
    </div>
</body>
</html>
"""

select_identifier_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Select Unique Identifier</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            width: 100%;
            max-width: 500px;
            padding: 20px;
            background-color: white;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        h1 {
            font-size: 1.5em;
            color: #333;
        }
        form {
            margin-top: 15px;
            text-align: left;
        }
        select {
            padding: 8px;
            width: 100%;
            margin: 10px 0;
        }
        input[type="submit"] {
            margin-top: 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 1em;
            border-radius: 5px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Select Unique Identifier Column</h1>
        <form action="/select_treatments" method="post">
            <input type="hidden" name="filename" value="{{ filename }}">
            {% for column in selected_columns %}
                <input type="hidden" name="columns" value="{{ column }}">
            {% endfor %}
            <select name="unique_identifier" required>
                {% for column in selected_columns %}
                    <option value="{{ column }}">{{ column }}</option>
                {% endfor %}
            </select>
            <input type="submit" value="Next">
        </form>
    </div>
</body>
</html>
"""

# Added missing HTML template
select_treatments_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Select Treatments</title>
</head>
<body>
    <h1>Select Treatments</h1>
    <form action="/process" method="post">
        <input type="hidden" name="filename" value="{{ filename }}">
        <input type="hidden" name="unique_identifier" value="{{ unique_identifier }}">
        {% for column in columns %}
            <input type="hidden" name="columns" value="{{ column }}">
        {% endfor %}
        {% for treatment in treatments %}
            <label><input type="checkbox" name="treatments" value="{{ treatment }}">{{ treatment }}</label><br>
        {% endfor %}
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Define Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return "No file selected"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        df = pd.read_excel(file_path, dtype=str)
        columns = df.columns.tolist()
        return render_template_string(select_columns_html, columns=columns, filename=file.filename)

    return render_template_string(index_html)

@app.route('/select_identifier', methods=['POST'])
def select_identifier():
    filename = request.form['filename']
    selected_columns = request.form.getlist('columns')
    return render_template_string(select_identifier_html, filename=filename, selected_columns=selected_columns)

@app.route('/select_treatments', methods=['POST'])
def select_treatments():
    filename = request.form['filename']
    unique_identifier = request.form['unique_identifier']
    selected_columns = request.form.getlist('columns')

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_excel(file_path, dtype=str)
    selected_df = df[selected_columns]
    treatments = selected_df['Intervention'].dropna().unique().tolist()
    return render_template_string(select_treatments_html, treatments=treatments, filename=filename, columns=selected_columns, unique_identifier=unique_identifier)


@app.route('/process', methods=['POST'])
def process():
    filename = request.form['filename']
    unique_identifier = request.form['unique_identifier']
    selected_columns = request.form.getlist('columns')
    selected_treatments = request.form.getlist('treatments')

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_excel(file_path, dtype={'TransportID': str})

    df['Intervention'] = df['Intervention'].str.strip()
    filtered_df = df[df['Intervention'].isin(selected_treatments)]

    # Group by unique_identifier and combine TransportID without conflict
    transport_id_df = df.groupby(unique_identifier)['TransportID'].apply(lambda x: ', '.join(x.unique())).reset_index(name='TransportID_combined')
    grouped_df = filtered_df.groupby([unique_identifier, 'Intervention'])['ProcedureDateTime'].apply(lambda x: ', '.join(x.astype(str))).reset_index()
    pivot_df = grouped_df.pivot(index=unique_identifier, columns='Intervention', values='ProcedureDateTime').reset_index()
    pivot_df = pd.merge(transport_id_df, pivot_df, on=unique_identifier, how='left')

    for intervention in selected_treatments:
        pivot_df['Is_' + intervention] = pivot_df[intervention].apply(lambda x: 1 if pd.notna(x) else 0)

    ordered_columns = [unique_identifier, 'TransportID_combined']
    sorted_interventions = sorted(selected_treatments)
    for intervention in sorted_interventions:
        ordered_columns.append('Is_' + intervention)
        ordered_columns.append(intervention)
    pivot_df = pivot_df[ordered_columns]

    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "pivoted_interventions_with_transportid_final.xlsx")
    pivot_df.to_excel(output_file_path, index=False)

    return send_file(output_file_path, as_attachment=True)

# Run the Flask app in a separate thread
class FlaskThread(threading.Thread):
    def run(self):
        make_server('localhost', 5000, app).serve_forever()

flask_thread = FlaskThread()
flask_thread.start()