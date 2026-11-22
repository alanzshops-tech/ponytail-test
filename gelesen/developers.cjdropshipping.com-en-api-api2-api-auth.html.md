# 1 Authentication | CJ Docs

- Quelle: https://developers.cjdropshipping.com/en/api/api2/api/auth.html
- Abgerufen: 2026-08-09 17:47 UTC
- Sprache laut HTML: en-US · gemessen: Englisch (de 0 / en 100)
- Extraktion: trafilatura
- Zeichen: 9900
- Verfügbarkeit: keine Strukturdaten (JSON-LD) auf der Seite

---
# [#](https://developers.cjdropshipping.com#_1-authentication) 1 Authentication

 ## [#](https://developers.cjdropshipping.com#_1-authentication-2) 1 Authentication

 ### [#](https://developers.cjdropshipping.com#_1-1-get-access-token-post) 1.1 Get access token（POST）

 Token-based authentication, the life of an access-token is 180 days, and the life of a refresh-token is 180 days. You can obtain new a access-tokens with refresh-token when access-token expired. You need to obtain a new access-token when refresh-token expired.

Rate limit is consistent with other API endpoints: maximum 1 call per second (QPS = 1).


**Token Caching**: When the same account calls the Get Token endpoint multiple times within 24 hours, the returned accessToken and refreshToken remain consistent (server-side cache). The Refresh Token endpoint also returns the same cached token within the 24-hour window. After 24 hours or after an explicit logout, a new token will be generated.


#### [#](https://developers.cjdropshipping.com#url) URL

 https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken

#### [#](https://developers.cjdropshipping.com#curl) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/authentication/getAccessToken' \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "apiKey": "CJUserNum@api@xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| apiKey | CJ API Key | string | Y | 200 | [Get API Key (opens new window)](https://www.cjdropshipping.com/my.html#/authorize/API) | 

How to get API Key:

**Step 1**: If you haven't installed the **API** app under **Apps** yet, you need to install it first before you can get an API Key. Click **Apps** in the left navigation, expand it, then click **Install App** to open the App Store.

**Figure 1:** Expand the **Apps** menu in the left navigation and click **Install App** to open the App Store.

In the App Store, under the **Others** category, find **API** and click the icon on its right to install it. Once installed, a toast reading "Installed Successfully" appears in the top-right corner, and the icon on the **API** card turns into a green check mark. If it's already installed (icon already shows a green check mark), you can skip this step.

**Figure 2:** The **API** app under the **Others** category in the App Store has finished installing — a "Installed Successfully" toast appears in the top-right corner, and the **API** card shows a green check mark on the right.

**Step 2**: Go to [Get API Key (opens new window)](https://www.cjdropshipping.com/my.html#/authorize/API). On the **API** tab, click the **Add API** button.

**Figure 3:** In the CJ personal center, open the **API** tab. When no API has been authorized yet, the page shows the empty state "You haven't authorized any API yet." with an orange **Add API** button. Click **Add API** to start.

**Step 3**: In the **Add API** dialog, enter the **API Key Name**, select **API Key** in the **Type** dropdown, then click **Confirm**.

**Figure 4:** The **Add API** dialog. Required fields: **API Key Name** (e.g. "Your API Name"), **API Store Name** (checkbox "Same As API Key Name" is checked by default) and **Type**. Set **Type** to **API Key**, then click the orange **Confirm** button (or **Cancel** to abort).

**Step 4**: In the API list, find the record whose **Type** is **API Key**, then click the **Copy** icon in the **API Key & MCP Token** column to copy your API Key.

**Figure 5:** The **API** list. Columns: **Name**, **Type**, **API Key & MCP Token**, **Status**, **Updated Date**, **Action**. Locate the row whose **Type** is **API Key** (Status **Activated**); the token is masked (e.g. `CJ4******38`). Click the **Copy** icon next to the eye icon in the **API Key & MCP Token** column to copy the full API Key.


#### [#](https://developers.cjdropshipping.com#return) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": {
        "openId": 123456789,
        "accessToken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "accessTokenExpiryDate": "2021-08-18T09:16:33+08:00",
        "refreshToken": "f7edabe65c3b4a198b50ca8f969e36eb",
        "refreshTokenExpiryDate": "2022-02-07T09:16:33+08:00",
        "createDate": "2021-08-11T09:16:33+08:00"
    },
    "requestId": "8b3d9ea1-00c3-4d10-9e2b-d18041d98080",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| openId | Open Id | Long | 20 |  | 
| accessToken | access token | string | 200 |  | 
| accessTokenExpiryDate | access token expiry time | string | 200 | Default 15 days | 
| refreshToken | Refresh Token | string | 200 |  | 
| refreshTokenExpiryDate | Refresh Token expiry time | string | 200 | Default 180 days | 
| createDate | Created date | string | 200 |  | 

error

```
{
    "code": 1601000,
    "result": false,
    "message": "User not find",
    "data": null,
    "requestId": "a18c9793-7c99-42f9-970b-790eecdceba2",
    "success": false
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | Error code | int | 20 | Return to error codes | 
| result | Whether returned | boolean | 1 |  | 
| message | Return message | string | 200 |  | 
| data |  |  |  | Data return | 
| requestId | Request ID | string | 48 | For error inquiry | 

### [#](https://developers.cjdropshipping.com#_1-2-refresh-access-token-post) 1.2 Refresh access token（POST）

 An API security mechanism with which the expiry date of access token can be refreshed. The life of an access token is 15 days.

#### [#](https://developers.cjdropshipping.com#url-2) URL

 https://developers.cjdropshipping.com/api2.0/v1/authentication/refreshAccessToken

#### [#](https://developers.cjdropshipping.com#curl-2) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/authentication/refreshAccessToken' \
                --header 'Content-Type: application/json' \
                --data-raw '{
                    "refreshToken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                }'
```
| Parameter | Definition | Type | Required | Length | Note | 
|---|---|---|---|---|---|
| refreshToken | Refresh Token | string | Y | 80 |  | 

#### [#](https://developers.cjdropshipping.com#return-2) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": {
        "accessToken": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "accessTokenExpiryDate": "2021-08-18T09:16:33+08:00",
        "refreshToken": "f7edabe65c3b4a198b50ca8f969e36eb",
        "refreshTokenExpiryDate": "2022-02-07T09:16:33+08:00",
        "createDate": "2021-08-11T09:16:33+08:00"
    },
    "requestId": "8b3d9ea1-00c3-4d10-9e2b-d18041d98080",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| accessToken | access token | string | 200 |  | 
| accessTokenExpiryDate | access token Expiry Time | string | 200 | Default 15 days | 
| refreshToken | Refresh Token | string | 200 |  | 
| refreshTokenExpiryDate | Refresh Token Expiry Time | string | 200 | Default 180 days | 
| createDate | Created Date | string | 200 |  | 

error

```
{
    "code": 1600003,
    "result": false,
    "message": "Refresh token is failure",
    "data": null,
    "requestId": "0b20dc1a-0043-43a7-a7c0-51ca6c61d976",
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

### [#](https://developers.cjdropshipping.com#_1-3-logout-token-post) 1.3 Logout Token（POST）

 API security mechanism. After logging out, access token and refresh token will expire.

#### [#](https://developers.cjdropshipping.com#url-3) URL

 https://developers.cjdropshipping.com/api2.0/v1/authentication/logout

#### [#](https://developers.cjdropshipping.com#curl-3) CURL

 ```
curl --location --request POST 'https://developers.cjdropshipping.com/api2.0/v1/authentication/logout' \
                --header 'CJ-Access-Token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```
#### [#](https://developers.cjdropshipping.com#return-3) Return

 success

```
{
    "code": 200,
    "result": true,
    "message": "Success",
    "data": true,
    "requestId": "b1d3728d-8a29-417e-9983-6df9926aaa49",
    "success": true
}
```
| Field | Definition | Type | Length | Note | 
|---|---|---|---|---|
| code | error code | int | 20 | [Reference error code](https://developers.cjdropshipping.com/en/api/api2/standard/ps-code.html) | 
| result | Whether or not the return is normal | boolean | 1 |  | 
| message | return message | string | 200 |  | 
| data | return data | object |  | interface data return | 
| requestId | requestId | string | 48 | Flag request for logging errors | 

error

```
{
    "code": 1600001,
    "result": false,
    "message": "Authentication failed",
    "data": null,
    "requestId": "5aa2bb6e-42fa-4e0a-ae88-1833c2c1c883",
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
