from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
import os
from bs4 import BeautifulSoup
from recruit_templates import templates

URL = "https://www.nationstates.net/page=activity/view=region.the_north_pacific/filter=move+founding"

list_num_inp = int(input("Enter the list number: "))
list_name_inp = str(input("Enter the list name: "))
template_name_inp = str(input("Enter the template key (Exec, Citizen, WA, NPA): "))

class HappeningstoList:
    def __init__(self, list_num, list_name, template) -> None:
        self.list_num = list_num
        self.list_name = list_name
        self.template = template
        self.options = Options()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.more_btn = '#reports > p > a'
        self.get_happenings()
    
    def interceptor(self, request) -> None:
        del request.headers['User-Agent']
        request.headers['User-Agent'] = 'TNP List Tool (by united_states_of_dictators)'

    def get_happenings(self) -> None:
        self.driver.request_interceptor = self.interceptor
        self.driver.get(URL)

        for _ in range(7):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll to the bottom of the page

            self.driver.implicitly_wait(10) #wait

            try:
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, self.more_btn))
                )
                button.click()
            except Exception as e:
                print(f"Exception: {e}")

            self.driver.implicitly_wait(5)

        with open('nse.html', 'wb') as file:
            file.write(self.driver.page_source.encode('utf-8'))
            file.close()

    def extract_happenings(self) -> list:
        happenings_lst = []
        with open('nse.html', 'rb') as file:
            f = file.read()
            soup = BeautifulSoup(f, features='lxml')
            reports_div = soup.find('div', id='reports')
            
            if reports_div:
                report_items = reports_div.find_all('li')

                for item in report_items:
                    time_tag = item.find('time')
                    nation_link = item.find('a', class_='nlink')
                    region_link = item.find('a', class_='rlink')

                    if time_tag and nation_link:
                        nation_name = nation_link.find('span', class_='nnameblock').get_text(strip=True)

                        if 'relocated' in item.get_text():
                            from_region = region_link.get_text(strip=True)
                            to_region = region_link.find_next('a', class_='rlink').get_text(strip=True)
                            msg = f"{nation_name} relocated from {from_region} to {to_region}"
                            happenings_lst.append(msg)
                            
                        else:
                            region_name = region_link.get_text(strip=True)
                            msg = f"{nation_name} was founded in {region_name}"
                            happenings_lst.append(msg)
        return happenings_lst

    def regex_parsing(self, lst: list) -> tuple:
        founded_pattern = re.compile(r'(?P<name>[A-Za-z0-9\s-]+) was founded in The North Pacific')
        relocated_pattern = re.compile(r'(?P<name>[A-Za-z0-9\s-]+) relocated from (?P<region>[A-Za-z0-9\s-]+) to The North Pacific')

        founded_names = []
        relocated_names = []

        for happening in lst:
            founded_matches = founded_pattern.match(happening)
            relocated_matches = relocated_pattern.match(happening)

            if founded_matches:
                founded_names.append(founded_matches.group('name'))

            if relocated_matches:
                relocated_names.append((relocated_matches.group('name')))

        return founded_names, relocated_names

    def execute(self):
        os.system('cls')
        nations_lst = []
        f, r = self.regex_parsing(self.extract_happenings())
        for nation in f:
            nations_lst.append(nation)
        for nation in r:
            nations_lst.append(nation)
        
        if self.template in templates.keys():
            tem_value = templates[self.template]
        
        nation_urls = '\n'.join([f"[*]https://www.nationstates.net/page=compose_telegram?tgto={nation_url.replace(' ', '_')}%2C%2Bregion%3Athe_north_pacific" for nation_url in nations_lst])

        template = f"""
[center][IMG]https://forum.thenorthpacific.org/images/seals/moha_seal.png[/IMG]
[B][big][big]List {self.list_num}: {self.list_name}[/big][/big][/center]

FOR INSTRUCTIONS ON HOW TO USE THIS TEMPLATE, SEE[/B] [URL]https://forum.thenorthpacific.org/topic/9067664/[/URL]

Remember to change the [Your Nation] at the end of the telegram to the name of your nation! [B]In order to collect accurate delivery report data, we ask that you please create a new template every time we send out a new list, instead of saving and reusing the template IDs.[/B]

To make your claim, please post below in this thread using this form:
[TABLE]
[TR]
[TD]Claim: (ex. 150-200)
Number of rows: (ex. 50)
Delivered:
Blocked:[/TD]
[/TR]
[/TABLE]
For "claim" put the range of rows you intend to complete, and for "number of rows" put how many rows total you have claimed. When you are finished with your rows, you MUST edit your post to fill in the "delivered" and "blocked" sections of the form. Otherwise, we will assume the rows were not completed and record that in the roster as such.

Oh, and before I forget, a favor. [B]Please be sure to claim the number of rows that you claim to be claiming![/B] If your number of rows claimed ends in zero, then the last digit of the end of the claimed rows range is the previous one regarding the last digit of the start of the claimed rows range. It is like adding 9 to the last digit of the start of the claimed rows range.

(DO NOT INCLUDE WHICH NATIONS BLOCKED YOUR TELEGRAM)

Please do skip obvious puppet nations. [b]Ensure that you do not telegram the same nation twice.[/b]

{tem_value}

[SPOILER="List"]
[list=1]
{nation_urls}
[/list]
[/SPOILER]
"""
        print(template)
        
e = HappeningstoList(list_num_inp, list_name_inp, template_name_inp)
e.execute()
