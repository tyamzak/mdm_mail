import requests
import json


def get_access_token() -> str:
    """アクセストークンを取得する関数

    Returns:
        str: アクセストークンを返します
    """

    #アクセストークンを取得する
    url = "https://URLURLtoken?grant_type=client_credentials"

    #Basic認証
    payload={}
    headers = {
    'Authorization': 'Basic aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #リクエストが失敗した場合、リクエストが成功したが期待したデータが得られなかった場合にエラーを出すようにしています。
    if response.status_code == requests.codes.ok:
        try:
            res = response.json()
            if res:
                token = res["access_token"]
                return token
        except Exception as e:
            print(f'レスポンスの処理で失敗しました　エラー:  {e}')
            return False
    else:
        print(f'get_acdess_token requests.getの結果がエラーでした エラーコード{response.status_code}')
        return False


def get_latest_report_id(token)-> str:
    """レポート世代を取得します

    Args:
        token (str): アクセストークン

    Returns:
        str: レポートid
    """
    #レポート世代を取得する

    url = "https://URLURL123456789/downloads/search"

    payload = json.dumps({
    "offset": 0,
    "page_size": 100
    })
    headers = {
    'Authorization': 'Bearer {token}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #リクエストが失敗した場合、リクエストが成功したが期待したデータが得られなかった場合にエラーを出すようにしています。
    if response.status_code == requests.codes.ok:
        try:
            res = response.json()
            if res:
                id = res["data"]["results"][0]["id"]
                return id
        except Exception as e:
            print(f'レスポンスの処理で失敗しました　エラー:  {e}')
            return False
    else:
        print(f'get_latest_report_id requests.getの結果がエラーでした エラーコード{response.status_code}')
        return False




def get_report_tocsv(token,id)->bool:
    """token id から、CSVをダウンロードし、保存します

    Args:
        token (str): トークン
        id (str): id

    Returns:
        bool: TrueもしくはFalse
    """

    #レポートを取得する

    headers = {
        'Authorization': f'Bearer {token}',
    }
    #リクエストが失敗した場合、リクエストが成功したが期待したデータが得られなかった場合にエラーを出すようにしています。
    response = requests.get(f'https://api.ap1.data.vmwservices.com/v1/reports/tracking/{id}/download', headers=headers)

    if response.status_code == requests.codes.ok:
        with open('C:UsersyoshidaDesktopapitest.csv', 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f'get_report_tocsv requests.getの結果がエラーでした エラーコード{response.status_code}')
        return False




def main():
    token = get_access_token()
    if token:
        id = get_latest_report_id(token)
    else:
        print('中断１')
        return

    if id:
        res = get_report_tocsv(token,id)
    else:
        print('中断２')
        return

    if res:
        print('処理が終了しました')
    else:
        print('中断３')

if __name__ == "__main__":
    main()