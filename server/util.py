import json
import datetime
import requests
import pickle
import pandas as pd
__locations = None

#input features
def predict_sum_of_taxi(zone_list,input_date,input_time): 


    time_hr_min = datetime.datetime.strptime(str(input_time), "%H:%M")
    time = str(time_hr_min.hour) + ':00'
    full_dt = input_date + ' ' +time+':00' #'2022-12-31 22:00:00' 
        
    # zone_list= ['Tribeca']
    zones_dict = getZones(zone_list)
    weekday_dict = getWeekDay(input_date)
    time_bin_dict =getTimeBinned(input_time)
    weather_dict =getWeather(full_dt )

    ## merge the all dicts
    feature_input_dict = {**zones_dict, **weekday_dict , **time_bin_dict, **weather_dict}

    #lower dict keys
    feature_input_dict = lower_dict_keys(feature_input_dict)

    #import the json columons and fill with values 0
    json_columons =json_columns_dict0()

    #create the dict with all sample of coulmons
    model_sample_dict = update_dict_values(json_columons,feature_input_dict)

    ## convert the dict to dataframe
    model_sample_df = pd.DataFrame(model_sample_dict, index=[0])

    #import the xgboost model and predict
    taxi_predict_model =get_model()
    #predicted
    predicted_num_of_taxi= str(taxi_predict_model.predict(model_sample_df)[0])
    #take a whole number of taxi drovers
    result = predicted_num_of_taxi.split(".")[0]

    return result







def get_model():
    with open('./artifacts/taxi_project_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    return __model




def json_columns_dict0(): # step 2
    #filling the json columons value with 0 and return dict
    with open("./artifacts/columns.json", "r") as f:
        data_columns = json.load(f)

    data_column_dict_0 = {}
    for column in data_columns["data_columns"]:
        data_column_dict_0[column] = 0 

    return data_column_dict_0


def update_dict_values(main_dict, sec_dict): # step 3
  #Returns a dictionary with the keys in the main dictionary and with the values ​​of sec_dict
  # input main_dict= {"Avi":0 ,"Beth":0 ,"Gamil":0}
  # input sec_dict ={"Noam":12 ,"Beth":2,"Avi":1 }
  # output {'Avi': 1, 'Beth': 2, 'Gamil': 0}
  
  updated_main_dict = {}
  for key in main_dict:
    if key in sec_dict:
      updated_main_dict[key] = sec_dict[key]
    else:
      updated_main_dict[key] = main_dict[key]
  return updated_main_dict




def lower_dict_keys(dictionary): #lower dict keys
    lower_dict = {}
    for key in dictionary:
        lower_key = key.lower()
        lower_dict[lower_key] = dictionary[key]
    return lower_dict



###~~~~~~~~~~~~~~~ ETL functions ###~~~~~~~~~~~~~~~
def get_hours_label(min: int, max: int):
    """ the function creates a list of labels in the format 00:00 - 00:59 for
        example

    Args:
        min (int): min hour (0)
        max (int): max hour (24)

    Returns:
        List: Returns a list of strings ( labels )
    """
    return [f'{s:02d}:00 - {s:02d}:59' for s in range(min, max)]


def getTimeBinned(input_date): #example # input_date = '17:40'
    
    #create var of time_bin
    date_dt = datetime.datetime.strptime(input_date,'%H:%M')
    hours_input = str(date_dt.hour)

    model_hour_input = f'{hours_input:02}:00 - {hours_input:02}:59'
    label_hour_list = get_hours_label(0,24)

    # #create dict hour_bin
    Dict_hourBin ={}

    for label in label_hour_list:
        if label == model_hour_input:
            Dict_hourBin[label] =1
        else:
            Dict_hourBin[label] = 0
    return Dict_hourBin

def getWeekDay(input_date): # example  input_date = '2022-12-30'

    #convert data to dt type
    date_time_obj = datetime.datetime.strptime(input_date, '%Y-%m-%d')

    #create var of day of week for model
    day_of_week  = date_time_obj.weekday()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    model_weekDay_input = day_names[day_of_week]

    #create dict
    dict_weekday ={}

    for every_day in day_names:
        if every_day == model_weekDay_input:
            dict_weekday[every_day] =1
        else:
            dict_weekday[every_day] = 0

    return dict_weekday


def getWeather_Format_unix():

    # Manhattan coordinates
    lat =  40.7834
    lon = -73.9662

    api_key = "9bbe29045340e664d456449c4584d432"

    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid={api_key}"


    response = requests.get(url)
    Raw_Weather_Data = response.json()

    return Raw_Weather_Data

def Convert_DT_To_unix_timestamp(date_request): #convert  '%Y-%m-%d %H:%M:%S to timestamp
    """Receiving the client's time and date data is in the form
    '%Y-%m-%d %H:%M:%S
     And this data is converted to the same type
    as the ones in the API which are timestamped
    """""
    date_time_obj = datetime.datetime.strptime(date_request, '%Y-%m-%d %H:%M:%S')
    unix_timestamp = date_time_obj.timestamp()
    Customer_unix_timestamp = int(unix_timestamp)
    return Customer_unix_timestamp 

def kelvin_to_fahrenheit(temp_kelvin):
    #The API temperature data is in Kelvin 
    #and the temperature data in our model is in Fahrenheit
  temp_fahrenheit = 9/5 * (temp_kelvin - 273) + 32
  return temp_fahrenheit


def getWeather(data_client):
    """"Takes time and date data from the client like
    '2022-12-30 21:00:00'   
    and returns the weather data to the model"""

    weather_data_API = getWeather_Format_unix()

    ## data_client = '2022-12-31 22:00:00' --  example
    dt_API = Convert_DT_To_unix_timestamp(data_client) 


    # Variables for CDD calculation
    cdd_total = 0



    data = weather_data_API['hourly']
    result = [hourly_data for hourly_data in data if hourly_data['dt'] == dt_API]
    if result:
        # calculate Tavg
        TempAvg_kelvin = ((result[0]["temp"] + result[0]["feels_like"]) / 2)
        TempAvg_f = kelvin_to_fahrenheit(TempAvg_kelvin)

        # Tdep
        Tdep =0

        # calculate CDD
        temperature = result[0]["temp"]
        temperature_fahrenheit = kelvin_to_fahrenheit(temperature)
        threshold_temperature_f = 70 # threshold temperature in Fahrenheit
        cdd = temperature_fahrenheit - threshold_temperature_f
        if cdd > 0:
            cdd_total += cdd
        
        # retrieve rain 1h
        if 'rain' in result:
          rain = result[0]["rain"]["1h"]
        else:
         rain =0

        # retrieve snow 1h
        if 'snow' in result:
            new_snow = result[0]["snow"]["1h"] 
            snow_dep = result[0]["snow"]["1h"] 
        else:
            new_snow , snow_dep = 0 , 0
            
    return {
        'Tavg':TempAvg_f,
        'Tdep':Tdep,
        'CDD':cdd_total,
        'Precipitation':rain,
        'new_snow':new_snow,
        'snow_depth':snow_dep}

zones_to_name_dict={
    "Inwood": [153, 128, 127],
    "Washington Heights": [120, 244],
    "Hamilton Heights": [116, 152],
    "Central Harlem": [42, 41],
    "Morningside Heights": [166],
    "Upper West Side": [24, 151, 238, 239, 143, 142],
    "Central Park": [43],
    "Spanish Harlem": [74, 75],
    "Randall's Island": [194],
    "Upper East Side": [236, 263, 262, 237, 141, 140],
    "Roosevelt Island": [202],
    "Midtown West": [50, 48, 163, 230, 161, 100, 164],
    "Midtown East": [170, 162, 229, 233, 170],
    "Kips Bay": [137],
    "Stuyvesant Town": [224],
    "Chelsea": [246, 68, 90],
    "Flatiron District": [186],
    "West Village": [158, 249],
    "Greenwich Village": [113, 114],
    "East Village": [79, 4],
    "Soho": [125, 221, 144],
    "Lower East Side": [148, 232],
    "Tribeca": [231],
    "Two Bridges": [45],
    "Battery Park City": [13, 12],
    "Financial District": [209, 261, 87, 88, 12]
}
def ListZonesNames (): #############################################################
    
    name_list =[]
    for name in zones_to_name_dict.keys():
            name_list.append(name)
    return name_list




def getZones(list_zone_names): #input string on zone_names example zone_list["Inwood"]
    # list_zone_names = ["Tribeca","Two Bridges"]
    new_dict_int = {}
    new_dict_string ={}
    
    # fill with 1 the user zones
    for name in list_zone_names:
        if name in zones_to_name_dict:
            for value in zones_to_name_dict[name]:
                new_dict_int[value] = 1

    
    # #convert dtypes keys from int to string
    for key, value in new_dict_int.items():
        new_key = str(key)
        new_dict_string[new_key] = value
    
    return new_dict_string  # {153: 1, 128: 1, 127: 1}

def load_saved_artifacts():
    global Tdep
    global TempAvg_f
    global cdd_total
    global rain
    global new_snow
    global snow_dep
    # global __locations
    # __locations =ListZonesNames()##################################################################
    

    print("loading saved artifacts......done ")

if __name__ == "__main__":
    load_saved_artifacts()

