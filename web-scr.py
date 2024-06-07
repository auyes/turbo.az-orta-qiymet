import requests
from bs4 import BeautifulSoup

def urlt(turbo, x): 
    turbo1 = turbo[0:28]
    turbo2 = turbo[29:]
    turbo = turbo1+str(x)+turbo2
    # url = f'https://turbo.az/autos?page=5&q%5Bavailability_status%5D=&q%5Bbarter%5D=0&q%5Bcrashed%5D=1&q%5Bcurrency%5D=azn&q%5Bengine_volume_from%5D=&q%5Bengine_volume_to%5D=&q%5Bfor_spare_parts%5D=0&q%5Bloan%5D=0&q%5Bmake%5D%5B%5D=23&q%5Bmileage_from%5D=&q%5Bmileage_to%5D=&q%5Bmodel%5D%5B%5D=&q%5Bmodel%5D%5B%5D=946&q%5Bonly_shops%5D=&q%5Bpainted%5D=1&q%5Bpower_from%5D=&q%5Bpower_to%5D=&q%5Bprice_from%5D=&q%5Bprice_to%5D=&q%5Bregion%5D%5B%5D=&q%5Bsort%5D=&q%5Bused%5D=&q%5Byear_from%5D=2004&q%5Byear_to%5D=2008'
    url = turbo
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    prices = soup.find_all('div', class_='product-price') #class-i product-price olan butun div-leri tapsin
    title = soup.find('div', class_='products-i__name products-i__bottom-text') #avtomobilin adi (avtomobilin adin duzgun cixarmir, BMW 5 series secende, BMW 540 kimi ad gelir)
    years = soup.find_all('div', class_='products-i__attributes products-i__bottom-text') #avtomobilin ili

    # total_price = sum([int(price.get_text().replace(' ', '').replace('AZN', '').replace('$', '')) for price in prices]) #Elave edilmeli: dollar isaresi varsa, hemin qiymeti hesablamasin !!!
    total_price = 0
    average = 0
    for price in prices:
        if 'AZN' in price.get_text(): #qiymet azn ile olanda hesablasin
            total_price += int(price.get_text().replace(' ', '').replace('AZN', ''))
            average += 1

    average_price = total_price / average # orta qiymet cixarilir

    total_year = sum([int(year.get_text()[0:4]) for year in years])
    average_year = total_year / len(years) #orta il cixarilir

    return average_price, len(prices), title, average_year

i=0
a=0
say = 0
il = 0
z=[]

turbo = input('Unvani daxil et: ') #sehifenin unvani
d = int(input('Ne qeder sehife yoxlasin: ')) #sehife sayi
d+=1

def urlcixaran(turbo): 
    url = turbo
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    sehifeNomresi = soup.find('span', class_='page current')
    hazirkiSehifeNomresi = sehifeNomresi.next_element.next_element.next_element.next_element.get('href')
    turbo = url[0:16] + hazirkiSehifeNomresi
    return turbo

turbo = urlcixaran(turbo)

for x in range(1,d): #necenci sehifeden necenci sehifeye kimi hesablasin
    say += 1
    i = i + int(urlt(turbo, x)[0])
    a = a + int(urlt(turbo, x)[1])
    il = il + int(urlt(turbo, x)[3])
    z.append(urlt(turbo, x))
    if x == 1:
        ad = urlt(turbo, x)[2].get_text() #avtomobilin adin ad deyisenine elave edir

print (f'{ad} ucun orta qiymet {int(i/say)}, orta buraxilis ili {int(il/say)}, umumi say {a}')
# print(i, '\n', a, '\n', z)