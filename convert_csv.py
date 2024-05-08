import pandas as pd
import os
import time
import datetime
import locale
import logging

formatType={'VerticalMag':['%B %d, %Y',"english"],
                         'AIAA':['%d %B %Y','english'], 
                         'Airbus':['%d %B %Y','english'], 
                         'AinOnline':['%B %d, %Y',"english"],
                         'AirlineHaber':['%d %B %Y, %H:%M',"turkish"], 
                         'AirNewsTimes':['%d %B %Y',"turkish"], 
                         'AirportHaber':['%d %B %Y, %A %H:%M:%S',"turkish"], 
                         'AirTurkHaber':['%d %B %Y',"turkish"], 
                         'BellFlight':['%d %B %Y','english'], 
                         'DefenseHere':['%d.%m.%Y',"turkish"], 
                         'DefenceNews':['%B %d, %Y','english'], 
                         'DefenceTurk':['%d %b %Y %H:%M','turkish'],
                         'DefenceTurkey':['%d %B, %Y','turkish'],
                         'DefenceWeb':['%d %B %Y','english'], 
                         'Enstrom':['%B %d, %Y','english'], 
                         'FlightGlobal':['%d %B %Y','english'], 
                         'GEAerospace':['%B %d, %Y','english'], 
                         'HeliHub':['%d-%b-%Y','english'],
                         'helicoptersmagazine':['%B %d, %Y','english'],
                         'HelicopterInvestor':['%d %B %Y','english'], 
                         'JustHelicopters':['%d.%m.%Y',"english"],
                         'Leonardo':['%d %B %Y','english'],
                         'lockheedmartin':['%b %d, %Y','english'],
                         'MDHelicopters':['%B %d, %Y','english'], 
                         'Robinson':['%d %m, %Y','english'], 
                         'RotorAndWing':['%B %d, %Y','english'],
                         'SavunmaSanayist':['%d %B %Y',"turkish"],
                         'TheWarzone':['%b %d, %Y','english'], 
                         'TurDef':['%d %b %Y','english'], 
                         }

default_format_type="%d.%m.%Y"
save_date_file_loc=".\\WebSiteDates"

def save_to_csv(data,fileName):
    
    # Kolon başlıkları
    column_headers = ["Url","category","image","text","timestamp","title","web_site_name"]

    # DataFrame oluşturma
    df = pd.DataFrame(data, columns=column_headers)
    # DataFrame'i CSV dosyasına kaydetme
    #df.to_csv(f"{fileName}-{file_number}.csv", index=False)
    while True: 
        file_number=0
        if not os.path.exists(f"./{fileName}-{file_number}"):

            df.to_csv(f"./{fileName}-{file_number}.csv",index=False,sep="½",encoding='utf-8-sig',)
            write_date(date_to_text(datetime.datetime.today(),fileName),fileName)
            break
        else:
            file_number=file_number+1
    print(f"{fileName} adlı CSV dosyası oluşturuldu.")
    logging.info(f"{fileName} adlı CSV dosyası oluşturuldu.")

def date_to_text(date,web_site_name):
        locale.setlocale(locale.LC_ALL,formatType[f'{web_site_name}'][1])
        return date.strftime("%d.%m.%Y")
    
def read_date(web_site_name):
    lines=""
    with open(save_date_file_loc+f'\\{web_site_name}.txt') as f:
        lines = f.readlines()
    return lines[0]

def write_date(date,web_site_name):
    if(os.path.exists(save_date_file_loc+f"\\{web_site_name}.txt")):
        with open(save_date_file_loc+f"\\{web_site_name}.txt", "w") as f:
            f.write(date)
    else:
        write_date(datetime.datetime.today().strptime(read_date(web_site_name),default_format_type))
  
      
def text_to_date(text,web_site_name):
    try:
        locale.setlocale(locale.LC_ALL,formatType[f'{web_site_name}'][1])
        return datetime.datetime.strptime(text,formatType[f'{web_site_name}'][0])
    
    except Exception as e:
        print(e)
        logging.error(e)
        return datetime.datetime(1970, 1, 1)
        
def to_default_date(text, web_site_name):
    try:
        locale.setlocale(locale.LC_ALL,formatType[f'{web_site_name}'][1])
        return datetime.datetime.strptime(text,default_format_type)
    
    except Exception as e:
        print(e)
        logging.error(e)
        return datetime.datetime()
        

def control_text_by(date, web_site_name):
    
    if(os.path.exists(save_date_file_loc+f"\\{web_site_name}.txt")):
        locale.setlocale(locale.LC_ALL,formatType[f'{web_site_name}'][1])
        file_date=datetime.datetime.strptime(read_date(web_site_name), default_format_type)
        scraping_date=datetime.datetime.today()
        date=text_to_date(date, web_site_name)
        
        if(file_date <= date and date <= scraping_date):
            return True
        else:
            return False
    else:
        write_date(datetime.datetime.today().strptime(read_date(web_site_name), default_format_type))
        return "writing"

def Content_Text_Control(news_date, news_text, web_site_name):
    if(control_text_by(news_date, web_site_name)==True or control_text_by(news_date, web_site_name)=="writing"):
        if(news_text.lower().find("helicopter")!=-1 or news_text.lower().find("helikopter")!=-1):
            return True
        else:
            return False
    else:
        return False
