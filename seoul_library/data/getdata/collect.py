# 데이터 수집
# pip install xlrd
# pip install openpyxl
import requests
import json
import xml.etree.ElementTree as et
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from mysql import data_save

def library_location():
    '''
    서울시 공공도서관 위치 정보
    '''
    key = '4976726e4d65756a313131516a417045'
    xml = f'http://openapi.seoul.go.kr:8088/{key}/xml/SeoulPublicLibraryInfo/1/192/'
    resp = requests.get(xml)
    tree = et.fromstring(resp.text)
    row = tree.findall('row')

    dict_lib = dict()
    for i in range(len(row)):
        lib_name = row[i].find('LBRRY_NAME').text
        lib_lat = row[i].find('XCNTS').text
        lib_lng = row[i].find('YDNTS').text
        lib_gu = row[i].find('CODE_VALUE').text
        dict_lib[lib_name] = [lib_gu, lib_lat, lib_lng]

    df = pd.DataFrame(dict_lib)
    df = df.transpose()
    df.reset_index(inplace=True)
    df.columns = ['도서관', '자치구', '위도', '경도']
    df = df[['자치구', '도서관', '위도', '경도']]

    return df

def gu_border():
    '''
    서울시 자치구별 경계 정보
    '''
    pass

def gu_libraries():
    '''
    서울시 자치구별 공공도서관 통계
    '''
    target_url = 'https://www.libsta.go.kr/statistics/public/main'
    service = Service('../drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(target_url)
    sleep(5)
    si = driver.find_element(By.CSS_SELECTOR, '#libraryLocal > option:nth-child(2)')
    si.click()
    sleep(5)
    btn = driver.find_element(By.ID, 'libraryBtn')
    btn.click()
    sleep(8)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.select('#libraryTbl')
    tr = table[0].select('tbody > tr')

    df = pd.DataFrame(columns=['자치구', '2017', '2018', '2019', '2020', '2021'])
    # 합계 태그 제거
    for i in range(len(tr) - 1):
        gu = tr[i].select_one('td:nth-child(2)').text
        cnt_2017 = tr[i].select_one('td:nth-child(3)').text
        cnt_2018 = tr[i].select_one('td:nth-child(4)').text
        cnt_2019 = tr[i].select_one('td:nth-child(5)').text
        cnt_2020 = tr[i].select_one('td:nth-child(6)').text
        cnt_2021 = tr[i].select_one('td:nth-child(7)').text
        new_row = [gu, cnt_2017, cnt_2018, cnt_2019, cnt_2020, cnt_2021]
        df.loc[i] = new_row
    # 정수 변환
    df[['2017', '2018', '2019', '2020', '2021']] = df[['2017', '2018', '2019', '2020', '2021']].applymap(
        lambda x: int(x))
    return df

def gu_materials_per():
    '''
    서울시 자치구별 1관당 자료 통계
    '''
    target_url = 'https://www.libsta.go.kr/statistics/public/main'
    service = Service('../drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(target_url)
    sleep(5)
    select = driver.find_element(By.CSS_SELECTOR, '#bookLocal > option:nth-child(2)')
    select.click()
    sleep(2)
    finder = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[8]/div[1]/span/button')
    finder.click()
    sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    trs = soup.select('#bookTbl > tbody > tr')
    tds = list()
    for tr in trs:
        td = tr.select('td')
        tds.append(td)
    dict_gu_books = dict()
    for td in tds:
        gu_name = td[1].text
        gu_books_2017 = td[2].text
        gu_books_2018 = td[3].text
        gu_books_2019 = td[4].text
        gu_books_2020 = td[5].text
        gu_books_2021 = td[-1].text
        dict_gu_books[gu_name] = [gu_books_2017, gu_books_2018, gu_books_2019, gu_books_2020, gu_books_2021]
    del dict_gu_books['84,278']  # 합계 행 삭제

    df = pd.DataFrame(dict_gu_books, index=['2017', '2018', '2019', '2020', '2021'])
    df = df.transpose()
    df.reset_index(inplace=True)
    df.rename(columns={'index': '자치구'}, inplace=True)
    df[['2017', '2018', '2019', '2020', '2021']] = df[['2017', '2018', '2019', '2020', '2021']].applymap(
        lambda x: float(x.replace(',', '')))

    return df

def gu_population_per():
    '''
    서울시 자치구별 1관당 인구 통계
    '''
    target_url = 'https://www.libsta.go.kr/statistics/public/main'
    service = Service('../drivers/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    sleep(3)
    driver.get(target_url)
    sleep(3)
    dosi = driver.find_element(By.CSS_SELECTOR, '#peopleLocal > option:nth-child(2)')
    dosi.click()
    sleep(3)
    sel = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/section/div/div[20]/div[1]/span/button')
    sel.click()
    sleep(10)

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    library_peo = soup.select('#peopleTbl > tbody > tr')

    peo_list = list()
    for lists in library_peo:
        ele = lists.select('td')
        peo_list.append(ele)

    gu_dict = dict()
    for peo in peo_list:
        gu_name = peo[1].text
        gu_people_2017 = peo[2].text
        gu_people_2018 = peo[3].text
        gu_people_2019 = peo[4].text
        gu_people_2020 = peo[5].text
        gu_people_2021 = peo[-1].text
        gu_dict[gu_name] = [gu_people_2017, gu_people_2018, gu_people_2019, gu_people_2020, gu_people_2021]
        # print(gu_dick)
    del gu_dict['61,609']
    df = pd.DataFrame(gu_dict, index=['2017', '2018', '2019', '2020', '2021'])
    df = df.transpose()
    df.reset_index(inplace=True)
    df.rename(columns={'index': '자치구'}, inplace=True)
    df[['2017', '2018', '2019', '2020', '2021']] = df[['2017', '2018', '2019', '2020', '2021']].applymap(
        lambda x: float(x.replace(',', '')))

    return df

def gu_librarybudget():
    '''
    서울시 자치구별 공공도서관 예산
    '''
    df = pd.read_excel('rawdata/gu_librarybudget.xlsx')
    df.drop(['개소', '자료수', '자료수.1', '자료수.2', '도서관 방문자수', '자료실 이용자수', '직원수', '직원수.1', '직원수.2'], axis=1, inplace=True)
    df.drop(0, inplace=True)
    df.rename(columns={'기간':'연도'}, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df[df['자치구'] != '합계']
    df[['좌석수', '연간대출 책수', '예산']] = df[['좌석수', '연간대출 책수', '예산']].applymap(lambda x: int(x))
    return df

def library_users():
    '''
    서울시 공공도서관 회원 및 이용자 통계
    '''
    start = 2017
    end = 2019

    df = pd.DataFrame(columns=['코드', '자치구', '구분', '도서관명', '설립연도', '어린이회원', '청소년회원', '성인회원', '방문자수', '주소', '설립기관', '연도'])
    for i in range(start, end + 1):
        url = f'https://www.libsta.go.kr/statistics/stat/getlibraryexcelstatinfo?lib_gubun=LIBTYPE000002&stat_gubun=MCST_STBL_0000003710%7CMCST_STBL_0000003738&start_year={i}&end_year={i}&local_code=11'
        resp = requests.get(url)
        lib_code_list = resp.json()['lib_code_list']
        info = resp.json()['stat_info']
        data = list()
        for code in lib_code_list:
            data.extend(info[code])
        df_temp = pd.json_normalize(data)
        gugun = list()
        for sigugun in df_temp['SIGUGUN']:
            gugun.append(sigugun[3:])
        df_temp['GUGUN'] = gugun
        df_temp['YEAR'] = str(i)
        # 필요한 데이터만 가져오기
        df_temp = df_temp[
            ['LIB_CODE', 'GUGUN', 'LIB_GUBUN_NM', 'LIB_NAME', 'ESTABLISH', 'COL_1', 'COL_2', 'COL_3', 'COL_4', 'ADDR',
             'FOUND_NM', 'YEAR']]
        # 컬럼명 변경
        df_temp.columns = ['코드', '자치구', '구분', '도서관명', '설립연도', '어린이회원', '청소년회원', '성인회원', '방문자수', '주소', '설립기관', '연도']
        df = pd.concat([df, df_temp], ignore_index=True)
    df[['어린이회원', '청소년회원', '성인회원', '방문자수']] = df[['어린이회원', '청소년회원', '성인회원', '방문자수']].applymap(lambda x: int(x))
    return df

def library_rent():
    '''
    서울시 공공도서관 대출자 통계
    (전자자료 제외, 인쇄자료만)
    '''
    # 대출자수(전자자료는 제외)
    start = 2017
    end = 2019

    df = pd.DataFrame(columns=['코드', '자치구', '구분', '도서관명', '어린이회원', '청소년회원', '성인회원', '주소', '설립기관', '연도'])
    for i in range(start, end + 1):
        url = f'https://www.libsta.go.kr/statistics/stat/getlibraryexcelstatinfo?lib_gubun=LIBTYPE000002&stat_gubun=MCST_STBL_0000003711%7CMCST_STBL_0000003739&start_year={i}&end_year={i}&local_code=11'
        resp = requests.get(url)
        lib_code_list = resp.json()['lib_code_list']
        info = resp.json()['stat_info']
        data = list()
        for code in lib_code_list:
            data.extend(info[code])
        df_temp = pd.json_normalize(data)
        gugun = list()
        for sigugun in df_temp['SIGUGUN']:
            gugun.append(sigugun[3:])
        df_temp['GUGUN'] = gugun
        df_temp['YEAR'] = str(i)
        # 필요한 데이터만 가져오기
        df_temp = df_temp[
            ['LIB_CODE', 'GUGUN', 'LIB_GUBUN_NM', 'LIB_NAME', 'COL_1', 'COL_2', 'COL_3', 'ADDR', 'FOUND_NM', 'YEAR']]
        # 컬럼명 변경
        df_temp.columns = ['코드', '자치구', '구분', '도서관명', '어린이회원', '청소년회원', '성인회원', '주소', '설립기관', '연도']
        df = pd.concat([df, df_temp], ignore_index=True)
    df[['어린이회원', '청소년회원', '성인회원']] = df[['어린이회원', '청소년회원', '성인회원']].applymap(lambda x: int(x))
    return df

def gu_population():
    '''
    서울시 자치구별 인구 통계
    '''
    df = pd.read_excel("rawdata/gu_population.xls", header=0)

    df = df.fillna(method='ffill')
    df = df.loc[:, ['기간', '자치구', '인구']]

    year_2017 = df['기간'] == '2017'
    df_year_2017 = df[year_2017]
    df_year_2017 = df_year_2017.drop(['기간'], axis=1)
    df_year_2017.set_index('자치구', inplace=True)
    # print(df_year_2017)

    year_2018 = df['기간'] == '2018'
    df_year_2018 = df[year_2018]
    df_year_2018 = df_year_2018.drop(['기간'], axis=1)
    df_year_2018.set_index('자치구', inplace=True)

    year_2019 = df['기간'] == '2019'
    df_year_2019 = df[year_2019]
    df_year_2019 = df_year_2019.drop(['기간'], axis=1)
    df_year_2019.set_index('자치구', inplace=True)

    year_2020 = df['기간'] == '2020'
    df_year_2020 = df[year_2020]
    df_year_2020 = df_year_2020.drop(['기간'], axis=1)
    df_year_2020.set_index('자치구', inplace=True)

    year_2021 = df['기간'] == '2021'
    df_year_2021 = df[year_2021]
    df_year_2021 = df_year_2021.drop(['기간'], axis=1)
    df_year_2021.set_index('자치구', inplace=True)

    # df_year_2017에 열로 데이터를 붙인 후 열 이름 변경
    df = pd.concat([df_year_2017, df_year_2018, df_year_2019, df_year_2020, df_year_2021], axis=1)
    df.columns = ['2017', '2018', '2019', '2020', '2021']
    df = df.drop(['합계'], axis=0)
    df.reset_index(inplace=True)

    df[['2017', '2018', '2019', '2020', '2021']] = df[['2017', '2018', '2019', '2020', '2021']].applymap(
        lambda x: int(x))
    return df

def gu_youth_population():
    '''
    서울시 자치구별 청소년 통계
    '''
    df = pd.read_excel('rawdata/gu_youth_population.xlsx')
    df.drop(['9세-24세', '9세-24세.1', '학령인구', '학령인구.1'], axis=1, inplace=True)
    df.columns = ['연도', '자치구', '총인구', '청소년합계', '청소년구성비']
    df.drop(0, inplace=True)
    df = df[df['자치구'] != '합계']
    df.reset_index(drop=True, inplace=True)
    df[['총인구', '청소년합계', '청소년구성비']] = df[['총인구', '청소년합계', '청소년구성비']].applymap(lambda x: float(x))
    return df

def gu_averageincome():
    '''
    서울시 자치구별 소득 통계
    '''
    ppl = pd.read_excel('rawdata/gu_income.xlsx', header=0)
    ppl = ppl.fillna(method='ffill')
    for i in range(2017, 2021):
        for j in range(2, 8):
            ppl = ppl.drop([f'{i}.{j}'], axis=1)
    ppl.rename(columns={'행정구역(시군구)별(2)': '자치구', '2017': '2017_ppl', '2017.1': '2017_income',
                        '2018': '2018_ppl', '2018.1': '2018_income',
                        '2019': '2019_ppl', '2019.1': '2019_income',
                        '2020': '2020_ppl', '2020.1': '2020_income'}, inplace=True)

    mask = (ppl['행정구역(시군구)별(1)'] == '서울')
    df = ppl[mask]
    df.set_index('자치구', inplace=True)
    df.drop(['행정구역(시군구)별(1)'], axis=1, inplace=True)
    for i in range(2017, 2021):
        df[f'{i}'] = df[f'{i}_income'] / df[f'{i}_ppl'] * 1000000
        df[f'{i}'].astype('int')
    df = df.iloc[:, 8:]
    df.drop('소계', inplace=True)
    df.reset_index(inplace=True)
    df[['2017', '2018', '2019', '2020']] = df[['2017', '2018', '2019', '2020']].applymap(lambda x: int(x))
    return df

def gu_satisfaction():
    '''
    서울시 자치구별 생활환경 만족도 통계
    '''
    sat2017 = pd.read_excel('rawdata/gu_satisfaction_2017.xls', header=0)
    sat2018 = pd.read_excel('rawdata/gu_satisfaction_2018.xls', header=0)
    sat2019 = pd.read_excel('rawdata/gu_satisfaction_2019.xls', header=0)
    sat2020 = pd.read_excel('rawdata/gu_satisfaction_2020.xls', header=0)

    sat_list = [sat2017, sat2018, sat2019, sat2020]
    year_list = [2017, 2018, 2019, 2020]

    # 필요없는 데이터 제거하고 데이터프레임 결합에 대비해 컬럼명 수정
    for i in range(4):
        sat_list[i].fillna(method='ffill')
        sat_list[i].drop(sat_list[i].index[0:35], inplace=True)
        sat_list[i].drop(sat_list[i].columns[[0, 1]], axis=1, inplace=True)
        sat_list[i].reset_index(drop=True, inplace=True)
        sat_list[i]['연도'] = str(year_list[i])
    df = pd.concat([sat_list[0], sat_list[1], sat_list[2], sat_list[3]], ignore_index=True)
    df.rename(columns={'분류': '자치구'}, inplace=True)
    return df

def gu_household():
    '''
    서울시 자치구별 가구원수 통계
    '''
    df = pd.read_excel('rawdata/gu_household.xls', header=1)
    df.drop(0, inplace=True)
    df.rename(columns={'기간': '연도', '구분': '자치구'}, inplace=True)
    df.sort_values(by='자치구', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

def gu_ages():
    '''
    서울시 연령대별 생활인구 통계
    '''
    gu_code = pd.read_csv('rawdata/gu_code.csv', encoding='cp949', skiprows=1)
    gu_code.columns = ['자치구코드', '자치구명']
    gu_code['자치구코드'] = gu_code['자치구코드'].apply(lambda x: str(x)[:5])
    gu_code.sort_values(by='자치구코드', inplace=True)

    gu_people = pd.read_csv('rawdata/gu_people.csv', encoding='cp949')
    columns = gu_people.columns[1:]
    gu_people.drop('여자70세이상생활인구수', inplace=True, axis=1)
    gu_people.columns = columns
    gu_people = gu_people[(gu_people.index == 20191231) & (gu_people['시간대구분'] == 23)]
    gu_people.sort_values(by='자치구코드')
    gu_people['자치구코드'] = gu_code['자치구명'].values
    gu_people.drop('시간대구분', axis=1, inplace=True)
    gu_people.rename(columns={'자치구코드': '자치구'}, inplace=True)
    gu_people.sort_values(by='자치구', inplace=True)
    gu_people.reset_index(inplace=True, drop=True)

    df = gu_people[['자치구', '총생활인구수']]
    # df['어린이'] = [gu_people.iloc[i, [2, 16]].sum() for i in range(len(gu_people))]
    # df['10대'] = [gu_people.iloc[i, [3, 4, 17, 18]].sum() for i in range(len(gu_people))]
    df['10이하'] = [gu_people.iloc[i, [2, 3, 4, 16, 17, 18]].sum() for i in range(len(gu_people))]
    df['2030대'] = [gu_people.iloc[i, [5, 6, 7, 8, 19, 20, 21, 22]].sum() for i in range(len(gu_people))]
    df['4050대'] = [gu_people.iloc[i, [9, 10, 11, 12, 23, 24, 25, 26]].sum() for i in range(len(gu_people))]
    df['60이상'] = [gu_people.iloc[i, [13, 14, 15, 27, 28, 29]].sum() for i in range(len(gu_people))]
    return df

def gu_disadv_budget():
    '''
    자치구별 취약계층 지원 예산 (2017-2019)
    '''
    df = pd.read_excel('rawdata/gu_disadv_budget.xlsx', header=0)
    df.fillna(method='ffill')
    for i in [3, 4, 5, 7, 8, 9, 11, 12, 13]:
        df = df.drop([f'Unnamed: {i}'], axis=1)
    df = df.drop([0, 1, 2, 185], axis=0)

    for i in range(2017, 2020):
        df[i] = df[i].map(lambda x: int(x.replace(',', '')))
    df = df.groupby('지역오름차순').sum()
    df = df.rename(index=lambda x: x.replace('서울 ', ''))
    df.reset_index(drop=False, inplace=True)
    df.rename(columns={'지역오름차순': '자치구'}, inplace=True)
    return df


def gu_disadv_users():
    '''
    자치구별 취약계층 이용자수 (2019)
    '''
    df = pd.read_excel('rawdata/gu_disadv_users.xlsx', header=0)
    df.fillna(method='ffill')
    df = df.drop([0, 1, 184], axis=0)
    df = df.drop(['도서관명', 2017, 'Unnamed: 3', 'Unnamed: 4', 2018, 'Unnamed: 6', 'Unnamed: 7'], axis=1)
    df.columns = ['자치구', '2019_장애인', '2019_노인', '2019_다문화']
    df.set_index('자치구', inplace=True)
    df = df.applymap(lambda x: int(x.replace(',', '')))
    df['2019'] = df.sum(axis=1)
    df.reset_index(drop=False, inplace=True)
    df = df.drop(['2019_장애인', '2019_노인', '2019_다문화'], axis=1)
    df = df.groupby('자치구').sum()
    df = df.rename(index=lambda x: x.replace('서울 ', ''))
    df.reset_index(drop=False, inplace=True)
    return df

def gu_schoolage():
    df = pd.read_excel("rawdata/gu_schoolage.xls")
    df = df[df['자치구'] != '합계'].reset_index(drop=True)
    df.rename(columns={'기간': '연도'}, inplace=True)
    return df