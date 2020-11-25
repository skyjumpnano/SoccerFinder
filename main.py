# Soccer Finder with Python
# Myeongho Park
# 2020. 11. 23.

# ##
# # Host Database
# #
# # localhost is used to configure the loopback interface
# # when the system is booting.  Do not change this entry.
# ##
# 127.0.0.1	localhost
# 255.255.255.255	broadcasthost
# ::1             localhost
# 만약에 실행이 똑바로 안된다면 HOST 문제일 가능성이 높음
# FOR MAC
# 1. 위의 Host Database copy
# 2. Terminal.app > sudo nano /etc/hosts 로 superuser grant후 파일 수정
# 3. DNS Cache refresh : Terminal.app > dscacheutil -flushcache

import sys
import os
import requests

from selenium import webdriver
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

path = "./chromedriver"  # web driver install location
driver = webdriver.Chrome(path, options=options)
driver.implicitly_wait(3)  # seconds


def pause():
    programPause = input("Press the <ENTER> key to continue...")
    # 프로그램을 잠깐 멈출 필요가 있을 때마다 사용하기 위해 만듬


def leagueload(team):
    # 리그 검색에서 매번 쓰기에 아무리 봐도 무리수라 따로 로드부만 작성
    num = team.select('.num > div.inner > strong')[0].text
    name = team.select('.align_l > div.inner > span.name')[0].text
    name_exception = team.select('td > div > span')[0].text
    # 리그 꼬다리 있을때
    if name_exception == '유로파 리그' or name_exception == '챔피언스 리그 직행' or name_exception == '강등 직행' or name_exception == '챔피언스 리그 예선':
        # state_bar3 / state_bar1 / state_bar4 / state_bar2 순서대로다.
        game_num = team.select('td > div > span')[2].text  # 경기수
        game_point = team.select('td > div > span')[3].text  # 승점
        game_win = team.select('td > div > span')[4].text  # 승
        game_draw = team.select('td > div > span')[5].text  # 무
        game_lose = team.select('td > div > span')[6].text  # 패
        game_plus_point = team.select('td > div > span')[7].text  # 득점
        game_minus_point = team.select('td > div > span')[8].text  # 실점
        game_plus_minus_point = team.select('td > div > span')[9].text  # 득실차
        # 예외 처리를 하는 이유 : 네이버 스포츠 쪽에 앞에 뭐가 하나 더 붙음.
    else:
        game_num = team.select('td > div > span')[1].text  # 경기수
        game_point = team.select('td > div > span')[2].text  # 승점
        game_win = team.select('td > div > span')[3].text  # 승
        game_draw = team.select('td > div > span')[4].text  # 무
        game_lose = team.select('td > div > span')[5].text  # 패
        game_plus_point = team.select('td > div > span')[6].text  # 득점
        game_minus_point = team.select('td > div > span')[7].text  # 실점
        game_plus_minus_point = team.select('td > div > span')[8].text  # 득실차
    print(
        num + "위 : " + name + " " + game_num + " " + game_point + " " + game_win + " " + game_draw + " " + game_lose + " " + game_plus_point + " " + game_minus_point + " " + game_plus_minus_point)


def leagueNameLoad(team):
    num = team.select('.num > div.inner > strong')[0].text
    name = team.select('.align_l > div.inner > span.name')[0].text
    if (int(num) % 3) == 1: # 한 줄에 3개씩 출력하기 위함
        print('\n')
    print(" [" + num + "] " + name, end='') # Python에서는 자동으로 개행하기에 개행을 방지하기 위하여 매개변수 삽입


def fun1():
    print('원하시는 리그를 선택하세요 \n')
    print(' 1. 프리미어리그')
    print(' 2. 라리가')
    print(' 3. 분데스리가')
    print(' 4. 세리에 A')
    print(' 5. 리그 1')
    print(' 0. 상위 메뉴로 이동\n')
    fun1_menu_num = int(input('선택 : '))
    if fun1_menu_num == 0:
        print('상위 메뉴로 이동합니다.')
        pause()
    elif fun1_menu_num == 1:
        leaguename = 'epl'
        fun1_year(leaguename)
    elif fun1_menu_num == 2:
        leaguename = 'primera'
        fun1_year(leaguename)
    elif fun1_menu_num == 3:
        leaguename = 'bundesliga'
        fun1_year(leaguename)
    elif fun1_menu_num == 4:
        leaguename = 'seria'
        fun1_year(leaguename)
    elif fun1_menu_num == 5:
        leaguename = 'ligue1'
        fun1_year(leaguename)
    else:
        print('{}는 없는 번호 입니다.\n'.format(menu_num))
        pause()


def fun1_year(leaguename):
    print('원하시는 시즌을 선택하세요 \n')
    print(' 1. 2020-21  ||  6. 2015-16 ')
    print(' 2. 2019-20  ||  7. 2014-15 ')
    print(' 3. 2018-19  ||  8. 2013-14 ')
    print(' 4. 2017-18  ||  9. 2012-13 ')
    print(' 5. 2016-17  ||  0. 상위로 이동 \n')
    league_search_year = int(input('선택 : '))
    if league_search_year == 0:
        print('상위 메뉴로 이동합니다.')
        pause()
    else:
        naver_wfootball = "https://sports.news.naver.com/wfootball/record/index.nhn?category=" + leaguename + "&year=" + str(
            int(2021 - league_search_year))
        driver.get(naver_wfootball)
        page = driver.page_source
        premi_team_rank_list = BeautifulSoup(page, "html.parser")
        team_rank_list = premi_team_rank_list.select('#wfootballTeamRecordBody>table>tbody>tr')
        for team in team_rank_list:
            leagueload(team)
        print('검색을 마쳐서 홈 화면으로 이동합니다.\n')

def fun2():
    print('원하시는 리그를 선택하세요 \n')
    print(' 1. 프리미어리그')
    print(' 2. 라리가')
    print(' 3. 분데스리가')
    print(' 4. 세리에 A')
    print(' 5. 리그 1')
    print(' 0. 상위 메뉴로 이동\n')
    fun2_menu_num = int(input('선택 : '))
    if fun2_menu_num == 0:
        print('상위 메뉴로 이동합니다.')
        pause()
    elif fun2_menu_num == 1:
        leaguename = 'epl'
        print('\n == 선택한 리그는 프리미어리그 입니다 ==')
        fun2_teamSearch(leaguename)
    elif fun2_menu_num == 2:
        leaguename = 'primera'
        print('\n == 선택한 리그는 라리가 입니다 ==')
        fun2_teamSearch(leaguename)
    elif fun2_menu_num == 3:
        leaguename = 'bundesliga'
        print('\n == 선택한 리그는 분데스리가 입니다 ==')
        fun2_teamSearch(leaguename)
    elif fun2_menu_num == 4:
        leaguename = 'seria'
        print('\n == 선택한 리그는 세리에 A 입니다 ==')
        fun2_teamSearch(leaguename)
    elif fun2_menu_num == 5:
        leaguename = 'ligue1'
        print('\n == 선택한 리그는 리그 1 입니다 ==')
        fun2_teamSearch(leaguename)
    else:
        print('{}는 없는 번호 입니다.\n'.format(menu_num))
        pause()


def fun2_teamSearch(leaguename):
    i = 0
    print('원하시는 시즌을 선택하세요 \n')
    print(' 1. 2020-21  ||  6. 2015-16 ')
    print(' 2. 2019-20  ||  7. 2014-15 ')
    print(' 3. 2018-19  ||  8. 2013-14 ')
    print(' 4. 2017-18  ||  9. 2012-13 ')
    print(' 5. 2016-17  ||  0. 상위로 이동 \n')
    league_search_year = int(input('선택 : '))
    if league_search_year == 0:
        print('상위 메뉴로 이동합니다.')
        pause()
    else:
        # 팀 리스트 호출 시작
        naver_wfootball = "https://sports.news.naver.com/wfootball/record/index.nhn?category=" + leaguename + "&year=" + str(
            int(2021 - league_search_year))
        driver.get(naver_wfootball)
        page = driver.page_source
        premi_team_rank_list = BeautifulSoup(page, "html.parser")
        team_rank_list = premi_team_rank_list.select('#wfootballTeamRecordBody>table>tbody>tr')
        for team in team_rank_list:
            leagueNameLoad(team)
        # 여기까지 팀 리스트 호출
        # 팀 선택 시작
        print(' 원하는 팀을 선택해주세요.')
        teamNumber = int(input('선택 : '))
        for team in team_rank_list:
            i += 1 # 기존 구성 활용하기 위해 증감연산 사용
            if int(i) == int(teamNumber): # 구조는 같기에 숫자 넣은 것이 몇 번째일때 팀 결과 출력하게끔 처리
                leagueload(team)
        pause()
        # 출력 완료 후 팀 검색 종료


while True:
    print('축구 팀 검색 프로그램입니다. \n')
    print(' 1. 순위표 검색')
    print(' 2. 팀 검색\n')
    print(' 0. 프로그램 종료')

    menu_num = int(input('선택 : '))  # 사용자 입력을 받기 위한 int형 menu_num 선

    if menu_num == 0:
        print('프로그램을 종료합니다. \n')
        sys.exit()
    elif menu_num == 1:
        fun1()
    elif menu_num == 2:
        fun2()
    else:
        print('{}는 없는 번호 입니다.\n'.format(menu_num))
        pause()
