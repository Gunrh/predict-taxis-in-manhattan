from flask import Flask, request, jsonify
app = Flask(__name__)
import util


@app.route('/predict_per_area', methods=['GET','POST'])
def predict_taxi_per_area():

    # receive the features
    zone_list = request.json['zone'] #user give list of string
    date = str(request.json['date']) 
    time = str(request.json['time'])
    responses = []

    for area in zone_list:
        responses.append( {'total_num_of_taxi  ' + area: util.predict_sum_of_taxi([area],date,time )})

    return jsonify(responses)



@app.route('/get_zones_names', methods=['GET','POST'])
def get_zones_names():
    response = jsonify({'locations': util.ListZonesNames()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

    
# @app.route('/demo', methods=['GET','POST'])
# def demo():
#        #Get the var of zones
#     zone_list= ['Tribeca','Soho']
#     # Get the current date
#     current_date = datetime.datetime.now()
#     # Add one day to the current date
#     next_day = current_date + datetime.timedelta(days=1)
#     input_date =next_day.strftime('%Y-%m-%d')
#     #Get the var of input_time
#     from datetime import datetime, timedelta
#     # Get the current time
#     now = datetime.now()
#     # Calculate the time 3 hours from now
#     next_3_hours = now + timedelta(hours=3)
#     mintues = '00'
#     input_time = next_3_hours.strftime(f'%H:{mintues}')
#     responses = []

#     for area in zone_list:
#         responses.append( {'total_num_of_taxi_' + area: util.predict_sum_of_taxi([area],input_date,input_time )})
    
#     print(responses)
        
#     return jsonify(responses)

 
if __name__ == "__main__":

    from waitress import serve
    serve(app,host='0.0.0.0',port=5000)

    app.run()
