# # -*- coding: utf-8 -*-
# import requests
# import json
# from datetime import datetime, timedelta
#
# def get_now():
#     return datetime.now()
#
#
# test_tender_data = {
#     "title": "Послуги шкільних їдалень",
#     "title_en": "Services in school canteens",
#     "procurementMethodType": "esco",
#     "minimalStepPercentage": 0.006,
#     "procuringEntity": {
#         "kind": "general",
#         "address": {
#             "countryName": "Україна",
#             "locality": "м. Вінниця",
#             "postalCode": "21027",
#             "region": "м. Вінниця",
#             "streetAddress": "вул. Стахурського. 22"
#         },
#         "contactPoint": {
#             "name": "Куца Світлана Валентинівна",
#             "name_en": "Kutsa Svitlana V.",
#             "telephone": "+380 (432) 46-53-02",
#             "availableLanguage": u"uk",
#             "url": "http://sch10.edu.vn.ua/"
#         },
#         "identifier": {
#             "id": "21725150",
#             "legalName": "Заклад \"Загальноосвітня школа І-ІІІ ступенів № 10 Вінницької міської ради\"",
#             "legalName_en": "The institution \"Secondary school I-III levels № 10 Vinnitsa City Council\"",
#             "scheme": "UA-EDR"
#         },
#         "name": "ЗОСШ #10 м.Вінниці",
#         "name_en": "School #10 of Vinnytsia"
#     },
#     "items": [
#         {
#             "unit": {
#                 "code": "44617100-9",
#                 "name": "item"
#             },
#             "additionalClassifications": [
#                 {
#                     "scheme": "ДКПП",
#                     "id": "17.21.1",
#                     "description": "Послуги шкільних їдалень"
#                 }
#             ],
#             "description": "Послуги шкільних їдалень",
#             "description_en": "Services in school canteens",
#             "classification": {
#                 "scheme": "ДК021",
#                 "id": "37810000-9",
#                 "description": "Test"
#             },
#             "deliveryDate": {
#                 "startDate": (get_now() + timedelta(days=20)).isoformat(),
#                 "endDate": (get_now() + timedelta(days=50)).isoformat()
#             },
#             "deliveryAddress": {
#                 "countryName": u"Україна",
#                 "postalCode": "79000",
#                 "region": u"м. Київ",
#                 "locality": u"м. Київ",
#                 "streetAddress": u"вул. Банкова 1"
#             },
#             "quantity": 1
#         },
#         {
#             "unit": {
#                 "code": "44617100-9",
#                 "name": "item"
#             },
#             "additionalClassifications": [
#                 {
#                     "scheme": "ДКПП",
#                     "id": "17.21.1",
#                     "description": "Послуги шкільних їдалень"
#                 }
#             ],
#             "description": "Послуги шкільних їдалень",
#             "description_en": "Services in school canteens",
#             "classification": {
#                 "scheme": "ДК021",
#                 "id": "37810000-9",
#                 "description": "Test"
#             },
#             "quantity": 1,
#             "deliveryDate": {
#                 "startDate": (get_now() + timedelta(days=20)).isoformat(),
#                 "endDate": (get_now() + timedelta(days=50)).isoformat()
#             },
#             "deliveryAddress": {
#                 "countryName": u"Україна",
#                 "postalCode": "79000",
#                 "region": u"м. Київ",
#                 "locality": u"м. Київ",
#                 "streetAddress": u"вул. Банкова 1"
#             }
#         }
#     ],
#     "NBUdiscountRate": 0.22,
#     "fundingKind": "other",
#     "yearlyPaymentsPercentageRange": 0.8
# }
#
#
#
# cookie = {'Cookie':'SERVER_ID=20aca072c375f487b6baa84e400150b6a551d9fd5e754e09f167f4ac408a4ff87cb7b65899e1e3bac6da4cc9a542bd24840a9d62cd3cd418c4189b06c5ad012e'}
# url = "http://localhost:8080/api/2.4/tenders"
# resp = requests.get(url)
#
# cookie['Cookie'] = resp.cookies.values()[0]
#
# headers = {'Connection':'keep-alive'}
#
# resp = requests.post(url, cookies=cookie, data=test_tender_data, headers=headers )
# print resp.__dict__
#
#
#
#
