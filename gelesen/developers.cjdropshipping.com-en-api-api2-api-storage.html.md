# 04. Storage | CJ Docs

- Quelle: https://developers.cjdropshipping.com/en/api/api2/api/storage.html
- Abgerufen: 2026-08-09 17:42 UTC
- Sprache laut HTML: en-US · gemessen: Englisch (de 0 / en 36)
- Extraktion: trafilatura
- Zeichen: 22097
- Verfügbarkeit: keine Strukturdaten (JSON-LD) auf der Seite

---
# [#](https://developers.cjdropshipping.com#_04-storage) 04. Storage

 ## [#](https://developers.cjdropshipping.com#_1-storage-info) 1 Storage Info

 ### [#](https://developers.cjdropshipping.com#_1-1-get-storage-info-get) 1.1 Get Storage Info (GET)

 #### [#](https://developers.cjdropshipping.com#url) URL

 https://developers.cjdropshipping.com/api2.0/v1/warehouse/detail

#### [#](https://developers.cjdropshipping.com#curl) CURL

 ```
curl --location 'https://developers.cjdropshipping.com/api2.0/v1/warehouse/detail?id=201e67f6ba4644c0a36d63bf4989dd70' \
     --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| id | Storage ID | string | Y | 200 |  | 

#### [#](https://developers.cjdropshipping.com#return) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": {
        "id": "201e67f6ba4644c0a36d63bf4989dd70",
        "name": "Cranbury Warehouse",
        "areaId": 2,
        "areaCountryCode": "US",
        "address1": "Cranbury, New Jersey ",
        "address2": null,
        "contacts": null,
        "phone": "+1-9095862127",
        "city": "Cranbury",
        "province": "New Jersey",
        "logisticsBrandList": [
            {
                "id": "USPS",
                "name": "USPS"
            },
            {
                "id": "FedEx",
                "name": "FedEx"
            },
            {
                "id": "UPS",
                "name": "UPS"
            },
            {
                "id": "GOFO",
                "name": "GOFO"
            },
            {
                "id": "DHL",
                "name": "DHL"
            },
            {
                "id": "UniUni",
                "name": "UniUni"
            },
            {
                "id": "CBT",
                "name": "CBT"
            }
        ],
        "isSelfPickup": null,
        "zipCode": null
    },
    "requestId": "2b97f15603384fe4832e85617cf07d9c",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| id | Storage Id | string | 200 |  | 
| name | name | string | 200 |  | 
| areaId | area id | integer | 200 |  | 
| areaCountryCode | country code | string | 200 |  | 
| province | province | string | 200 |  | 
| city | city | string | 200 |  | 
| address1 | address1 | string | 200 |  | 
| address2 | address2 | string | 200 |  | 
| contacts | contacts | string | 200 |  | 
| phone | phone number | string | 200 |  | 
| isSelfPickup | Is support self pickup | integer | 1 | 1: support 0: not supported | 
| zipCode | zip Code | string | 200 |  | 
| logisticsBrandList | Supported logistics brands | list | 200 |  | 
| - id | Logistics brand ID | string | 200 |  | 
| - name | Logistics brand Name | string | 200 |  | 

error

```
{
    "code": 1608001,
    "result": false,
    "message": "Warehouse info not found",
    "data": null,
    "requestId": "c5d92fbc9c794c5caa0ce453dd9c9236",
    "success": false
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | error code | int | 20 | [Reference error code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-code.html) | 
| result | Whether or not the return is normal | boolean | 1 |  | 
| message | return message | string | 200 |  | 
| data | return data | object |  | interface data return | 
| requestId | requestId | string | 48 | Flag request for logging errors | 

## [#](https://developers.cjdropshipping.com#_2-private-inventory) 2 Private Inventory

 All APIs below query private inventory data for the account bound to the current `CJ-Access-Token`. The server automatically binds the current user, so `userId` is not required in the request body.

### [#](https://developers.cjdropshipping.com#_2-1-query-private-inventory-spu-page-post) 2.1 Query Private Inventory SPU Page (POST)

 #### [#](https://developers.cjdropshipping.com#url-2) URL

 https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySpuPage

#### [#](https://developers.cjdropshipping.com#curl-2) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySpuPage' \
         --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
         --header 'Content-Type: application/json' \
         --data-raw '{
                "pageNum": 1,
                "pageSize": 20,
                "keyword": "shirt",
                "availableStock": true,
                "productId": "1234567890",
                "sku": "CJNS000000101AZ",
                "sortField": "totalWarehouseQuantity",
                "sortType": "desc"
         }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| pageNum | Page number | integer | N | 20 | Default 1 | 
| pageSize | Page size | integer | N | 20 | Default 20 | 
| keyword | Search keyword | string | N | 200 | Fuzzy search by product name/SPU/SKU | 
| availableStock | Only products with available stock | boolean | N | 1 | true-yes | 
| pack | Is packaging product | boolean | N | 1 | true-yes | 
| serviceProd | Is service product | boolean | N | 1 | true-yes | 
| pod | Is POD product | boolean | N | 1 | true-yes | 
| productId | Product ID | string | N | 200 | CJ product ID | 
| sku | SKU | string | N | 200 | Product SKU | 
| sortField | Sort field | string | N | 100 | e.g. totalWarehouseQuantity, minStockPrice | 
| sortType | Sort type | string | N | 10 | asc/desc | 

#### [#](https://developers.cjdropshipping.com#return-2) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": {
        "pageSize": 20,
        "pageNumber": 1,
        "totalRecords": 1,
        "totalPages": 1,
        "content": [
            {
                "productId": "1234567890",
                "productName": "Private Inventory Product",
                "spu": "CJNS0000001",
                "productPic": "https://...",
                "productType": "NORMAL",
                "skuQuantity": 3,
                "totalWarehouseQuantity": 100,
                "minStockPrice": 1.23,
                "maxStockPrice": 2.34,
                "warehouseQuantityInfoList": [
                    {
                        "countryCode": "US",
                        "warehouseQuantity": 100,
                        "clientTransitQuantity": 0
                    }
                ]
            }
        ]
    },
    "requestId": "2b97f15603384fe4832e85617cf07d9c"
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| pageSize | Page size | long | 20 | Pagination field | 
| pageNumber | Current page | long | 20 | Pagination field | 
| totalRecords | Total records | long | 20 | Pagination field | 
| totalPages | Total pages | long | 20 | Pagination field | 
| content | SPU inventory list | list |  |  | 
| productId | Product ID | string | 200 |  | 
| productName | Product name | string | 500 |  | 
| spu | SPU | string | 200 |  | 
| productPic | Product image | string | 500 |  | 
| productType | Product type | string | 100 |  | 
| skuQuantity | SKU quantity | integer | 20 |  | 
| totalWarehouseQuantity | Total warehouse inventory | long | 20 |  | 
| minStockPrice | Minimum inventory unit price | BigDecimal | (18,2) | Unit: USD | 
| maxStockPrice | Maximum inventory unit price | BigDecimal | (18,2) | Unit: USD | 
| warehouseQuantityInfoList | Warehouse inventory list | list |  |  | 
| - countryCode | Warehouse country code | string | 20 | e.g. CN, US | 
| - warehouseQuantity | Warehouse inventory quantity | long | 20 |  | 
| - clientTransitQuantity | In-transit quantity | long | 20 |  | 

### [#](https://developers.cjdropshipping.com#_2-2-query-private-inventory-sku-list-by-product-id-post) 2.2 Query Private Inventory SKU List By Product ID (POST)

 #### [#](https://developers.cjdropshipping.com#url-3) URL

 https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySkuListByProductId

#### [#](https://developers.cjdropshipping.com#curl-3) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySkuListByProductId' \
         --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
         --header 'Content-Type: application/json' \
         --data-raw '{
                "productId": "1234567890",
                "keyword": "black",
                "variantId": "9876543210"
         }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| productId | Product ID | string | Y | 200 | CJ product ID | 
| keyword | Search keyword | string | N | 200 | Fuzzy search by SKU/specification | 
| variantId | Variant ID | string | N | 200 | CJ variant ID | 

#### [#](https://developers.cjdropshipping.com#return-fields) Return Fields

 | Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| data | SKU inventory list | list |  |  | 
| merchantId | Merchant ID | string | 200 |  | 
| productId | Product ID | string | 200 |  | 
| variantId | Variant ID | string | 200 |  | 
| sku | SKU | string | 200 |  | 
| productName | Product name | string | 500 |  | 
| variantKey | Variant attributes | string | 500 |  | 
| variantValue1 | Variant value 1 | string | 200 |  | 
| variantValue2 | Variant value 2 | string | 200 |  | 
| variantValue3 | Variant value 3 | string | 200 |  | 
| bigImage | Variant image | string | 500 |  | 
| minStockPrice | Minimum inventory unit price | BigDecimal | (18,2) | Unit: USD | 
| maxStockPrice | Maximum inventory unit price | BigDecimal | (18,2) | Unit: USD | 
| warehouseQuantityInfoList | Warehouse inventory list | list |  | Same as 2.1 | 

### [#](https://developers.cjdropshipping.com#_2-3-query-private-inventory-sku-detail-page-post) 2.3 Query Private Inventory SKU Detail Page (POST)

 #### [#](https://developers.cjdropshipping.com#url-4) URL

 https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySkuDetailPage

#### [#](https://developers.cjdropshipping.com#curl-4) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySkuDetailPage' \
         --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
         --header 'Content-Type: application/json' \
         --data-raw '{
                "pageNum": 1,
                "pageSize": 20,
                "sku": "CJNS000000101AZ",
                "productId": "1234567890",
                "storageIds": ["US"],
                "availableStock": true
         }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| pageNum | Page number | integer | N | 20 | Default 1 | 
| pageSize | Page size | integer | N | 20 | Default 20 | 
| sku | SKU | string | N | 200 |  | 
| productId | Product ID | string | N | 200 |  | 
| keyword | Search keyword | string | N | 200 | Fuzzy search by SKU/product name | 
| orderCode | Stock order code | string | N | 200 | Source order code of private inventory | 
| storageIds | Warehouse ID list | list | N | 200 | e.g. CN, US | 
| availableStock | Only SKUs with available stock | boolean | N | 1 | true-yes | 
| pack | Is packaging product | boolean | N | 1 | true-yes | 
| serviceProd | Is service product | boolean | N | 1 | true-yes | 
| pod | Is POD product | boolean | N | 1 | true-yes | 
| skuList | SKU list | list | N |  | Exact query by multiple SKUs | 

#### [#](https://developers.cjdropshipping.com#return-fields-2) Return Fields

 | Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| pageSize/pageNumber/totalRecords/totalPages | Pagination fields | long | 20 | Same as 2.1 | 
| content | SKU detail list | list |  |  | 
| merchantId | Merchant ID | string | 200 |  | 
| sku | SKU | string | 200 |  | 
| variantId | Variant ID | string | 200 |  | 
| productId | Product ID | string | 200 |  | 
| productName | Product name | string | 500 |  | 
| storageId | Warehouse ID | string | 100 |  | 
| clientTransitQuantity | In-transit quantity | long | 20 |  | 
| clientAvailableQuantity | Available quantity | long | 20 |  | 
| clientLockQuantity | Locked quantity | long | 20 |  | 
| clientUseQuantity | Used quantity | long | 20 |  | 
| clientDisputeQuantity | Dispute quantity | long | 20 |  | 
| clientDisputeCompleteQuantity | Completed dispute quantity | long | 20 |  | 
| clientFreezeQuantity | Frozen quantity | long | 20 |  | 
| variantKey | Variant attributes | string | 500 |  | 
| bigImage | Variant image | string | 500 |  | 

### [#](https://developers.cjdropshipping.com#_2-4-query-private-inventory-batch-detail-by-sku-post) 2.4 Query Private Inventory Batch Detail By SKU (POST)

 #### [#](https://developers.cjdropshipping.com#url-5) URL

 https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySkuDetailListBySku

#### [#](https://developers.cjdropshipping.com#curl-5) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySkuDetailListBySku' \
         --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
         --header 'Content-Type: application/json' \
         --data-raw '{
                "sku": "CJNS000000101AZ",
                "orderCode": "SY230101000001",
                "storageIds": ["US"],
                "availableStock": true
         }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| sku | SKU | string | Y | 200 | Query SKU | 
| keyword | Search keyword | string | N | 200 | Fuzzy search | 
| orderCode | Stock order code | string | N | 200 | Source order code of private inventory | 
| storageIds | Warehouse ID list | list | N | 200 | e.g. CN, US | 
| availableStock | Only batches with available stock | boolean | N | 1 | true-yes | 

#### [#](https://developers.cjdropshipping.com#return-fields-3) Return Fields

 | Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| data | SKU batch detail list | list |  |  | 
| merchantId | Merchant ID | string | 200 |  | 
| sku | SKU | string | 200 |  | 
| orderCode | Stock order code | string | 200 | Source order code of private inventory | 
| storage | Warehouse name | string | 200 |  | 
| storageId | Warehouse ID | string | 100 |  | 
| unitPrice | Inventory unit price | integer | 20 | Subject to API return unit | 
| productId | Product ID | string | 200 |  | 
| orderQuantity | Order quantity | long | 20 |  | 
| clientTransitQuantity | In-transit quantity | long | 20 |  | 
| clientAvailableQuantity | Available quantity | long | 20 |  | 
| clientLockQuantity | Locked quantity | long | 20 |  | 
| clientUseQuantity | Used quantity | long | 20 |  | 
| clientDisputeQuantity | Dispute quantity | long | 20 |  | 
| clientDisputeCompleteQuantity | Completed dispute quantity | long | 20 |  | 
| clientFreezeQuantity | Frozen quantity | long | 20 |  | 

### [#](https://developers.cjdropshipping.com#_2-5-query-private-inventory-sku-flow-page-post) 2.5 Query Private Inventory SKU Flow Page (POST)

 #### [#](https://developers.cjdropshipping.com#url-6) URL

 https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySkuFlowByCondition

#### [#](https://developers.cjdropshipping.com#curl-6) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/product/stock/privateInventory/querySkuFlowByCondition' \
         --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
         --header 'Content-Type: application/json' \
         --data-raw '{
                "pageNum": 1,
                "pageSize": 20,
                "sku": "CJNS000000101AZ",
                "orderCode": "SY230101000001",
                "eventOrderCode": "ORDER230101000001",
                "storageId": "US",
                "recordId": "REC123456",
                "clientVisible": 1
         }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| pageNum | Page number | integer | N | 20 | Default 1 | 
| pageSize | Page size | integer | N | 20 | Default 20 | 
| sku | SKU | string | N | 200 | Query SKU flow | 
| orderCode | Stock order code | string | N | 200 | Source order code of private inventory | 
| eventOrderCode | Business order code | string | N | 200 | Order/business code that caused the inventory change | 
| storageId | Warehouse ID | string | N | 100 | e.g. CN, US | 
| unitPrice | Inventory unit price | integer | N | 20 | Subject to API return unit | 
| recordId | Flow record ID | string | N | 200 | Exact query by flow record | 
| clientVisible | Client visibility flag | integer | N | 1 | 1-visible, 0-invisible | 

#### [#](https://developers.cjdropshipping.com#return-3) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": {
        "pageSize": 20,
        "pageNumber": 1,
        "totalRecords": 1,
        "totalPages": 1,
        "content": [
            {
                "clientRecordId": "REC123456",
                "eventDesc": "Stock in",
                "changeQuantity": 10,
                "createDate": 1704067200000,
                "eventOrderCode": "ORDER230101000001",
                "orderCode": "SY230101000001",
                "storage": "US Warehouse",
                "storageId": "US",
                "clientAvailableQuantity": 100,
                "clientAvailableChangeQuantity": "+10"
            }
        ]
    },
    "requestId": "2b97f15603384fe4832e85617cf07d9c"
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| pageSize/pageNumber/totalRecords/totalPages | Pagination fields | long | 20 | Same as 2.1 | 
| content | SKU flow list | list |  |  | 
| clientRecordId | Client flow record ID | string | 200 |  | 
| eventDesc | Flow event description | string | 500 |  | 
| changeQuantity | Change quantity | long | 20 | Positive means increase, negative means decrease | 
| createDate | Created time | long | 20 | Timestamp | 
| eventOrderCode | Business order code | string | 200 | Order/business code that caused the inventory change | 
| eventOrderCodeType | Business order code type | integer | 20 | Subject to API enum return | 
| clientVisible | Client visibility flag | integer | 1 | 1-visible, 0-invisible | 
| orderCode | Stock order code | string | 200 | Source order code of private inventory | 
| storage | Warehouse name | string | 200 |  | 
| storageId | Warehouse ID | string | 100 |  | 
| unitPrice | Inventory unit price | integer | 20 | Subject to API return unit | 
| clientTransitQuantity | In-transit quantity | long | 20 |  | 
| clientAvailableQuantity | Available quantity | long | 20 |  | 
| clientLockQuantity | Locked quantity | long | 20 |  | 
| clientUseQuantity | Used quantity | long | 20 |  | 
| clientDisputeQuantity | Dispute quantity | long | 20 |  | 
| clientDisputeCompleteQuantity | Completed dispute quantity | long | 20 |  | 
| clientFreezeQuantity | Frozen quantity | long | 20 |  | 
| clientTransitChangeQuantity | In-transit quantity change | string | 50 | e.g. +1, -1 | 
| clientAvailableChangeQuantity | Available quantity change | string | 50 | e.g. +1, -1 | 
| clientLockChangeQuantity | Locked quantity change | string | 50 | e.g. +1, -1 | 
| clientUseChangeQuantity | Used quantity change | string | 50 | e.g. +1, -1 | 
| clientDisputeChangeQuantity | Dispute quantity change | string | 50 | e.g. +1, -1 | 
| clientDisputeChangeCompleteQuantity | Completed dispute quantity change | string | 50 | e.g. +1, -1 | 
| clientFreezeChangeQuantity | Frozen quantity change | string | 50 | e.g. +1, -1 | 
| skuDetailInfo | SKU inventory snapshot | object |  | Quantity after change for each inventory dimension | 

error

```
{
    "code": 1600100,
    "result": false,
    "message": "Param error",
    "data": null,
    "requestId": "2b97f15603384fe4832e85617cf07d9c"
}
```
### [#](https://developers.cjdropshipping.com#_2-6-query-warehouse-order-pictures-post) 2.6 Query Warehouse Order Pictures (POST)

 Query photos of orders being processed in the warehouse.

#### [#](https://developers.cjdropshipping.com#url-7) URL

 https://developers.cjdropshipping.com/api2.0/v1/storehouseCenterWeb/syncStorehouseVideoRequests

#### [#](https://developers.cjdropshipping.com#curl-7) CURL

 ```
curl --location 'https://developers.cjdropshipping.com/api2.0/v1/storehouseCenterWeb/syncStorehouseVideoRequests' \
     --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
     --header 'Content-Type: application/json' \
     --data '{
         "orderIdList": ["ORDER001", "ORDER002"]
     }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| orderIdList | Order ID list | List<String> | Y | - |  | 

#### [#](https://developers.cjdropshipping.com#return-4) Return

 success

```
{
    "code": 200,
    "data": [
        {
            "orderId": "ORDER001",
            "pictureJson": [
                {
                    "url": "https://example.com/pic1.jpg",
                    "type": "packing"
                }
            ]
        }
    ],
    "message": "success",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| orderId | Order ID | string | 200 |  | 
| pictureJson | Picture JSON list | Array | - |  | 

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
