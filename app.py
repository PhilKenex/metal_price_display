from flask import Flask, render_template, jsonify
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Load the metal data
with open("rounded_structured_metal_data.json", "r") as file:
    data = json.load(file)
metals_data = data['Metals']

@app.route('/')
def index():
    return render_template('index.html', metals=metals_data)

@app.route('/plot/<metal_name>')
def plot(metal_name):
    # Get the metal's data
    metal = next((m for m in metals_data if m['Metal_Name'] == metal_name), None)
    if not metal:
        return jsonify(data=[])

    # Create the time-series plot using Plotly
    dates = [entry['Date_Collected'] for entry in metal['Prices']]
    prices = [entry['Price'] for entry in metal['Prices']]
    
    graph = {
        'data': [
            go.Scatter(
                x=dates,
                y=prices,
                mode='lines+markers'
            )
        ],
        'layout': {
            'title': metal['Metal_Name']
        }
    }

    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify(data=[graphJSON])

if __name__ == '__main__':
    app.run(debug=True)
