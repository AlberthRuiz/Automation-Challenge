import requests, os,  util, logging, pandas as pd, json
from faker import Faker
from requests.models import Response
from datetime import datetime 

API_KEY = '077a3e545585d4fe7693e3bfb78c96ee'
API_URL = 'http://api.countrylayer.com/v2/'
URL_CODE = 'alpha/{code}'
COUNTRY = ['US','DE','GB']

# Definicion de Carpetas
dir_path = os.path.dirname(__file__)
dir_in = os.path.join(dir_path,"input")
dir_out = os.path.join(dir_path,"output")
dir_log = os.path.join(dir_path,"log")
util.create_folder_env(dir_path)

# Definicion de Variables
today = datetime.now()
today_line=str(today.strftime("%Y%m%d%H%M%S"))
today_format=str(today.strftime("%d/%m/%Y %H:%M:%S"))
today_date = str(today.strftime("%d/%m/%Y"))
file_mockup = os.path.join(dir_in,'mockup.xlsx')

# Loggin file 
file_log=os.path.join(dir_log,"task_2_" + today_line + ".log")
log=util.config_logging( file_log, logging.DEBUG, True)



def get_countr_info(url, code):
    log.debug('Request to url ->'+ url)
    response = requests.get(url)
    if response.status_code == 200: 
        log.debug(response.text)
        df = pd.DataFrame.from_dict(json.loads(response.text), orient="index")        
        with open(os.path.join(dir_out,code+'_response.txt'),'+w') as f:
            f.write(str(df))

    elif response.status_code == 101: 
        log.error('invalid_access_key - No API Key was specified or an invalid API Key was specified.')
    elif response.status_code == 103:
        log.error('invalid_api_function - The requested API endpoint does not exist.')
    elif response.status_code == 104: 
        log.error('usage_limit_reached - The maximum allowed API amount of monthly API requests has been reached.')

def post_info(data):
    url= API_URL+URL_CODE.replace('{code}','postmethod')+'?access_key='+API_KEY
    response = requests.post(url, data=data)
    if response.status_code == 200: 
        log.debug(response.text)
    elif response.status_code == 101: 
        log.error('invalid_access_key - No API Key was specified or an invalid API Key was specified.')
    elif response.status_code == 103:
        log.error('invalid_api_function - The requested API endpoint does not exist.')
    elif response.status_code == 104: 
        log.error('usage_limit_reached - The maximum allowed API amount of monthly API requests has been reached.')
    elif response.status_code == 500:
        log.error(response.text)


def main():    
    #Get information from countries
    for item in COUNTRY:
        log.debug('Code country ->'+ item)
        url= API_URL+URL_CODE.replace('{code}',item)+'?access_key='+API_KEY
        get_countr_info(url,item)
    
    #Post country information 
    fake = Faker()
    for i in range(3):
        country = fake.country()
        log.debug('post country ->'+country )
        data =  { 'name': country , 'alpha2_code': fake.country_code(), 'alpha3_code': fake.postcode() }
        post_info(data)

 
    


main()
