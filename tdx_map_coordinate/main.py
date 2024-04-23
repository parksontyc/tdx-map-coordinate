import requests
import time
import re

def get_coordinates_from_address(address, token):
    url = f'https://tdx.transportdata.tw/api/advanced/V3/Map/GeoCode/Coordinate/Address/{address}?format=JSON'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # 假設 API 返回的 JSON 數據中包含緯度和經度信息
        print(data)
        match = re.search(r'POINT \(([-+]?\d*\.\d+) ([-+]?\d*\.\d+)\)', data[0]['Geometry'])
        if match:
            longitude = float(match.group(1))
            latitude = float(match.group(2))
            print("Longitude:", longitude)
            print("Latitude:", latitude)
            return latitude,longitude
        else:
            print("No match found.")
    else:
        print(f"Failed to fetch coordinates for address: {address}")
        return None, None

# 调用示例
addresses = ["110台北市信義區信義路五段7號", "台北市松山區敦化北路340號"]  # 添加更多地址到這個列表中
token = token  # 替換為你的 Bearer token

requests_per_second = 50
with open('output.csv','w',encoding='utf-8') as f:
  f.write('address,lat,lon\n')
  for address in addresses:
      latitude, longitude = get_coordinates_from_address(address, token)
      if latitude is not None and longitude is not None:
        print(f"The coordinates for {address} are: Latitude {latitude}, Longitude {longitude}")
        f.write(f'{address},{latitude},{longitude}\n')
      else:
          print("Failed to fetch coordinates.")
      # 控制每秒請求次數
      time.sleep(1 / requests_per_second)
