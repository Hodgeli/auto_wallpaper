# coding=utf-8
import random
import re
import requests
import win32api
import win32con
import win32gui


def get_img_full_url():
    search_url = 'https://wallhaven.cc/search?q=%s&categories=111&purity=100&atleast=1600x900&ratios=16x9&sorting=favorites&order=desc&page=%s'
    categories = ['nature', 'universe', 'HD%20wallpaper', 'fruit', 'animals', 'DC%20Comics', 'sword', 'samurai',
                  'digital%20art', 'anime', 'Naruto', 'artwork', 'space', 'planet', 'spaceship', 'futuristic',
                  'mountains', 'machine', 'robot', 'cyberpunk', 'metal', 'cat', 'helmet', 'Monkey%20D.%20Luffy',
                  'Roronoa%20Zoro']
    list_page_id = [1, 2, 3, 4, 5]
    search_url = search_url % (random.choice(categories), str(random.choice(list_page_id)))
    response = requests.get(search_url)

    if response.status_code == 200:
        rule = r'class="preview" href="(.*?)"'
        list_full_url = re.findall(rule, response.text)
        if len(list_full_url) >= 1:
            return random.choice(list_full_url)
        else:
            return 0
    else:
        return 0


def download_img(img_full_url):
    down_path = "G:" + u"\壁纸\\"
    try:
        response = requests.get(img_full_url)

        if response.status_code == 200:
            rule = r'id="wallpaper" src="(.*?)"'
            img_final_url = re.findall(rule, response.text)[0]
            if img_final_url:
                img_name = str(img_final_url).split("/")[-1]
                pic_path = down_path + img_name

                response_img = requests.get(img_final_url)
                if response.status_code == 200:
                    with open(pic_path, 'wb') as file:
                        file.write(response_img.content)
                    return pic_path
                else:
                    return 0
            else:
                return 0
        else:
            return 0
    except:
        return 0


def set_wallpaper(path):
    # 打开指定注册表路径
    reg_key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 最后的参数:2拉伸,0居中,6适应,10填充,0平铺
    win32api.RegSetValueEx(reg_key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 最后的参数:1表示平铺,拉伸居中等都是0
    win32api.RegSetValueEx(reg_key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # 刷新桌面
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, win32con.SPIF_SENDWININICHANGE)


if __name__ == '__main__':
    flag = 0
    while flag < 5:
        img_full_url = get_img_full_url()
        if img_full_url != 0:
            pic_path = download_img(img_full_url)
            if pic_path != 0:
                set_wallpaper(pic_path)
                break
        else:
            flag += 1
