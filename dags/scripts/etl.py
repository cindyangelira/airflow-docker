import os
import pandas as pd
import warnings # built in library
import glob
import xml.etree.ElementTree as ET
import datetime as dt
from detect_delimiter import detect
warnings.filterwarnings('ignore')

# asumsikan kita start dari baca path data yg sudah di unzip
# extract csv
def extract_csv(file_path:str):
    with open(file_path, 'r') as file:
        header = file.readline()
        delim = detect(header)
        
    # path = lokasi file berada
    df = pd.read_csv(file_path, sep = delim) # dengan adjusted delimeter yg sesuai dengan hasil deteksi delimeter
    return df

# extract json
def extract_json(file_path:str):
    df = pd.read_json(file_path, lines = True)
    return df

# extract xml
# define list of variable
def extract_xml(file_path:str):
    # define dctionary yg berisi nama kolom yg akan digunakan
    dic = {
        'name' : [],
        'height' : [],
        'weight' : []
    }
    # parsing xml dulu, untuk mendapatkan root 
    tree = ET.parse(file_path)
    root = tree.getroot()

    # looping to get value person dari root
    for person in root:
        name = person.find('name').text
        height = float(person.find('height').text)
        weight = float(person.find('weight').text)

        # Append valu ini ke dictionary
        dic['name'].append(name)
        dic['height'].append(height)
        dic['weight'].append(weight)

    # convert ke dataframe
    df = pd.DataFrame(dic)
    
    return df

# wrap it up
def extract(file_path:str, destination_path:str):
    # gunakan support .glob karena kita akan automatically detect delimeter
    # definisikan dataframe
    data = pd.DataFrame(columns = ['name', 'height','weight', 'source'])

    # looping apply fungsi extract_csv
    print('Get Data From csv type')
    for csv_file in glob.glob(f'{file_path}/*.csv'):
        df = pd.DataFrame(extract_csv(csv_file))
        df['source'] = 'csv'
        data = pd.concat([data, df], ignore_index = True)


    # apply fungsi extract_json
    print('Get Data From json type')
    for json_file in glob.glob(f'{file_path}/*.json'):
        df = pd.DataFrame(extract_json(json_file))
        df['source'] = 'json'
        data = pd.concat([data, df], ignore_index = True)

    # apply fungsi extract_xml
    print('Get Data From xml type')
    for xml_file in glob.glob(f'{file_path}/*.xml'):
        df = pd.DataFrame(extract_xml(xml_file))
        df['source'] = 'xml'
        data = pd.concat([data, df], ignore_index = True)
    print('Data is already extracted')
    
    # save to csv
    if not os.path.exists(destination_path):
        os.makedirs(destination_path) # if not exists, then create the folder
    data.to_csv(f"{destination_path}/raw.csv", index= False)  

# transform data
def load(file_path, destination_path):
    data = pd.read_csv(file_path)
    print('Transformed Data')
    # rename variable
    data = data.rename(columns = {
        "weight" : "height",
        "height" : "weight"})

    # convert height to meter
    data['height'] = round(data.height / 100, 2)

    # create new column
    data['timestamps'] = dt.datetime.now()
    data['is_obesitas'] = [True if i > 70 else False for i in data['weight']]

    # save to csv
    if not os.path.exists(destination_path):
        os.makedirs(destination_path) # if not exists, then create the folder
    data.to_csv(f"{destination_path}/clean.csv", index= False)    

# create log
def log_process(messages:str):
    time_format = "%Y-%m-%d %H:%M:%S"
    time_now = dt.datetime.now()
    time_now_str = time_now.strftime(time_format)
    # write log to .txt file
    with open("log.txt", 'a') as f:
        f.write(time_now_str + "," + messages + "\n") # append by new line
