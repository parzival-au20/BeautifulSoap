import threading
import time
from AinOnline import fetch_ainonline_news
from AirportHaber import fetch_airporthaber_news
from AIAA import fetch_AIAA_news
from AirlineHaber import fetch_Airline_news
from AirTurkHaber import fetch_AirTurk_news
from BellFlight import fetch_BellFlight_news
from DefenceNews import fetch_DefenceNews_news
from DefenceWeb import fetch_DefenceWeb_news
from Enstrom import fetch_Enstrom_news
from GEAerospace import fetch_GEAerospace_news
from HelicopterInvestor import fetch_HelicopterInvestor_news
from MDHelicopters import fetch_MDHelicopters_news
from Robinson import fetch_Robinson_news
from TheWarzone import fetch_TheWarzone_news
from TurDef import fetch_TurDef_news
from VerticalMag import fetch_VerticalMag_news
from airbuscorporatehelicopters import fetch_Airbus_news
from DefenceTurk import fetch_DefenceTurk_news
from DefenceTurkey import fetch_DefenceTurkey_news
from SavunmaSanayist import fetch_SavunmaSanayist_news
from RotorAndWing import fetch_RotorAndWing_news
from lockheedmartin import fetch_lockheedmartin_news
from HeliHub import fetch_HeliHub_news
from Leonardo import fetch_Leanardo_news
from JustHelicopters import fetch_JustHelicopters_news
from AirNewsTimes import fetch_AirNewsTimes_news
from DefenseHere import fetch_DefenseHere_news

news_fetch_functions = [
    fetch_HelicopterInvestor_news,
    fetch_Airbus_news,
    fetch_BellFlight_news,
    fetch_DefenceNews_news,
    fetch_Enstrom_news,
    fetch_GEAerospace_news,
    fetch_AirTurk_news,
    fetch_VerticalMag_news,
    fetch_JustHelicopters_news,
    fetch_Leanardo_news,
    fetch_HeliHub_news,
    fetch_lockheedmartin_news,
    fetch_Robinson_news,
    fetch_RotorAndWing_news,
    fetch_TheWarzone_news,
    fetch_DefenceTurk_news,
    
    fetch_SavunmaSanayist_news,
    fetch_TurDef_news,
    fetch_Airline_news,
    fetch_airporthaber_news,
    fetch_DefenceTurkey_news,
    fetch_AirNewsTimes_news,
    fetch_AIAA_news,
    fetch_MDHelicopters_news,
    fetch_ainonline_news,
    fetch_DefenceWeb_news,
    # fetch_DefenseHere_news,  # Sayfa dinamik ve geç yüklendiği için beklemesi gerekiyor çözüm aranacak.
]

start_time = time.time()
threads = []

for fetch_function in news_fetch_functions:
    thread = threading.Thread(target=fetch_function)
    threads.append(thread)
    thread.start()

# Tüm iş parçacıklarının bitmesini bekleyelim
for thread in threads:
    thread.join()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"İşlem {elapsed_time} saniye sürdü")
print("Haberler başarıyla çekildi.")
