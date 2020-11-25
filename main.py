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

import unicodedata

from selenium import webdriver
from bs4 import BeautifulSoup
from wcwidth import wcswidth

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

path = "./chromedriver"  # web driver install location
driver = webdriver.Chrome(path, options=options)
driver.implicitly_wait(3)  # seconds


def fps(string, width, align='<', fill=' '):
    count = (width - sum(1 + (unicodedata.east_asian_width(c) in "WF")
                         for c in string))
    """
    # East_Asian_Width (ea)
    ea ; A         ; Ambiguous
    ea ; F         ; Fullwidth
    ea ; H         ; Halfwidth
    ea ; N         ; Neutral
    ea ; Na        ; Narrow
    ea ; W         ; Wide
    """
    return {
        '>': lambda s: fill * count + s,
        '<': lambda s: s + fill * count,
        '^': lambda s: fill * (count / 2)
                       + s
                       + fill * (count / 2 + count % 2)
    }[align](string)


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
    # print(
    # num + "위 : " + name + " " + game_num + " " + game_point + " " + game_win + " " + game_draw +
    # " " + game_lose + " " + game_plus_point + " " + game_minus_point + " " + game_plus_minus_point)
    print('{0:>2}'.format(num) + u"위 : ", end='')  # 인덱스:>길이, 오른쪽으로 정렬 후 나머지 공백. 경기수
    # print("%s" % (fps(name, 40)), end='')
    # print(fps(name, 30), end='')
    print('{:\u3000<20s}'.format(name), end='')
    print('{0:>5}'.format(game_num) + " ", end='')
    print('{0:>5}'.format(game_point) + " ", end='')
    print('{0:>5}'.format(game_win) + " ", end='')
    print('{0:>5}'.format(game_draw) + " ", end='')
    print('{0:>5}'.format(game_lose) + " ", end='')
    print('{0:>5}'.format(game_plus_point) + " ", end='')
    print('{0:>5}'.format(game_minus_point) + " ", end='')
    print('{0:>5}'.format(game_plus_minus_point))


def leagueNameLoad(team):
    num = team.select('.num > div.inner > strong')[0].text
    name = team.select('.align_l > div.inner > span.name')[0].text
    if (int(num) % 3) == 1:  # 한 줄에 3개씩 출력하기 위함
        print('\n')
    leagueName = " [" + num + "] " + name
    print(fps(leagueName, 35), end='')


def resultUpperPrint(a):
    """
    1 = 일반 순위표 검색
    2 = 팀 연도 검색
    3 = 팀 10개년 검색
    """
    if a == 1 or a == 2:
        print("=" * 80)
        print(" 순위   팀                           경기수  승점    승     무    패    득점   실점  득실차")
        print("=" * 80)
    elif a == 3:
        print("=" * 90)
        print("   연도    순위   팀                           경기수  승점    승     무    패    득점   실점  득실차")
        print("=" * 90)

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
        print('{}는 없는 번호 입니다.\n'.format(fun1_menu_num))
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
        try:
            naver_wfootball = "https://sports.news.naver.com/wfootball/record/index.nhn?category=" + leaguename + "&year=" + str(
                int(2021 - league_search_year))
            driver.get(naver_wfootball)
            page = driver.page_source
            premi_team_rank_list = BeautifulSoup(page, "html.parser")
            team_rank_list = premi_team_rank_list.select('#wfootballTeamRecordBody>table>tbody>tr')
            print('조회 완료: ' + str(int(2021 - league_search_year)) + '-' + str(
                int(22 - league_search_year)) + ' 시즌의 리그 순위는 다음과 같습니다.')
            resultUpperPrint(1)  # 폼 불러오기
            for team in team_rank_list:
                leagueload(team)
            print("=" * 80)
            print('검색을 마쳐서 홈 화면으로 이동합니다.\n')
        except:
            print('인터넷에 연결되지 않았거나 입력에 오류가 있습니다. 다시 한 번 확인해주세요.')
            pause()


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
        print('{}는 없는 번호 입니다.\n'.format(fun2_menu_num))
        pause()


def fun2_teamSearch(leaguename):
    i = 0
    print('원하시는 시즌을 선택하세요 \n')
    print(' 1. 2020-21  ||   6. 2015-16 ')
    print(' 2. 2019-20  ||   7. 2014-15 ')
    print(' 3. 2018-19  ||   8. 2013-14 ')
    print(' 4. 2017-18  ||   9. 2012-13 ')
    print(' 5. 2016-17  ||  10. 2011-12 ')
    print('11. 2020-11  (상위 10개년 조회)')
    print(' 0. 상위 메뉴로 이동\n')
    league_search_year = int(input('선택 : '))
    if league_search_year == 0:
        print('상위 메뉴로 이동합니다.')
        pause()
    elif 1 <= league_search_year <= 10:
        # 팀 리스트 호출 시작
        try:
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
            print('\n 원하는 팀을 선택해주세요.')
            teamNumber = int(input(' 선택 : '))
            print(' 선택한 결과는 다음과 같습니다.')
            resultUpperPrint(2)
            for team in team_rank_list:
                i += 1  # 기존 구성 활용하기 위해 증감연산 사용
                if int(i) == int(teamNumber):  # 구조는 같기에 숫자 넣은 것이 몇 번째일때 팀 결과 출력하게끔 처리
                    leagueload(team)
            print("=" * 80)
            pause()
            # 출력 완료 후 팀 검색 종료
        except:
            print('인터넷에 연결되지 않았거나 입력에 오류가 있습니다. 다시 한 번 확인해주세요.')
            pause()
    elif league_search_year == 11:
        try:
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
            print('\n 원하는 팀을 선택해주세요.')
            teamNumber = int(input(' 선택 : '))
            for team in team_rank_list:
                i += 1  # 기존 구성 활용하기 위해 증감연산 사용
                if int(i) == int(teamNumber):  # 구조는 같기에 숫자 넣은 것이 몇 번째일때 팀 불러오게
                    league_search_name = team.select('.align_l > div.inner > span.name')[0].text # 순회하여 매칭된 팀의 이름을 기억
            print(' 선택한 결과는 다음과 같습니다. [ {} ]'.format(league_search_name)) # 일단 팀을 출력
            print(' 조회한 결과는 다음과 같습니다.')
            resultUpperPrint(3)
            j = 0
            while j <= 10:
                k = 0
                naver_wfootball = "https://sports.news.naver.com/wfootball/record/index.nhn?category=" + leaguename + "&year=" + str(
                    int(2020 - j))
                driver.get(naver_wfootball)
                page = driver.page_source
                premi_team_rank_list = BeautifulSoup(page, "html.parser")
                team_rank_list = premi_team_rank_list.select('#wfootballTeamRecordBody>table>tbody>tr')
                for team in team_rank_list:
                    if team.select('.align_l > div.inner > span.name')[0].text == league_search_name:
                        print('[ ' + str(int(2020 - j)) + ' ] ', end='')
                        leagueload(team)
                j += 1
            print("=" * 90)
            pause()
        except:
            print('인터넷에 연결되지 않았거나 입력에 오류가 있습니다. 다시 한 번 확인해주세요.')
            pause()
    else:
        print('{}는 없는 번호 입니다.\n'.format(league_search_year))
        pause()


while True:
    print('축구 팀 검색 프로그램입니다. \n')
    print(' 1. 순위표 검색')
    print(' 2. 팀 검색\n')
    print(' 0. 프로그램 종료')
    try:
        menu_num = int(input('선택 : '))  # 사용자 입력을 받기 위한 int형 menu_num 선
        if menu_num == 0 or menu_num == "0":
            print('프로그램을 종료합니다. \n')
            break
        elif menu_num == 1:
            fun1()
        elif menu_num == 2:
            fun2()
        else:
            print('{}는 없는 번호 입니다.\n'.format(menu_num), flush=False)

    except:
        print('알 수 없는 오류가 발생했습니다. 다시 실행합니다. \n')
        menu_num = None
