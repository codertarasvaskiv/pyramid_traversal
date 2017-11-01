import csv
import json
from ruamel import yaml


data_uk = []
data_en = []
data_ru = []
data = {
    'uk': data_uk,
    'en': data_en,
    'ru': data_ru
}

with open('/home/codertarasvaskiv/Documents/Projects/messaging/messaging/messaging/sheet1.csv', 'rb') as csv_file:
    tenderreader = csv.reader(csv_file, delimiter=',')
    for  row in tenderreader:
        data['uk'].append(
                {
                    "procurementMethodType": row[5].strip(),
                    "procurementMethod": row[4].strip(),
                    "name": row[1].strip(),
                    "autoInitiated": True if row[9].strip() == "Yes" else False,
                    "description": " ".join(row[6].strip().split('\n'))
                }
            )
        data['en'].append(
                {
                    "procurementMethodType": row[5].strip(),
                    "procurementMethod": row[4].strip(),
                    "name": row[2].strip(),
                    "autoInitiated": True if row[9].strip() == "Yes" else False,
                    "description": " ".join(row[7].strip().split('\n'))
                }
            )
        data['ru'].append(
                {
                    "procurementMethodType": row[5].strip(),
                    "procurementMethod": row[4].strip(),
                    "name": row[3].strip(),
                    "autoInitiated": True if row[9].strip() == "Yes" else False,
                    "description": " ".join(row[8].strip().split('\n'))
                }
        )

for lang in ['en', 'uk', 'ru']:
    with open('/home/codertarasvaskiv/Documents/Projects/messaging/messaging/messaging/archive/{}.json'.format(lang), 'w') as json_file:
        json.dump(data[lang][2:], json_file, sort_keys=True)

    with open('/home/codertarasvaskiv/Documents/Projects/messaging/messaging/messaging/archive/{}_pretty.json'.format(lang), 'w') as json_file:
        json.dump(data[lang][2:], json_file, sort_keys=True, indent=4)

    with open('/home/codertarasvaskiv/Documents/Projects/messaging/messaging/messaging/archive/{}.yaml'.format(lang), 'w') as yaml_file:
        yaml.safe_dump(data[lang][2:], yaml_file, width=1000, default_flow_style=False)

    with open('/home/codertarasvaskiv/Documents/Projects/messaging/messaging/messaging/archive/{}_pretty.yaml'.format(lang), 'w') as yaml_file:
        yaml.safe_dump(data[lang][2:], yaml_file, width=1000, default_flow_style=False, indent=2, allow_unicode=True)





