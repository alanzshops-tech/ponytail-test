# 2 Settings | CJ Docs

- Quelle: https://developers.cjdropshipping.com/en/api/api2/api/setting.html
- Abgerufen: 2026-08-09 17:47 UTC
- Sprache laut HTML: en-US · gemessen: Englisch (de 0 / en 8)
- Extraktion: trafilatura
- Zeichen: 3057
- Verfügbarkeit: keine Strukturdaten (JSON-LD) auf der Seite

---
# [#](https://developers.cjdropshipping.com#_2-settings) 2 Settings

 ## [#](https://developers.cjdropshipping.com#_1-settings) 1 Settings

 ### [#](https://developers.cjdropshipping.com#_1-1-get-settings-get) 1.1 Get Settings（GET）

 Account settings include profile, API quota limits, general API QPS limits, sandbox account, etc.

#### [#](https://developers.cjdropshipping.com#url) URL

 https://developers.cjdropshipping.com/api2.0/v1/setting/get

#### [#](https://developers.cjdropshipping.com#curl) CURL

 ```
curl --location --request GET 'https://developers.cjdropshipping.com/api2.0/v1/setting/get' \
                --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```
#### [#](https://developers.cjdropshipping.com#return) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": {
        "openId": 1,
        "openName": "121 2322",
        "openEmail": "v0pjsw5t@linshiyouxiang.net",
        "setting": {
            "quotaLimits": [
                {
                    "quotaUrl": "/api2.0/v1/setting/account/get",
                    "quotaLimit": 74,
                    "quotaType": 0
                }
            ],
            "qpsLimit": 100
        },
        "callback": {
            "product": {
                "type": "ENABLE",
                "urls": ["https://your-domain.com/api2.0/"]
            },"order": {
                "type": "CANCEL",
                "urls": []
            }
        },
        "root": "GENERAL",
        "isSandbox": false
    },
    "requestId": "ea5896b0-273d-4b49-8c54-ad8f025a49b8"
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| openId | Account ID | string | 200 |  | 
| openName | Account name | string | 200 |  | 
| openEmail | Account Email | string | 200 |  | 
| setting | Settings | list | 200 |  | 
| quotaLimits | Quota limits | list |  | Applicable on specific URLs | 
| quotaUrl | Quota URL | string | 200 |  | 
| quotaLimit | Quota limit | int | 20 |  | 
| quotaType | Quota Type | byte | 4 | 0-total，1-per year，2-per quarter，3-per month，4-per day，5-per hour | 
| qpsLimit | QPS limit | int | 20 | account Queries per second | 
| root | Root access | string | 200 | root：NO_PERMISSION - not authorized | 
|  |  |  |  | GENERAL - general account | 
|  |  |  |  | VIP - VIP account | 
|  |  |  |  | ADMIN - administrator | 
| isSandbox | (Whether) Sandbox account | byte | 4 |  | 

error

```
{
    "code": 1601000,
    "result": false,
    "message": "User not find",
    "data": null,
    "requestId": "a18c9793-7c99-42f9-970b-790eecdceba2"
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | error code | int | 20 | [Reference error code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-code.html) | 
| result | Whether or not the return is normal | boolean | 1 |  | 
| message | return message | string | 200 |  | 
| data | return data | object |  | interface data return | 
| requestId | requestId | string | 48 | Flag request for logging errors |
