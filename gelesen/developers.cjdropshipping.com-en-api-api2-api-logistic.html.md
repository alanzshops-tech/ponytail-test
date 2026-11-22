# 6 Logistics | CJ Docs

- Quelle: https://developers.cjdropshipping.com/en/api/api2/api/logistic.html
- Abgerufen: 2026-08-09 17:47 UTC
- Sprache laut HTML: en-US · gemessen: Englisch (de 0 / en 66)
- Extraktion: trafilatura
- Zeichen: 28540
- Verfügbarkeit: keine Strukturdaten (JSON-LD) auf der Seite

---
# [#](https://developers.cjdropshipping.com#_6-logistics) 6 Logistics

 ## [#](https://developers.cjdropshipping.com#_1-logistics) 1 Logistics

 ### [#](https://developers.cjdropshipping.com#_1-1-freight-calculation-post) 1.1 Freight Calculation (POST)

 Freight calculation. Bulk purchase products will have designated shipping methods, while dropshipping products will usually have more options.

This is a simple mode of logistics trial calculation. If you want to use a more accurate logistics trial calculation, please use the interface: [1.2 Freight Calculation Tip](https://developers.cjdropshipping.com/en/api/api2/api/logistic.html#_1-2-freight-calculation-tip-post)

#### [#](https://developers.cjdropshipping.com#url) URL

 https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculate

#### [#](https://developers.cjdropshipping.com#curl) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculate' \
                --header 'Content-Type: application/json' \
                --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
                --data-raw '{
                    "startCountryCode": "CN",
                    "endCountryCode": "US",
                    "products": [
                        {
                            "quantity": 2,
                            "vid": "439FC05B-1311-4349-87FA-1E1EF942C418"
                        }
                    ]
                }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| startCountryCode | Country of origin | string | Y | 200 |  | 
| endCountryCode | Country of destination | string | Y | 200 |  | 
| zip | zip | string | N | 200 |  | 
| taxId | tax id | string | N | 200 |  | 
| houseNumber | house number | string | N | 200 |  | 
| iossNumber | ioss number | string | N | 200 |  | 
| quantity | Quantity | int | Y | 10 |  | 
| vid | Variant id | string | Y | 200 |  | 

#### [#](https://developers.cjdropshipping.com#return) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": [
        {
            "logisticAging": "2-5",
            "logisticPrice": 4.71,
            "logisticPriceCn": 30.54,
            "logisticName": "USPS+"
        }
    ],
    "requestId": "0242ad78-eea2-481d-876a-7cf64398f07f",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| logisticPrice | Shipping cost in USD | BigDecimal | （18，2） | Unit: $ (USD） | 
| logisticPriceCn | Shipping cost in CNY | BigDecimal | （18，2） | Unit: ¥ (CNY) | 
| logisticAging | Shipping time | string | 20 |  | 
| logisticName | Carrier name | string | 20 |  | 
| taxesFee | taxes fee | BigDecimal | (18, 2) | Unit：$(USD) | 
| clearanceOperationFee | customs clearance fee | BigDecimal | (18, 2) | Unit：$(USD) | 
| totalPostageFee | total postage | BigDecimal | (18, 2) | Unit：$(USD) | 

error

```
{
    "code": 1600100, 
    "result": false,
    "message": "Param error",
    "data": null,
    "requestId": "323fda9d-3c94-41dc-a944-5cc1b8baf5b1"
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | error code | int | 20 | [Reference error code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-code.html) | 
| result | Whether or not the return is normal | boolean | 1 |  | 
| message | return message | string | 200 |  | 
| data | return data | object |  | interface data return | 
| requestId | requestId | string | 48 | Flag request for logging errors | 

### [#](https://developers.cjdropshipping.com#_1-2-freight-calculation-tip-post) 1.2 Freight Calculation Tip(POST)

 Freight calculation. Bulk purchase products will have designated shipping methods, while dropshipping products will usually have more options.

#### [#](https://developers.cjdropshipping.com#url-2) URL

 https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculateTip

#### [#](https://developers.cjdropshipping.com#curl-2) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/logistic/freightCalculateTip' \
                --header 'Content-Type: application/json' \
                --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
                --data-raw '{
                    "reqDTOS": [
                        {
                            "srcAreaCode": "CN",
                            "destAreaCode": "US",
                            "length": 0.3,
                            "width": 0.4,
                            "height": 0.5,
                            "volume": 0.06,
                            "totalGoodsAmount":123.2,
                            "productProp": [
                                "COMMON"
                            ],
                            "freightTrialSkuList": [
                                {
                                    "skuQuantity": 1,
                                    "sku": "CJCF104237201AZ"
                                }
                            ],
                            "skuList": [
                                "CJCF104237201AZ"
                            ],
                            "platforms": [
                                "Shopify"
                            ]
                        }
                    ]
                }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| srcAreaCode | Country of origin | string | Y | 200 | First call [Query Inventory by Product ID](https://developers.cjdropshipping.com/en/api/api2/api/product.html#_3-3-query-inventory-by-product-id-get) — the response field`inventories.countryCode` lists the country/countries currently holding stock (i.e. valid shipping origins) for that product, then cross-reference against the[Country Code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-country.html) enum to confirm the srcAreaCode | 
| destAreaCode | Country of destination | string | Y | 200 |  | 
| customerCode | customer code | string | N | 200 |  | 
| zip | zip | string | N | 200 |  | 
| houseNumber | house number | string | N | 100 |  | 
| iossNumber | ioss number | string | N | 200 |  | 
| storageIdList | Storage id List | string[] | N | 100 |  | 
| recipientAddress | Recipient address | string | N | 200 |  | 
| city | City | string | N | 50 |  | 
| recipientName | Recipient name | String | N | 200 |  | 
| skuList | Sku list | String[] | Y | 200 |  | 
| town | Town | String | N | 100 |  | 
| phone | Phone | String | N | 50 |  | 
| wrapWeight | wrap weight,Unit:g | int | Y | 200 |  | 
| volume | Volume,Unit:cm³ | BigDecimal | Y | 200 |  | 
| station | station | String | N | 200 | Referer: [Country Code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-country.html) , Please use The two-letter code | 
| platforms | Platform List | String[] | N | 200 | Referer [Platforms](https://developers.cjdropshipping.com/en/api/api2/standard/ps-Platforms.html) | 
| dutyNo | dutyNo | String | N | 200 |  | 
|  |  | String | N | 100 |  | 
| province | province | String | N | 100 |  | 
| recipientAddress1 | recipient address1 | String | N | 200 |  | 
| uid | uid | String | N | 200 |  | 
| recipientId | recipient id | String | N | 200 |  | 
| recipientAddress2 | recipient address2 | String | N | 200 |  | 
| amount | amount | BigDecimal | N | 50 |  | 
| productTypes | product type | String[] | N |  | 0: normal goods, 1: service goods, 3: packaged goods, 4: supplier goods, 5: supplier self-delivered goods, 6: virtual goods, 7: pod personalized goods | 
| weight | weight,Unit:g | int | Y | 100 |  | 
| productProp | product prop | String | Y | 100 | Get it via [Product Details](https://developers.cjdropshipping.com/en/api/api2/api/product.html#_1-5-product-details-get) — use the response field`productProEnSet` as this input. See[Appendix 4：Product Logistics Property](https://developers.cjdropshipping.com/en/api/api2/standard/ps-product-property.html) for the full list of valid values | 
| optionName | option name | String | N | 200 |  | 
| volumeWeight | volume weight,Unit:g | BigDecimal | N | 100 |  | 
| orderType | order type | String | N | 100 |  | 
| totalGoodsAmount | total value of goods | BigDecimal | N | 100 |  | 
| freightTrialSkuList | freight trial sku list | Object[] | Y |  |  | 
| - productCode | product code | String | N | 100 |  | 
| - hscode | hs code | String | N | 100 |  | 
| - sku | sku | String | N | 100 |  | 
| - productPropList | Product attributes | String[] | N | 100 |  | 
| - productTypeList | product type | String[] | N |  | 0: normal goods, 1: service goods, 3: packaged goods, 4: supplier goods, 5: supplier self-delivered goods, 6: virtual goods, 7: pod personalized goods | 
| - vid | variant id | String | N | 100 |  | 
| - skuQuantity | sku quantity | int | N | 50 |  | 
| - skuWeight | sku weight,Unit:g | BigDecimal | N | 100 |  | 
| - skuVolume | sku volume,Unit:cm³ | BigDecimal | N | 100 |  | 
| - combinationType | combination type | int | N | 50 |  | 
| - parentVid | parent variant id | String | N | 50 |  | 
| - unsalable | unsalable | int | N | 10 |  | 
| - tailCostQuantity | tail cost quantity | int | N | 10 |  | 
| - privateDeductionQuantity | private deduction quantity | int | N | 10 |  | 

#### [#](https://developers.cjdropshipping.com#return-2) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": [
        {
            "arrivalTime": "12-50",
            "discountFee": 4.09,
            "discountFeeCNY": 25.30,
            "volumeWeight": null,
            "option": {
                "arrivalTime": "12-50",
                "cnName": "CJ航空挂号小包",
                "enName": "CJPacket Postal",
                "id": "1564849338719199233"
            },
            "ruleTips": [
                {
                    "expression": "^[\\s\\d\\-（）()+]{6,32}$",
                    "interceptType": "0",
                    "max": null,
                    "min": null,
                    "msgCode": "1001",
                    "msgEn": "Must be a 6-32 digit number (only numbers, symbols and spaces are supported).",
                    "type": "phone"
                }
            ],
            "ruleTipTypes": [
                "phone"
            ],
            "channelId": "1564543005939785730",
            "error": "",
            "errorEn": "",
            "optionId": "1564849338719199233",
            "postage": 3.55,
            "postageCNY": 22.00,
            "priceIncreases": "115",
            "reSort": "62",
            "remoteFee": 0,
            "remoteFeeCNY": 0,
            "tip": "",
            "uid": "",
            "orderId": null,
            "unWeightChargeTarget": null,
            "floatMaxPrice": null,
            "floatMinPrice": null,
            "logisticsParamRespDTO": null,
            "message": "Hi, CJ will not accept any disputes when you choose the shipping method, which is not trackable when orders arrived at some countries, states, or cities.",
            "wrapPostage": 4.09,
            "wrapPostageCNY": 25.30,
            "wrapWeight": 0,
            "stopWords": [],
            "channel": {
                "cnName": "促佳燕文航空挂号小包特货",
                "enName": "燕文航空挂号小包特货",
                "id": "1564543005939785730"
            },
            "cjRespDTO": {
                "postage": "3.55",
                "postageCNY": "22.00",
                "remoteFee": "0.00",
                "remoteFeeCNY": "0"
            },
            "destArea": {
                "cnName": "美国",
                "countryId": "233",
                "enName": "United States of America (the)",
                "id": "233",
                "parentId": null,
                "postCode": "",
                "shortCode": "US"
            },
            "srcArea": {
                "cnName": "中国",
                "countryId": "48",
                "enName": "China",
                "id": "48",
                "parentId": null,
                "postCode": "",
                "shortCode": "CN"
            },
            "dump": false,
            "zonePrice": [],
            "allRuleTips": [
                {
                    "expression": "^[\\s\\d\\-（）()+]{6,32}$",
                    "interceptType": "0",
                    "max": null,
                    "min": null,
                    "msgCode": "1001",
                    "msgEn": "Must be a 6-32 digit number (only numbers, symbols and spaces are supported).",
                    "type": "phone"
                }
            ],
            "taxesFee": null,
            "clearanceOperationFee": null
        }
    ],
    "requestId": "55c4708d15d44a499f061582ddbd989b",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| arrivalTime | arrival time | string | 200 |  | 
| discountFee | discount Fee | BigDecimal | （18，2） | Unit: $ (USD） | 
| discountFeeCNY | discount Fee CNY | BigDecimal | （18，2） |  | 
| volumeWeight | volume weight | BigDecimal | （18，2） | Unit: $ (USD） | 
| channelId | channel id | String | 200 |  | 
| error | error | String | 200 |  | 
| errorEn | errorEn | String | 200 |  | 
| optionId | option id | String | 100 |  | 
| postage | postage | BigDecimal | （18，2） | Unit: $ (USD） | 
| postageCNY | postage CNY | BigDecimal | （18，2） | Unit: $ (USD） | 
| priceIncreases | price increases | String | 100 |  | 
| reSort | reSort | String | 100 |  | 
| remoteFee | remoteFee | BigDecimal | （18，2） | Unit: $ (USD） | 
| remoteFeeCNY | remoteFee CNY | BigDecimal | （18，2） | Unit: $ (USD） | 
| tip | tip | string | 200 |  | 
| uid | uid | String | 200 |  | 
| orderId | order id | String | 100 |  | 
| unWeightChargeTarget | unWeightChargeTarget | BigDecimal | （18，2） | Unit: $ (USD） | 
| floatMaxPrice | floatMaxPrice | BigDecimal | （18，2） | Unit: $ (USD） | 
| floatMinPrice | floatMinPrice | BigDecimal | （18，2） | Unit: $ (USD） | 
| logisticsParamRespDTO | logisticsParamRespDTO | String | 200 |  | 
| message | message | String | 200 |  | 
| wrapPostage | wrap postage | BigDecimal | （18，2） | Unit: $ (USD） | 
| wrapPostageCNY | wrap postage CNY | BigDecimal | （18，2） | Unit: $ (USD） | 
| wrapWeight | wrap weight | BigDecimal | （18，2） | Unit: $ (USD） | 
| stopWords | Stop Words | String[] | 200 |  | 
| channel | channel | Object |  |  | 
| - cnName | name(CN) | String | 200 |  | 
| - enName | name(EN) | String | 200 |  | 
| - id | id | String | 200 |  | 
| option | option | Object |  |  | 
| - arrivalTime | arrival time | String | 100 |  | 
| - cnName | name(CN) | String | 100 |  | 
| - enName | name(EN) | String | 100 |  | 
| - id | id | String | 100 |  | 
| taxesFee | US taxes fee (not included in postage) | BigDecimal | （18，2） | Unit: $ (USD） | 
| clearanceOperationFee | customs clearance fee | BigDecimal | （18，2） | Unit: $ (USD） | 
| tariff | EU tariff (not included in postage) | BigDecimal | （18，2） | Unit: $ (USD） | 
| totalPostageFee | total postage = postage + taxesFee + clearanceOperationFee + tariff | BigDecimal | (18, 2) | Unit：$(USD) | 
| recommendLogisticsTypeList | recommend logistics type, 0-time priority, 1-price priority, 2-composite recommend | int[] |  |  | 
| timePrioritySort | time priority sort value | int |  |  | 
| pricePrioritySort | price priority sort value | int |  |  | 
| compositeRecommendSort | composite recommend sort value | int |  |  | 
| zonePrice | zone price list | object[] |  |  | 
| - storageId | storage id | string | 100 |  | 
| - discountFee | discount fee | string | 100 |  | 
| - lastDiscountFee | last discount fee | string | 100 |  | 
| - wrapPostage | wrap postage | string | 100 |  | 
| - lastWrapPostage | last wrap postage | string | 100 |  | 
| allRuleTips | all rule tips | object[] | 200 |  | 
| - expression | expression | string | 20 |  | 
| - interceptType | InterceptType | string | 20 | 0-Strong Interception 1-Non-strong Interception | 
| - max | Maximum range (name, address) | string | 20 |  | 
| - min | Minimum scope (name, address) | string | 20 |  | 
| - msgCode | Tip code | string | 20 |  | 
| - type | Type | string | 20 | phone-Phone number required rule; dutyNo-Duty number required rule; email-Email required rule; zip-Zip code required rule; town-Town/County required rule; houseNumber-House number required rule; iossNumber-IOSS number required rule; recipientId-Recipient ID required rule; province-Province/State required rule; recipientName-Recipient name length validation; recipientAddress-Address1+Address2 length validation; city-City character length validation | 
| - msgEn | msg(english) | string | 20 |  | 
| destArea | Target Area | object | 20 |  | 
| - cnName | Country name (In Chinese) | string | 20 |  | 
| - enName | Country Name (English) | string | 20 |  | 
| - countryId | Country Id | string | 20 |  | 
| - parentId | Parent Id | string | 20 |  | 
| - postCode | Post Code | string | 20 |  | 
| - shortCode | Short Code | string | 20 |  | 
| - id | id | string | 20 |  | 
| srcArea | Source Area | object | 20 |  | 
| - cnName | Country name (In Chinese) | string | 20 |  | 
| - enName | Country Name (English) | string | 20 |  | 
| - countryId | Country Id | string | 20 |  | 
| - parentId | Parent Id | string | 20 |  | 
| - postCode | Post Code | string | 20 |  | 
| - shortCode | Short Code | string | 20 |  | 
| - id | id | string | 20 |  | 

error

```
{
    "code": 1600100, 
    "result": false,
    "message": "Param error",
    "data": null,
    "requestId": "323fda9d-3c94-41dc-a944-5cc1b8baf5b1"
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | error code | int | 20 | [Reference error code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-code.html) | 
| result | Whether or not the return is normal | boolean | 1 |  | 
| message | return message | string | 200 |  | 
| data | return data | object |  | interface data return | 
| requestId | requestId | string | 48 | Flag request for logging errors | 

### [#](https://developers.cjdropshipping.com#_1-3-partner-freight-calculation-post) 1.3 Partner Freight Calculation(POST)

 Freight calculation for merchant partner orders. Calculates shipping costs based on order information and destination.

#### [#](https://developers.cjdropshipping.com#url-3) URL

 https://developers.cjdropshipping.com/api2.0/v1/logistic/partnerFreightCalculate

#### [#](https://developers.cjdropshipping.com#curl-3) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/logistic/partnerFreightCalculate' \
                --header 'Content-Type: application/json' \
                --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
                 --data-raw '{
                    "orderNumber": "1234",
                    "shippingZip": "10001",
                    "shippingCountryCode": "US",
                    "shippingCountry": "United States",
                    "shippingProvince": "New York",
                    "shippingCity": "New York",
                    "shippingAddress": "123 Test St",
                    "shippingCustomerName": "John Doe",
                    "shippingPhone": "1234567890",
                    "remark": "note",
                    "fromCountryCode": "CN",
                    "logisticName": "PostNL",
                    "houseNumber": "123",
                    "iossType": 1,
                    "iossNumber": "",
                    "products": [
                        {
                            "vid": "92511400-C758-4474-93CA-66D442F5F787",
                            "quantity": 1
                        }
                    ]
                }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| orderNumber | Order number | String | Y | 40 |  | 
| shippingCountryCode | Destination country code | string | Y | 200 |  | 
| shippingCountry | Destination country | string | Y | 200 |  | 
| shippingProvince | Province/State | string | Y | 200 |  | 
| shippingCity | City | string | Y | 200 |  | 
| shippingAddress | Address | string | N | 200 |  | 
| shippingCustomerName | Recipient name | string | N | 200 |  | 
| shippingZip | Zip code | string | Y | 200 |  | 
| shippingPhone | Phone | string | N | 200 | Make sure the phone number is accurate | 
| houseNumber | House number | string | N | 20 |  | 
| remark | Order remark | string | N | 500 |  | 
| logisticName | Logistics name | string | N | 200 |  | 
| fromCountryCode | Origin country | string | Y | 200 | Warehouse country | 
|  |  | string | N | 200 |  | 
| consigneeID | Consignee ID | string | N | 200 |  | 
| iossType | IOSS type | int | N | 20 | 1-Don't use IOSS 2-Use my IOSS number 3-Use CJ's IOSS number | 
| iossNumber | IOSS number | string | N | 20 |  | 
| products | Product list | list | Y | 200 |  | 
| - vid | Variant id | string | Y | 200 |  | 
| - quantity | Quantity | int | Y | 200 |  | 

#### [#](https://developers.cjdropshipping.com#return-3) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": [
        {
            "postageAmount": 1.69,
            "logisticsModel": "YTGN",
            "logisticsName": "YTO China Domestic",
            "arrivalTime": "2-3",
            "isSupportIoss": false,
            "iossList": [
                {
                   "iossNumber": "",
                   "iossType": "",
                   "serviceAmount": "",
                   "taxAmount": ""
                }
            ]
         }
    ],
    "requestId": "0242ad78-eea2-481d-876a-7cf64398f07f",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| postageAmount | Shipping cost | BigDecimal | (18, 2) | Unit: $(USD) | 
| logisticsModel | Logistics channel | string | 200 |  | 
| logisticsName | Logistics name | string | 200 |  | 
| arrivalTime | Delivery time | string | 20 |  | 
| isSupportIoss | Whether IOSS is supported | boolean |  |  | 
| iossList | IOSS list | list |  |  | 
| - iossNumber | IOSS number | string |  |  | 
| - iossType | Whether default. 1-Don't use IOSS 2-Use my IOSS 3-Use CJ's IOSS |  |  |  | 
| - serviceAmount | Service fee | BigDecimal | (18, 2) | Unit: $(USD) | 
| - taxAmount | Tax amount | BigDecimal | (18, 2) | Unit: $(USD) | 

error

```
{
    "code": 1600100, 
    "result": false,
    "message": "Param error",
    "data": null,
    "requestId": "323fda9d-3c94-41dc-a944-5cc1b8baf5b1"
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | error code | int | 20 | [Reference error code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-code.html) | 
| result | Whether or not the return is normal | boolean | 1 |  | 
| message | return message | string | 200 |  | 
| data | return data | object |  | interface data return | 
| requestId | requestId | string | 48 | Flag request for logging errors | 

### [#](https://developers.cjdropshipping.com#_1-4-supplier-self-shipment-logistics-trial-calculation-post) 1.4 Supplier self-shipment logistics trial calculation(POST)

 #### [#](https://developers.cjdropshipping.com#url-4) URL

 https://developers.cjdropshipping.com/api2.0/v1/logistic/getSupplierLogisticsTemplate

#### [#](https://developers.cjdropshipping.com#curl-4) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/logistic/getSupplierLogisticsTemplate' \
                --header 'Content-Type: application/json' \
                 --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
                 --data-raw '{
                    "skuList": ""
                }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| skuList | Product SPU | String[] | Y | 200 |  | 

#### [#](https://developers.cjdropshipping.com#response) Response

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": [
        {
            "skuList": [],
            "logisticsInfoList": [
                {
                    "id": "123",
                    "logisticsName": "fdd",
                    "postage": "",
                    "startCountryCode": "",
                    "destCountryCode": ""
                }
            ]
        }
    ],
    "requestId": "0242ad78-eea2-481d-876a-7cf64398f07f",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| skuList | SPU List | String[] |  |  | 
| logisticsInfoList | logistics Information | Object[] |  |  | 
| - id | Template Id | string | 100 |  | 
| - logisticsName | Logistics Name | string | 200 |  | 
| - postage | Postage Fee | BigDecimal | (18,2) | Unit：$(USD) | 
| - startCountryCode | Start Country Code | string | 100 |  | 
| - destCountryCode | Target Country Code | string | 100 |  | 

error

```
{
    "code": 1600100, 
    "result": false,
    "message": "Param error",
    "data": null,
    "requestId": "323fda9d-3c94-41dc-a944-5cc1b8baf5b1"
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | error code | int | 20 | [Reference error code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-code.html) | 
| result | Whether or not the return is normal | boolean | 1 |  | 
| message | return message | string | 200 |  | 
| data | return data | object |  | interface data return | 
| requestId | requestId | string | 48 | Flag request for logging errors | 

## [#](https://developers.cjdropshipping.com#_2-tracking-number) 2 Tracking Number

 ### [#](https://developers.cjdropshipping.com#_2-1-get-tracking-information-get) 2.1 Get Tracking Information (GET)

 Shipping information can be found upon tracking numbers. You can also visit [CJ Logistic Platform (opens new window)](https://cjpacket.com/)

#### [#](https://developers.cjdropshipping.com#url-5) URL

 https://developers.cjdropshipping.com/api2.0/v1/logistic/trackInfo?trackNumber=CJPKL7160102171YQ

#### [#](https://developers.cjdropshipping.com#curl-5) CURL

 ```
curl --location --request GET 'https://developers.cjdropshipping.com/api2.0/v1/logistic/trackInfo?trackNumber=CJPKL7160102171YQ
                                                                                                    &trackNumber=CJPKL7160102171YQ
                                                                                                    &trackNumber=CJPKL7160102171YQ
                                                                                                    &trackNumber=CJPKL7160102171YQ
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| trackNumber | trackNumber | string | Y | 200 | batch query | 

#### [#](https://developers.cjdropshipping.com#return-4) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": [
        {
            "trackingNumber": "CJPKL7160102171YQ",
            "logisticName": "CJPacket Sensitive",
            "trackingFrom": "CN",
            "trackingTo": "US",
            "deliveryDay": "13",
            "deliveryTime": "2021-06-17 07:04:04",
            "trackingStatus": "In transit",
            "lastMileCarrier": "CJPacket",
            "lastTrackNumber": "926112903032124"
        }
    ],
    "requestId": "3426e927-8c50-4687-9ced-623e77d55bd0",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| trackingNumber | tracking number | string | 200 |  | 
| trackingFrom | from | string | 20 |  | 
| trackingTo | to | string | 20 |  | 
| deliveryDay | Delivery day | string | 200 |  | 
| deliveryTime | Delivery time | string | 200 |  | 
| trackingStatus | tracking status | string | 200 |  | 
| lastMileCarrier | last mile carrier | string | 200 |  | 
| lastTrackNumber | last mile tracking number | string | 200 |  | 

error

```
{
    "code": 1600100,
    "result": false,
    "message": "Param error",
    "data": null,
    "requestId": "323fda9d-3c94-41dc-a944-5cc1b8baf5b1" 
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | error code | int | 20 | [Reference error code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-code.html) | 
| result | Whether or not the return is normal | boolean | 1 |  | 
| message | return message | string | 200 |  | 
| data | return data | object |  | interface data return | 
| requestId | requestId | string | 48 | Flag request for logging errors |
