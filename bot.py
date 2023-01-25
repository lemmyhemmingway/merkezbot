import requests
import datetime
import xmltodict
import json

left_at = None
try: 
    with open('leftat.json', 'r') as f:
        data = json.loads(f.read())
        left_at = data['left_at']

    with open("result.json", 'r') as f:
        data = json.loads(f.read())
except: pass

if left_at is not None:
    start_date = datetime.datetime.strptime(left_at, "%Y-%m-%d")
    merkez_bankasi_data = data
else:
    start_date = datetime.datetime(2021, 12, 30)
    merkez_bankasi_data = []
today = datetime.date.today()


loop = 1
currency_data = []
while start_date.date() < today:
    try:
        year = start_date.strftime("%Y")
        month = start_date.strftime("%m")
        day = start_date.strftime("%d")
        timestamp = start_date.timestamp()
        url = f"https://www.tcmb.gov.tr/kurlar/{year}{month}/{day}{month}{year}.xml?_={timestamp}"
        response = requests.get(url)
        tarih = start_date.date()
        if response.status_code != 404:
            parsed_xml = xmltodict.parse(response.text)
            tarih = parsed_xml['Tarih_Date']['@Tarih']
            currency = parsed_xml['Tarih_Date']['Currency']
            currency_data = dict()
            for item in currency:
                kod = item["@Kod"]
                forex_buy = item["ForexBuying"]
                forex_sell = item["ForexSelling"]
                currency_data[kod] = dict(forex_buy=forex_buy, forex_sell=forex_sell)


            merkez_bankasi_data.append(dict(tarih=datetime.datetime.strptime(tarih, "%d.%m.%Y").strftime("%Y-%m-%d"), data=currency_data, tatil=False))

        else:
            merkez_bankasi_data.append(dict(tarih=datetime.datetime.strftime(start_date, "%Y-%m-%d"), data=currency_data, tatil=True))

        start_date = start_date + datetime.timedelta(days=1)

        print(start_date)
    except:
        with open('leftat.json', 'w') as file:
            file.write(json.dumps(dict(left_at=datetime.datetime.strftime(start_date, "%Y-%m-%d"))))
        break

with open('result.json', 'w') as file:
    file.write(json.dumps(merkez_bankasi_data))

