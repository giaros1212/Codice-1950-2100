import os
import glob
import logging
import xarray as xr

# ==============================================================================
# CONFIGURAZIONE LOGGING
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ==============================================================================
# 1. PARAMETRI E DIRECTORY PRINCIPALI
# ==============================================================================
DIR_OUTPUT = "/storage/local/home/georm3/mlpetitta/dati_geophys/LAUREE/GROSSINI"
DIR_MODELLO_BASE = "/storage/local/home/georm3/mlpetitta/dati_geophys/NASA_NEX/NEX_GDDP_CMIP6/ACCESS-ESM1-5"
NOME_MODELLO = "ACCESS-ESM1-5"

os.makedirs(DIR_OUTPUT, exist_ok=True)
logging.info(f"Directory di output pronta: {DIR_OUTPUT}")

# ==============================================================================
# 2. DIZIONARIO COMPLETO (60 AEROPORTI)
# ==============================================================================
airports = {
    # EUROPA
    'EBBR': {'nome': 'Brussels Airport', 'lat': 50.9014, 'lon': 4.4844},
    'EDDF': {'nome': 'Frankfurt Airport', 'lat': 50.0333, 'lon': 8.5706},
    'EDDL': {'nome': 'Dusseldorf Airport', 'lat': 51.2895, 'lon': 6.7668},
    'EDDM': {'nome': 'Munich Airport', 'lat': 48.3538, 'lon': 11.7861},
    'EGKK': {'nome': 'Gatwick Airport', 'lat': 51.1481, 'lon': -0.1903},
    'EGLC': {'nome': 'London City Airport', 'lat': 51.5053, 'lon': 0.0553},
    'EGLL': {'nome': 'Heathrow Airport', 'lat': 51.4700, 'lon': -0.4543},
    'EHAM': {'nome': 'Amsterdam Airport Schiphol', 'lat': 52.3105, 'lon': 4.7683},
    'EIDW': {'nome': 'Dublin Airport', 'lat': 53.4264, 'lon': -6.2499},
    'EKCH': {'nome': 'Copenhagen Airport', 'lat': 55.6180, 'lon': 12.6560},
    'ENGM': {'nome': 'Oslo Airport', 'lat': 60.1939, 'lon': 11.1004},
    'ESSA': {'nome': 'Stockholm Arlanda Airport', 'lat': 59.6519, 'lon': 17.9186},
    'LEBL': {'nome': 'Barcelona El Prat Airport', 'lat': 41.2974, 'lon': 2.0833},
    'LEMD': {'nome': 'Adolfo Suarez Madrid-Barajas', 'lat': 40.4839, 'lon': -3.5680},
    'LEPA': {'nome': 'Palma de Mallorca Airport', 'lat': 39.5517, 'lon': 2.7388},
    'LESO': {'nome': 'San Sebastian Airport', 'lat': 43.3565, 'lon': -1.7906},
    'LFPG': {'nome': 'Paris Charles de Gaulle', 'lat': 49.0097, 'lon': 2.5479},
    'LFPO': {'nome': 'Paris Orly General Airport', 'lat': 48.7262, 'lon': 2.3652},
    'LGAV': {'nome': 'Athens International Airport', 'lat': 37.9364, 'lon': 23.9445},
    'LGHI': {'nome': 'Chios Island National Airport', 'lat': 38.3432, 'lon': 26.1406},
    'LICG': {'nome': 'Pantelleria Airport', 'lat': 36.8167, 'lon': 11.9689},
    'LIMC': {'nome': 'Milan-Malpensa Airport', 'lat': 45.6301, 'lon': 8.7255},
    'LIRF': {'nome': 'Rome-Fiumicino International', 'lat': 41.7999, 'lon': 12.2462},
    'LIRV': {'nome': 'Ciampino Airport', 'lat': 41.7994, 'lon': 12.5949},
    'LOWW': {'nome': 'Vienna International Airport', 'lat': 48.1103, 'lon': 16.5697},
    'LPPT': {'nome': 'Lisbon Portela Airport', 'lat': 38.7742, 'lon': -9.1342},
    'LSZH': {'nome': 'Zurich Airport', 'lat': 47.4582, 'lon': 8.5555},
    'LTAI': {'nome': 'Antalya Airport', 'lat': 36.8987, 'lon': 30.8005},
    'LTFJ': {'nome': 'Sabiha Gokcen International', 'lat': 40.8986, 'lon': 29.3092},
    'LTFM': {'nome': 'Istanbul Ataturk Airport', 'lat': 41.2622, 'lon': 28.7420},
    # NORD AMERICA
    'KATL': {'nome': 'Hartsfield-Jackson Atlanta', 'lat': 33.6407, 'lon': -84.4277},
    'KDFW': {'nome': 'Dallas/Fort Worth', 'lat': 32.8998, 'lon': -97.0403},
    'KDEN': {'nome': 'Denver International', 'lat': 39.8561, 'lon': -104.6737},
    'KORD': {'nome': 'Chicago O\'Hare', 'lat': 41.9742, 'lon': -87.9073},
    'KLAX': {'nome': 'Los Angeles International', 'lat': 33.9416, 'lon': -118.4085},
    'KJFK': {'nome': 'John F. Kennedy International', 'lat': 40.6413, 'lon': -73.7781},
    'KMCO': {'nome': 'Orlando International', 'lat': 28.4312, 'lon': -81.3081},
    'KMIA': {'nome': 'Miami International', 'lat': 25.7959, 'lon': -80.2870},
    'KLAS': {'nome': 'Harry Reid International', 'lat': 36.0840, 'lon': -115.1537},
    'KCLT': {'nome': 'Charlotte Douglas', 'lat': 35.2140, 'lon': -80.9431},
    'KSEA': {'nome': 'Seattle-Tacoma International', 'lat': 47.4502, 'lon': -122.3088},
    'KSFO': {'nome': 'San Francisco International', 'lat': 37.6213, 'lon': -122.3790},
    'KPHX': {'nome': 'Phoenix Sky Harbor', 'lat': 33.4352, 'lon': -112.0101},
    'KIAH': {'nome': 'George Bush Intercontinental', 'lat': 29.9902, 'lon': -95.3368},
    'KBOS': {'nome': 'Boston Logan International', 'lat': 42.3656, 'lon': -71.0096},
    'KEWR': {'nome': 'Newark Liberty International', 'lat': 40.6895, 'lon': -74.1745},
    'KMSP': {'nome': 'Minneapolis-St. Paul', 'lat': 44.8848, 'lon': -93.2223},
    'KDTW': {'nome': 'Detroit Metropolitan', 'lat': 42.2121, 'lon': -83.3488},
    'KPHL': {'nome': 'Philadelphia International', 'lat': 39.8729, 'lon': -75.2437},
    'KSLC': {'nome': 'Salt Lake City International', 'lat': 40.7899, 'lon': -111.9791},
    'KIAD': {'nome': 'Washington Dulles', 'lat': 38.9531, 'lon': -77.4565},
    'PANC': {'nome': 'Ted Stevens Anchorage', 'lat': 61.1759, 'lon': -149.9901},
    'CYYZ': {'nome': 'Toronto Pearson', 'lat': 43.6777, 'lon': -79.6248},
    'CYVR': {'nome': 'Vancouver International', 'lat': 49.1939, 'lon': -123.1844},
    'CYUL': {'nome': 'Montréal-Trudeau', 'lat': 45.4706, 'lon': -73.7408},
    'CYYC': {'nome': 'Calgary International', 'lat': 51.1215, 'lon': -114.0076},
    'CYHZ': {'nome': 'Halifax Stanfield', 'lat': 44.8808, 'lon': -63.5086},
    'MMMX': {'nome': 'Benito Juárez International', 'lat': 19.4361, 'lon': -99.0719},
    'MMUN': {'nome': 'Cancún International', 'lat': 21.0365, 'lon': -86.8771},
    'MMGL': {'nome': 'Miguel Hidalgo y Costilla', 'lat': 20.5218, 'lon': -103.3112}
}

# ==============================================================================
# FUNZIONI DI SUPPORTO
# ==============================================================================
def trova_cartella_run(percorso_base):
    try:
        if not os.path.exists(percorso_base):
            return None
        cartelle = [d for d in os.listdir(percorso_base) if os.path.isdir(os.path.join(percorso_base, d))]
        run_dirs = [d for d in cartelle if d.startswith('r')]
        
        if not run_dirs:
            logging.error(f"Nessuna cartella di tipo 'r1i1...' trovata in {percorso_base}")
            return None
        return run_dirs[0]
    except Exception as e:
        logging.error(f"Errore nella ricerca cartella run in {percorso_base}: {e}")
        return None

# ==============================================================================
# FASE 1: ESTRAZIONE
# ==============================================================================
def fase1_estrazione(dir_modello_base, nome_modello):
    logging.info(f"--- FASE 1: Estrazione annuale ({nome_modello}) ---")
    scenari = ['historical', 'ssp585']
    
    for scenario in scenari:
        percorso_scenario = os.path.join(dir_modello_base, scenario)
        
        cartella_run = trova_cartella_run(percorso_scenario)
        if not cartella_run:
            continue
            
        percorso_run = os.path.join(percorso_scenario, cartella_run)
        
        pattern_ricerca = os.path.join(percorso_run, '**', 'tasmax*.nc')
        files_nc = sorted(glob.glob(pattern_ricerca, recursive=True))
        
        if len(files_nc) == 0:
            logging.warning(f"Nessun file tasmax*.nc trovato dentro {percorso_run} o sottocartelle.")
            continue
            
        logging.info(f"Trovati {len(files_nc)} file per {nome_modello} - {scenario}.")
        
        for file_in in files_nc:
            nome_file_base = os.path.basename(file_in)
            try:
                anno = nome_file_base.split('_')[-1].replace('.nc', '')
            except Exception:
                anno = "YYYY"
                
            try:
                ds = xr.open_dataset(file_in)
                var_name = 'tasmax' if 'tasmax' in ds.data_vars else 't2m'
                
                # Controllo robusto sulla longitudine massima (estratto come valore numerico reale)
                is_grid_360 = ds['lon'].max().item() > 180
                
                for icao, info in airports.items():
                    lat_apt = info['lat']
                    lon_apt = info['lon']
                    
                    lon_model = lon_apt
                    if lon_apt < 0 and is_grid_360:
                        lon_model = 360 + lon_apt
                        
                    da_local = ds[var_name].sel(lat=lat_apt, lon=lon_model, method='nearest')
                    ds_out = da_local.to_dataset(name='tasmax')
                    
                    nome_out = f"{icao}_{nome_modello}_{anno}_{scenario}.nc"
                    path_out = os.path.join(DIR_OUTPUT, nome_out)
                    
                    ds_out.to_netcdf(path_out)
                    
                ds.close()
            except Exception as e:
                logging.error(f"Errore fatale processando {nome_file_base}: {e}")

# ==============================================================================
# FASE 2: MERGING
# ==============================================================================
def fase2_merging(nome_modello):
    logging.info(f"--- FASE 2: Merging dei file ({nome_modello}) ---")
    scenari = ['historical', 'ssp585']
    
    for icao in airports.keys():
        for scenario in scenari:
            pattern = os.path.join(DIR_OUTPUT, f"{icao}_{nome_modello}_*_{scenario}.nc")
            files_aeroporto = sorted(glob.glob(pattern))
            
            if not files_aeroporto:
                continue
                
            try:
                # Merging robusto basato sulla dimensione temporale e tollerante alle coordinate spaziali
                ds_merged = xr.open_mfdataset(
                    files_aeroporto, 
                    combine='nested', 
                    concat_dim='time', 
                    coords='minimal', 
                    compat='override'
                )
                
                nome_merged = f"{icao}_{nome_modello}_{scenario}_COMPLETO.nc"
                path_merged = os.path.join(DIR_OUTPUT, nome_merged)
                
                ds_merged.to_netcdf(path_merged)
                ds_merged.close()
                logging.info(f"Master salvato: {nome_merged}")
                
            except Exception as e:
                logging.error(f"Errore nell'unione dei file per {icao} ({scenario}): {e}")

# ==============================================================================
# ESECUZIONE MAIN 
# ==============================================================================
if __name__ == '__main__':
    logging.info("**************************************************")
    logging.info("AVVIO JOB ESTRAZIONE")
    logging.info("**************************************************")
    
    if not os.path.exists(DIR_MODELLO_BASE):
        logging.error(f"ATTENZIONE: La directory del modello non esiste! ({DIR_MODELLO_BASE})")
    else:
        fase1_estrazione(DIR_MODELLO_BASE, NOME_MODELLO)
        fase2_merging(NOME_MODELLO)
            
    logging.info("**************************************************")
    logging.info("JOB COMPLETATO CON SUCCESSO")
    logging.info("**************************************************")
