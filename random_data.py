import csv, util, os, pandas as pd
from faker import Faker

# Definicion de Carpetas
dir_path = os.path.dirname(__file__)
dir_in = os.path.join(dir_path,"input")
dir_out = os.path.join(dir_path,"output")
dir_log = os.path.join(dir_path,"log")
util.create_folder_env(dir_path)

csv_columns = ['Title', 'First name', 'Last name', 'Email', 'Password',
            'Date of Birth', 'Company', 'Address', 'Address (Line 2)',
            'City', 'State','Zip/Postal Code','Country','Additional information',
            'Home phone','Mobile phone','Assign an address alias for future reference'
            ]

fake = Faker()
country = fake.country()
data=[]
# United states
for i in range(3):
    os.F_OK
    new_row = {'Title':fake.prefix(), 'First name': fake.first_name(), 'Last name': fake.last_name(), 'Email':fake.email(), 
           'Password':"Passw@rd", 'Date of Birth': fake.date_of_birth(), 'Company': fake.company(), 'Address': fake.address(), 
           'Address (Line 2)': fake.street_address() ,'City': fake.city(), 'State':fake.state(),'Zip/Postal Code': fake.postcode(),
           'Country': 'United States', 'Additional information':fake.street_address(),
           'Home phone': fake.msisdn() ,'Mobile phone': fake.msisdn(),
           'Assign an address alias for future reference':fake.address().replace('\n',' ') }
    
    data.append(new_row)


csv_file = os.path.join(dir_in,"mockup.xlsx")
df = pd.DataFrame(data, columns=csv_columns)    
df.to_excel(csv_file, index=None)




