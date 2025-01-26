import requests,time
#Username, Password
username=''
password=''
url_login='https://khonickgiare.vn/model/login'
res=requests.get('https://khonickgiare.vn/tai-khoan/tai-khoan-free-fire')
csrf_token=res.text.split('csrf_token = "')[1].split('"')[0]
cookie=res.headers['set-cookie']
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Cookie": cookie,  
}
data={
    'csrf_token': csrf_token,
    'username': username,
    'password': password
}
res=requests.post(url_login, data=data, headers=headers)

data = {
    "draw": 1,
    "start": 0,
    "length": 1,
    "search[value]": "",
    "search[regex]": "false",
    "type": "tai-khoan-free-fire",
}
columns_json = {}
for i in range(10):
    columns_json[f"columns[{i}][data]"] = i
    columns_json[f"columns[{i}][name]"] = ""
    columns_json[f"columns[{i}][searchable]"] = "true"
    columns_json[f"columns[{i}][orderable]"] = "true"
    columns_json[f"columns[{i}][search][value]"] = ""
    columns_json[f"columns[{i}][search][regex]"] = "false"
data.update(columns_json)
url_del='https://khonickgiare.vn/model/ctv/account'
def del_acc(id_account):
    data_del={
        'action': 'delete',
        'id': id_account
    }
    res=requests.post(url_del,data=data_del, headers=headers)
    return res.json()['status']
def check_acc(ms):
    return requests.get(f'https://shophoangquyet.com/tai-khoan/thong-tin/{ms}').status_code==200
while True:
    res=requests.post('https://khonickgiare.vn/model/ctv/listaccount',data=data, headers=headers)
    total_records=int(res.json()['recordsTotal'])
    data['length']=total_records
    res=requests.post('https://khonickgiare.vn/model/ctv/listaccount',data=data, headers=headers)
    json_data=res.json()
    for uid in json_data['data']:
        st_acc=1
        ms_acc=0
        try:
            ms_acc=uid[3].split('MS:')[1].split(' ')[0].strip()
        except: pass
        if ms_acc: st_acc=check_acc(ms_acc)
        if st_acc:
            print(f'MS {ms_acc} - Chưa được bán')
        else:  
            print(f'MS {ms_acc} - Đã được bán => Tiến hành xóa')
            print(del_acc(uid[0]))
    time.sleep(1)
