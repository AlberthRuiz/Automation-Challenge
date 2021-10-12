import platform,os, logging ,pandas as pd, time, sys
import util
from selenium_layer import SeleniumLayer 
from datetime import datetime

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
file_log=os.path.join(dir_log,'taks_1_' + today_line + ".log")
log=util.config_logging( file_log, logging.DEBUG, True)

se = SeleniumLayer(log, dir_in, dir_path, dir_out)


# Lectura de informacion mockup
df = pd.read_excel(file_mockup, index_col=None)
df.fillna('', inplace=True)

def sing_in_usuario():
    log.debug('Sing in')
    se.click_visible_element_by_xpath("//*[contains(text(),'Sign in')]")

def sing_out_usuario():
    log.debug('Sign out')
    se.click_visible_element_by_xpath("//*[contains(text(),'Sign out')]")


def registrar_nuevo_usuario(data):    
    log.debug('Writing Mail ' + data['Email'])    
    se.clear_visible_element_by_id("email_create")
    se.send_key_visible_element_by_id("email_create",data['Email'])

    log.debug('Click en Create Account')
    se.click_visible_element_by_id('SubmitCreate')    
    time.sleep(4)

    if se.check_exists_visible_element_by_id('create_account_error'):
        raise Exception (data['Email'] + 'has already been registered')

    log.debug('Select Title')
    if (data['Title'] =='Mr.'):
        se.click_located_element_id('id_gender1')
    elif (data['Title'] =='Mrs.'):
        se.click_located_element_id('id_gender2')
    
    log.debug('Wrting Personal information')
    se.send_key_visible_element_by_id('customer_firstname',data['First name'])
    se.send_key_visible_element_by_id('customer_lastname', data['Last name'])
    se.send_key_located_element_by_id('passwd',data['Password'])
    

    date_birth= datetime.strptime(str(data['Date of Birth']), '%Y-%m-%d  %H:%M:%S')
    se.select_by_value_located_by_id('days',str(date_birth.day))
    se.select_by_value_located_by_id('months',str(date_birth.month))
    se.select_by_value_located_by_id('years',str(date_birth.year))
    
    log.debug('Wrting your address')
    se.send_key_visible_element_by_id('company', data['Company'])
    se.send_key_visible_element_by_id('city', data['City'])    
    se.send_key_located_element_by_id('id_country',data['Country'])
    se.send_key_located_element_by_id('id_state',data['State'])
    
    se.send_key_located_element_by_id('postcode',str(data['Zip/Postal Code']).zfill(5))
    se.send_key_located_element_by_id('phone', data['Mobile phone'])

    se.send_key_located_element_by_id('phone_mobile',data['Mobile phone'])
    se.send_key_located_element_by_id('other',data['Assign an address alias for future reference'])


    if str(data['Address (Line 2)']).strip() !='':
        se.send_key_visible_element_by_id('address2',data['Address (Line 2)'])
        
    se.send_key_visible_element_by_id('address1',data['Address'])

    



def main():
    se.iniciar_driver_chrome()
    se.navegar_url_chrome("http://automationpractice.com/")
    sing_in_usuario()
    for id, fila in df.iterrows():
        try:
            log.debug('Fill infomration '+ str(fila))
            registrar_nuevo_usuario(fila)            
            sing_out_usuario()
            log.debug('OK')
        except Exception as e:
            log.error(str(e) , exc_info=True)    
    se.quit_driver_chrome()


main()    
