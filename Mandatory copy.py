# Vi henter vores værktøjer der skal bruges, csv og json 
# CSV = Comma-Separated Values
# Simpelt tekstformat til tabeller; værdier adskilles
# JSON = JavaScript Object Notation
# tekstformat til strukturerede/hierarkiske data
import json 
import csv 

try: 
    # Her åbner vi json filen, for at aflæse inholdet 
    with open("incident1.json", "r") as file:
# Aflæser hele json filen, og laver den om til python-data (dict/lister)
        incident_data  = json.load(file)
# Dykker ind i dataen, for at finde præcis de alerts vi søger
        alerts = incident_data.get("alerts")
except: 
    print("fil ikke fundet")
    exit() 
# Headers navne til csv filen, de sidste her hører ind under entities 
domain_headers = ["alertID", "machineId", "firstActivity", "domains"]
hashes_headers = ["alertID", "machineId", "firstActivity", "fileHashes"]
ips_headers = ["alertID", "machineId", "firstActivity", "ips"]
processes_headers = ["alertID", "machineId", "firstActivity", "processes"]

# Funktion som gemmer data i en CSV-fil med de kolonner du giver ("headers") og det filnavn du angiver ("file_name")
def json_to_csv(headers, file_name):
# Åbner Csvfilen, så vi kan tilskrive i den, vi bruger newline til undgå tomme linjer med gapes i mellem coderne i csvfilen
    # print(f'I will do {headers}, {file_name}')
    # print(f'alerts at the begining {alerts}')
    with open(file_name, "w", newline="") as file:
# Starter række skrivningen i csvfilen
        csv_writer = csv.writer(file)
# Indskriver headernes 
        csv_writer.writerow(headers) 
# Henter de 3 første headers alertId, machineId og firstActivity 
        for alert in alerts: 
            alertId = alert.get("alertId")
            machineId = alert.get("machineId")
            firstActivity = alert.get("firstActivity")
            # Kigger ind i entities for at finde den item, som er vores sidste header i hver domains, fileHashes, ips og processes 
            # Domains, fileHashes, ips og processes ligger alle under entities
            # Prøver at hente listen med værdier for den sidste header (fx domains, fileHashes, ips, processes) fra entities
            try:
                for item in alert["entities"].get(headers[-1]):   
                    # Skriver en række til CSV med alertId, machineId, firstActivity og værdien fra listen
                    csv_writer.writerow([alertId, machineId, firstActivity, item])
            # Hvis der opstår en fejl (fx headeren findes ikke), udskrives en fejlbesked og den kører videre 
            except Exception as e: 
                print((f"fejl ved behandling af alert {alertId}: can  not find header {headers[-1]}"))

# Expection as e er brugt for at finde de her fejl her: 

# IndexError hvis headers er tom (headers[-1])

# KeyError hvis "entities" mangler (alert["entities"])

# TypeError hvis .get(...) giver None og du prøver at iterere over det
    
# Laver en csvfil ud fra vores variabler headers og filename 
json_to_csv(domain_headers, "csv_file_1.csv")
json_to_csv(hashes_headers, "csv_file_2.csv")
json_to_csv(ips_headers, "csv_file_3.csv")
json_to_csv(processes_headers, "csv_file_4.csv")


