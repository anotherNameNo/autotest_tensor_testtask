from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import requests
import functools
from time import sleep


def func_do_it(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(repr(func.__doc__))
        print(func.__name__, end=": ")
        func(*args, **kwargs)
        print("OK")

    return wrapper

class PageObject:

    def __init__(self, url="https://sbis.ru/"):
        self.driver = self.driver_init(url)
      
    def wait_element(self, xpath):
        "Получение элемента страницы с ожиданием"
        
        # последняя активаня вкладка
        self.driver.switch_to.window(self.driver.window_handles[-1])

        element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        return element
        
    @staticmethod
    def driver_init(url):
        "Инициализация webdriver"
        
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("start-maximized")
        # executable_path=r'chromedriver.exe') ???
        driver = webdriver.Chrome(options=options) 
        driver.get(url)    
        return driver

    def quit(self):
        "quit webdriver"
        
        self.driver.quit()
        return True

    def click_elem(self, xpath, space=False, end=False):
        "Получение элемента страницы и клик по нему"
        
        el = self.wait_element(xpath)
        if space:
            el.send_keys(Keys.SPACE)
        if end:
            el.send_keys(Keys.END)
        sleep(0.5)
        el.click()
        return True

    def get_url(self):
        "Получение url активной вкладки"
        
        return self.driver.current_url

    def get_title(self):
        "Получение title активной вкладки"
        
        return self.driver.title


class TestFirst:
    "От расположения методов зависит работоспсобность теста"

    @staticmethod
    def test_init_PageObject():
        "Создание PageObject"
        
        setattr(TestFirst, "first", PageObject())
        assert TestFirst.first


    @staticmethod
    def test_contact_click():
        "Поиск кнопки контактов и клик по этой кнопке"
        
        xpath = '//*[@id="wasaby-content"]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/ul/li[2]/a'
        assert TestFirst.first.click_elem(xpath)

    @staticmethod
    def test_banner_tenor_click():
        "Поиск банера Тензор и клик по нему"

        xpath = '//*[@id="contacts_clients"]/div[1]/div/div/div[2]/div/a/img'
        assert TestFirst.first.click_elem(xpath)

    @staticmethod
    def test_strong_into_people():
        "Проверка блока Сила в людях"

        xpath = '//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]'
        assert "сила в людях" in TestFirst.first.wait_element(xpath).text.lower()

    @staticmethod
    def test_strong_into_people_click():
        """Переход по ссылке в блоке сила в людях, https://tensor.ru/about"""

        xpath = '//*[@id="container"]/div[1]/div/div[5]/div/div/div[1]/div/p[4]/a'
        assert TestFirst.first.click_elem(xpath, space=True)
        sleep(0.5)
        assert TestFirst.first.get_url() == "https://tensor.ru/about"

    @staticmethod
    def test_size_img_into_job():
        "Проверка равенства размеров картинок в разделе Работаем"

        
        img = []
        for i in range(1, 5):
            xpath = f'//*[@id="container"]/div[1]/div/div[4]/div[2]/div[{i}]/a/div[1]/img'
            el = TestFirst.first.wait_element(xpath)
            img.append((el.rect['height'], el.rect['width']))

        assert len(set(img)) == 1

    @staticmethod
    def test_quit_PageObject():
        "quit webdriver"
        
        assert TestFirst.first.quit()
        
class TestSecond:
    "От расположения методов зависит работоспсобность теста"
    
    @staticmethod
    def test_init_PageObject():
        "Создание PageObject"
        
        setattr(TestSecond, "second", PageObject())
        assert TestSecond.second
        
    @staticmethod
    def test_contact_click():
        "Поиск кнопки контактов и клик по этой кнопке"
        
        xpath = '//*[@id="wasaby-content"]/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/ul/li[2]/a'
        assert TestSecond.second.click_elem(xpath)

    @staticmethod
    def test_region_and_partners(dist="Свердловская", city="Екатеринбург"):
        "Проверка на свой регион и список пратнеров"

        # Проверка своего региона
        xpath_1 = '//*[@id="container"]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/span/span'
        el = TestSecond.second.wait_element(xpath_1)
        sleep(0.5)
        assert dist in el.text

        # Проверка блока партнеров
        xpath_2 = '//*[@id="contacts_list"]/div/div[2]/div[2]/div/div[2]/div[1]/div[3]'
        el = TestSecond.second.wait_element(xpath_2)
        sleep(0.5)
        assert city in el.text

    @staticmethod
    def test_region_kamchat():
        """Изменить регион на Камчатский край\
        Проверить, что подставился выбранный регион, список партнеров\
        изменился, url и title содержат информацию выбранного региона"""

        # Открытие окна выбора реион
        xpath_1 = '//*[@id="container"]/div[1]/div/div[3]/div[2]/div[1]/div/div[2]/span/span'
        assert TestSecond.second.click_elem(xpath_1)


        # Выбор региона
        xpath_2 = '//*[@id="popup"]/div[2]/div/div/div/div/div[2]/div/ul/li[43]'
        assert TestSecond.second.click_elem(xpath_2)

        TestSecond.test_region_and_partners(dist="Камчатский",
                                            city="Петропавловск-Камчатский")

        assert "41" in TestSecond.second.get_url()
        assert "Камчатский" in TestSecond.second.get_title()

    @staticmethod
    def test_quit_PageObject():
        "quit webdriver"
        
        assert TestSecond.second.quit()


class TestThird:
    "От расположения методов зависит работоспсобность теста"
    
    @staticmethod
    def test_init_PageObject():
        "Создание PageObject"
        
        setattr(TestThird, "third", PageObject())
        assert TestThird.third

    @staticmethod
    def test_footer_download_click():
        "В Footer'e найти и перейти 'Скачать СБИС'"

        
        xpath = '//*[@id="container"]/div[2]/div[1]/div[3]/div[10]/ul/li[6]/a'
        assert TestThird.third.click_elem(xpath, end=True)

    @staticmethod
    def test_download_plagin():
        """Скачать СБИС Плагин для вашей для windows, \
        веб-установщик в папку с данным тестом"""

        # Плагин СБИС
        xpath_1 = '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div[2]'
        assert TestThird.third.click_elem(xpath_1)

        # windows
        xpath_2 = '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/div[1]'
        assert TestThird.third.click_elem(xpath_2)
      
        # скачать Веб-установщик
        xpath_3 = '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[2]/div/a'
        el = TestThird.third.wait_element(xpath_3)

        assert "Скачать" in el.text

        filesize = "".join(i for i in el.text if i.isdigit() or i in (".,"))
        setattr(TestThird, "filesize_in_MB", float(filesize))
        assert TestThird.filesize_in_MB > 0

        file_url = el.get_attribute("href")


        # Отправка GET-запроса на получение файла
        response = requests.get(file_url)
        response.raise_for_status()

        # Сохранение файла на диск
        setattr(TestThird, "filename", file_url.split("/")[-1])
        with open(TestThird.filename, 'wb') as file:
            file.write(response.content)

        assert TestThird.filename

    @staticmethod
    def test_is_plugin():
        "Убедиться, что плагин скачался"

        assert __import__("os").path.exists(TestThird.filename)

    @staticmethod
    def test_is_size_plugin():
        """Сравнить размер скачанного файла в мегабайтах. Он должен\
        совпадать с указанным на сайте"""

        filesize_in_bytes = __import__("os").path.getsize(TestThird.filename)
        filesize_in_MB = round(filesize_in_bytes/1024**2, 2)

        assert filesize_in_MB == TestThird.filesize_in_MB
    
    @staticmethod
    def test_quit_PageObject():
        "quit webdriver"
        
        assert  TestThird.third.quit()



def run_test(test_obj):
    "Запуск сценария тестирования"


    print("START", test_obj.__name__)
    for test in [i for i in test_obj.__dict__ if i.startswith("test")]:
        func_do_it(getattr(test_obj, test))()
    print("END", test_obj.__name__, end="\n\n")

    

if __name__ == "__main__":
    
    run_test(TestFirst)
    run_test(TestSecond)
    run_test(TestThird)




__import__("os").system("pause")

