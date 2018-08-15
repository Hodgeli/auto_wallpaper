# coding=utf-8
import random
import re
import requests
import win32api
import win32con
import win32gui


def get_img_id():
    search_url = 'https://alpha.wallhaven.cc/search?q=%s&purity=100&ratios=16x9&sorting=relevance&order=desc&page=%s'
    categories = ['nature', 'universe', 'car', 'HD wallpaper', 'fruit', 'animals', 'DC Comics', 'sword', 'samurai',
                  'digital art', 'anime', 'Naruto', 'artwork', 'space', 'planet', 'spaceship', 'futuristic',
                  'mountains', 'machine', 'robot', 'cyberpunk', 'metal', 'cat', 'helmet', 'Monkey D. Luffy',
                  'Roronoa Zoro']
    list_page_id = [1, 2, 3, 4, 5]
    search_url = search_url % (random.choice(categories), str(random.choice(list_page_id)))
    response = requests.get(search_url)

    rule = r'data-wallpaper-id="(.*?)" style'
    list_id = re.findall(rule, response.text)
    if len(list_id) >= 1:
        return random.choice(list_id)
    else:
        return 0


def download_img(id):
    base_url = 'https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.%s'
    down_path = "G:" + u"\壁纸\\"
    try:
        pic_path = down_path + id + '.jpg'
        img_url = base_url % (id, 'jpg')
        response = requests.get(img_url)
        if response.status_code == 404:
            pic_path = down_path + id + '.png'
            img_url = base_url % (id, 'png')
            response = requests.get(img_url)
            if response.status_code == 200:
                with open(pic_path, 'wb') as file:
                    file.write(response.content)
                return pic_path
            else:
                return 0
        elif response.status_code == 200:
            with open(pic_path, 'wb') as file:
                file.write(response.content)
            return pic_path
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
    while 1:
        img_id = get_img_id()
        if img_id != 0:
            pic_path = download_img(img_id)
            if pic_path != 0:
                set_wallpaper(pic_path)
                break
