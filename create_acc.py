from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import re
import time,requests
op=webdriver.FirefoxOptions()
op.headless=1
driver=webdriver.Firefox(options=op)
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
res=requests.post(url_login, data=data, headers=headers) #Login
res=requests.get('https://shophoangquyet.com/home').text
total_acc=int(res.split('<h2 class="text-sm font-bold text-truncate hover:whitespace-normal">Acc Free Fire Hquyết</h2>')[1].split('/span> ')[0].split('500">')[1].split('<')[0])
if total_acc%16==0: page=total_acc//16
else: page=(total_acc//16)+1
list_ms=[]
for intpage in range(1,page+1):
    driver.get(f'https://shophoangquyet.com/tai-khoan/free-fire-seven-nuoc-ngoai?page={intpage}')
    time.sleep(1.5)
    html=driver.page_source
    split_html=html.split(' <div id="app" data-v-app=""><section><div class="ant-spin-nested-loading css-eq3tly')[1].split('hover:text-white text-sm font-Inter font-medium transition-all duration-300 relative top-[2px]"><i class="fas fa-arrow-right"></i></a></li></ul></div></div></div></section></div>')[0]
    soup=BeautifulSoup(split_html, 'html.parser')
    result=soup.find_all(class_="ant-ribbon-text")
    cnt=0
    for i in result: 
        if cnt%2==0:
            tx=i.get_text()
            list_ms+=[tx.split('MS:')[1].strip()]
        cnt+=1
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
#Get listacc
res=requests.post('https://khonickgiare.vn/model/ctv/listaccount',data=data, headers=headers)
total_records=int(res.json()['recordsTotal'])
data['length']=total_records
res=requests.post('https://khonickgiare.vn/model/ctv/listaccount',data=data, headers=headers)
json_data=res.json()
def find_ind(ms):
    for i in range(len(list_ms)):
        if list_ms[i]==ms:
            return i+1
    return 0
for uid in json_data['data']:
    st_acc=1
    ms_acc=0
    try:
        ms_acc=uid[3].split('MS:')[1].split(' ')[0].strip()
    except: pass
    if ms_acc:
        ind=find_ind(ms_acc)
        if not ind: continue
        list_ms.pop(ind-1)
for tab in list_ms:
    driver.execute_script(f"window.open('https://shophoangquyet.com/tai-khoan/thong-tin/{tab}', '_blank');")
    time.sleep(1)
list_tab=driver.window_handles
for i, flow in enumerate(list_tab[1:][::-1]):
    driver.switch_to.window(flow)
    time.sleep(1)
    html=driver.page_source
    split_html=html.split('  const ITEM_DATA = {{"code":"{}"}};'.format(list_ms[i]))[1].split('<button type="button" data-te-ripple-init="" data-')[0]
    soup=BeautifulSoup(split_html, 'html.parser')
    el=soup.find(class_="text-[18px] md:text-[24px] text-primary").get_text()
    price=el.split("Giá:")[1].split('₫')[0].replace('.','')
    price=int(price)+100000
    fimg=soup.find("img", class_="h-[200px] w-full cursor-pointer rounded-lg md:h-[300px]").get('src')
    login=soup.find(class_='btn btn-sm btn-primary inline-flex items-center capitalize').get_text().strip()
    msg=split_html.split('"pills-tabContentHorizontal">')[1].split('data-caption="Image #1">')[0]
    img=soup.find_all('img', attrs={'data-src': True})
    msg1=msg.split('<p>')[1].split('</p>')[0]
    list_img=[]
    for ig in img:
        list_img+=[ig['data-src']]
    list_img=['https://shophoangquyet.com'+fimg]+list_img
    print(f"Task thứ {i+1}",price,login,msg1,list_ms[i])
    url="https://khonickgiare.vn/model/ctv/account"
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://khonickgiare.vn/ctv/subcategory/account/list/57",
        "Cookie": cookie,  
    }
    data={
        "type_category": "tai-khoan-free-fire",
        "action": "add",
        "taikhoan": f"LH-Zalo, MS:{list_ms[i]}",
        "matkhau": "LH-Zalo",
        "mota": msg1,
        "phuongthucdangnhap": login,
        "cash": price,
        "sale": "0"
    }
    files={}
    for i, image_url in enumerate(list_img):
        image_response=requests.get(image_url)
        if image_response.status_code==200:
            file_name=f"image_{i+1}.jpg"
            files[f"image[{i}]"]=(file_name, image_response.content, "image/jpeg")
        else:
            print(f"Không thể tải ảnh từ URL: {image_url}")
    response=requests.post(url, headers=headers, data=data, files=files) # Up acc
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
if not len(list_ms): print("Hiện tại chưa có account nào mới")
driver.quit()
