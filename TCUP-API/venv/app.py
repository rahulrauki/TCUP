from flask import Flask, send_from_directory, request, jsonify, send_file
from collections import defaultdict
import pandas as pd
import logging as log
import pymongo
import os, requests, json
import openai
import ast, re

app = Flask(__name__)
config = {} # Placeholder
with open('api-config.json', 'r') as config_json:
    config = json.load(config_json)

# DB initialization
myclient = pymongo.MongoClient(config['db_credentials']['hostname'])
mydb = myclient[config['db_credentials']['db_name']]
mycol = mydb[config['db_credentials']['collection_name']]

# OpenAI initialization
openai.api_key = config['open_api_credentials']['api_key']
model = config['open_api_credentials']['model']

# Alias mapping helper
alias_map = config['alias_mapping']


class ResultData

# Serve Angular build files
angular_files_path = config['angular_build_files']['path']
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_angular_build(path):
    if path != "" and os.path.exists(angular_files_path + path):
        
        # Set MIME type based on file extension
        if path.endswith('.js'):
            mimetype = 'application/javascript'
        elif path.endswith('.css'):
            mimetype = 'text/css'
        else:
            mimetype = None
        return send_from_directory(angular_files_path, path, mimetype=mimetype)
    else:
        return send_from_directory(angular_files_path, "index.html")


# API endpoints that make queries to MongoDB
# Get map data
@app.route('/api/mapdata', methods=['GET'])
def get_mapdata():
    raw_data_list, coord_list = [], []
    response_data = {
        "status" : 200,
        "data" : [] }
    # getting data regarding the index from which the data has to be sent
    index = request.args.get("index", "") # 'index' is the param sent from UI
    if index == "" : index = 0
    else: index = int(index)
    try:
        raw_data_list = [document for document in mycol.find({}, {'_id':0})]
        coord_list = map_coords_helper(raw_data_list[index:])
        response_data['data'] = coord_list
    except:
        response_data['status'] = 500
    return jsonify(response_data)

@app.route('/api/plotdata', methods=['GET'])
def get_plotdata():
    raw_data_list = []
    response_data = {
        "status" : 200,
        "data" : {} }
    # getting data regarding the index from which the data has to be sent
    index = request.args.get("index", "") # 'index' is the param sent from UI
    if index == "" : index = 0
    else: index = int(index)
    try:
        raw_data_list = [document for document in mycol.find({}, {'_id':0})]
        response_data['data'] = raw_to_plot_data(raw_data_list[index:])
    except:
        response_data['status'] = 500
    return jsonify(response_data)

@app.route('/api/data', methods=['GET'])
def get_data():
    raw_data_list, mapped_data_list = [], []
    response_data = {
        "status" : 200,
        "data" : [] }
    # getting data regarding the index from which the data has to be sent
    index = request.args.get("index", "") # 'index' is the param sent from UI
    if index == "" : index = 0
    else: index = int(index)
    try:
        raw_data_list = [document for document in mycol.find({}, {'_id':0})]
        mapped_data_list = alias_map_helper(raw_data_list[index:]) # accessing everything from index
        response_data['data'] = mapped_data_list
    except:
        response_data['status'] = 500
    return jsonify(response_data)
    

@app.route('/api/report', methods=['GET'])
def get_report():
    report_path = config["report"]['path']
    report_name = config['report']['report_name']
    return send_from_directory(report_path, report_name, mimetype='text/html')

@app.route('/api/insights', methods=['POST'])
def get_insights():
    request_data = request.get_json()
    prompt_data = request_data.get('data')
    x_axis, y_axis = prompt_data.keys()
    prompt = f"Give some insights about this plot data between {x_axis} and {y_axis}, data is {json.dumps(prompt_data)}"
    insight_from_gpt = ''
    response_data = {
        "status" : 200,
        "data" : ''
    }
    try:
        insight_from_gpt = insight_helper(model=model, prompt=prompt)
        response_data['data'] = insight_from_gpt
    except:
        response_data['status'] = 500
    return jsonify(response_data)

@app.route('/api/addprocess', methods=['POST'])
def add_process():
    request_data = request.get_json()
    new_name = request_data.get("name")
    equation = request_data.get("equation")
    codecs_data = [equation, new_name]
    response_data = {
        "status" : 200,
        "data" : ''
    }
    codecs_return = add_preprocess_data(codecs_data)
    response_data['status'] = codecs_return["status"]
    response_data['data'] = codecs_return["message"]
    if response_data['status'] == 200:
        update_alias_json(new_name)
    return jsonify(response_data)

@app.route('/api/addrelation', methods=['POST'])
def add_relation():
    request_data = request.get_json()
    condition_list = request_data.get("condition")
    response_data = {
        "status" : 200,
        "data" : ''
    }
    function_result = add_condition_to_db(condition_list)
    response_data['status'] = function_result['status']
    response_data['data'] = function_result['message']
    # Placeholder to add logic if need be
    return jsonify(response_data)
    


@app.route('/api/export', methods=['GET'])
def get_exportdata():
    raw_data_list, mapped_data_list = [], []
    default_fail_list = [
        {"status": 500, "message" : "No Valid data or unknown error"}
    ]
    index = request.args.get("index", "") # 'index' is the param sent from UI
    if not index == "" : index = int(index)
    try:
        raw_data_list = [document for document in mycol.find({}, {'_id':0})]
        if index == "" : index = len(raw_data_list)
        mapped_data_list = alias_map_helper(raw_data_list[:index]) # We generate report for given number of data
        list_to_xlsx(mapped_data_list)
    except:
        list_to_xlsx(default_fail_list)
    return send_file('export_data.xlsx', as_attachment=True)

@app.route('/api/clientstatus', methods=['GET'])
def get_client_status():
    result_data = {
        "status" : 200,
        "current_status" : ''
    }
    try:
        with open('api-config.json', 'r') as config_file:
            result_data['current_status'] = json.load(config_file)['client_status']
    except:
        result_data['current_status'] = 'Offline'
        result_data['status'] = 500
    return jsonify(result_data)


#'''''''''''''''''''#
#   HELPER METHODS  #
#'''''''''''''''''''#
# Calls ChatGPT API to get insights on the given data
def insight_helper(model, prompt):
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=20)
    return response.choices[0].text

# Maps alias to actual names
def alias_map_helper(raw_list):
    mapped_list = list()
    raw_list_copy = raw_list[:] #Just to be sure as objects are CBR
    for document in raw_list_copy:
        mapped_dict = {}
        for alias, value in document.items():
            if alias in alias_map: mapped_dict[alias_map[alias]] = value
            else: mapped_dict[alias] = value
        mapped_list.append(mapped_dict)
    return mapped_list

# Iterates through the raw list and returns the co-ordinates as List[List[int, int]]
def map_coords_helper(raw_list):
    return [document["2"] for document in raw_list] # Accessing "2" which is stored as "2": [123,123]
      
# Takes a list of dict of data and converts to excel (xlsx) using pandas
def list_to_xlsx(mapped_list):
    df = pd.DataFrame(mapped_list)
    # Create a new Excel file and write the DataFrame to it
    with pd.ExcelWriter('export_data.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

# Takes a list of dicts and returns dict of lists of values of each attribute
def raw_to_plot_data(raw_list):
    plot_data_dict = defaultdict(list)
    for document in raw_list:
        for alias, value in document.items():
            if alias in alias_map:
                plot_data_dict[alias_map[alias]].append(value)
    return plot_data_dict

# Helper Method that handles dynamically adding new process
def add_preprocess_data(x):
    a=x
    with open('app_process.py', 'r') as f:
        code = f.read()
        module = ast.parse(code)
        my_list = ast.literal_eval(module.body[0].value)
    with open("subscribe.json") as jsonFileSub:
        jsonObjectsub = json.load(jsonFileSub)
    metric=jsonObjectsub[1]['metricValue']
    try:
        b=re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', a[0])
        for i in b:
            if len(i)>0:
                for k, v in metric.items():
                    if v ==i.strip():
                        a[0]=a[0].replace(i,'?'+k+'?',-1)
                        break
        # Update the list
        my_list.append(a)

        # Save the updated list to the file
        with open('app_process.py', 'w') as f:
            f.write(f"my_list = {my_list}")
        return {"status" : 200, "message" : "Successfully added a new process"}
    except:
        return {"status" : 500 , "message" : "Please check the format correctly"}
    
# Adds the condtion to the DB
def add_condition_to_db(condition):
    pass # return dict[status, data]

# Adds new alias to alias_mapping in api-config.json file
def update_alias_json(new_variable):
    alias_map[new_variable] = new_variable
    config['alias_mapping'] = alias_map
    with open("api-config.json", "w") as api_config_file:
        json.dump(config, api_config_file)


if __name__ == '__main__':
    app.run()
