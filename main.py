# Soccer Finder with Python
# Myeongho Park
# 2020. 11. 23.

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
    # 리그 조회와 팀 검색에서 공통되게 사용하는 출력부
    num = team.select('.num > div.inner > strong')[0].text  # 순위
    name = team.select('.align_l > div.inner > span.name')[0].text  # 팀의 이름
    name_exception = team.select('td > div > span')[0].text  # 테이블 앞쪽에 플래그 (색깔로 이루어진 꼬다리) 가 있는지 확인하는 용도
    if name_exception == '유로파 리그' or name_exception == '챔피언스 리그 직행' or name_exception == '강등 직행' or name_exception == '챔피언스 리그 예선':
        # 태그에서 state_bar3 / ~~1 / ~~4 / ~~2 순서대로다. 예외 처리를 하는 이유 : 네이버 스포츠 쪽에 앞에 뭐가 하나 더 붙음. 그래서 Table에 +1씩 해준다.
        league_exception_flag = 1
    else:
        league_exception_flag = 0

    game_num = team.select('td > div > span')[1 + league_exception_flag].text  # 경기수
    game_point = team.select('td > div > span')[2 + league_exception_flag].text  # 승점
    game_win = team.select('td > div > span')[3 + league_exception_flag].text  # 승
    game_draw = team.select('td > div > span')[4 + league_exception_flag].text  # 무
    game_lose = team.select('td > div > span')[5 + league_exception_flag].text  # 패
    game_plus_point = team.select('td > div > span')[6 + league_exception_flag].text  # 득점
    game_minus_point = team.select('td > div > span')[7 + league_exception_flag].text  # 실점
    game_plus_minus_point = team.select('td > div > span')[8 + league_exception_flag].text  # 득실차

    print('{0:>2}'.format(num) + u"위 : ", end='')  # 인덱스:>길이, 오른쪽으로 정렬 후 나머지 공백. 경기수
    print('{:\u3000<20s}'.format(name), end='')  # 팀의 이름이 국문 영문 혼용이라 유니코드로 처리 (u)
    print('{0:>5}'.format(game_num) + " " + '{0:>5}'.format(game_point) + " " + '{0:>5}'.format(game_win) + " " +
          '{0:>5}'.format(game_draw) + " " + '{0:>5}'.format(game_lose) + " " + '{0:>5}'.format(game_plus_point) + " " +
          '{0:>5}'.format(game_minus_point) + " " + '{0:>5}'.format(game_plus_minus_point))  # 위의 순서대로 그대로 출력을 해줌


def leagueNameLoad(team):
    # 리그 이름 만을 출력해주기 위함 (팀 검색에서 사용)
    num = team.select('.num > div.inner > strong')[0].text
    name = team.select('.align_l > div.inner > span.name')[0].text
    # if (int(num) % 3) == 1:  # 한 줄에 3개씩 출력하기 위함
    #    print('\n')
    print(" [" + '{0:>2}'.format(num) + "] " + name)


def resultUpperPrint(a):
    # 표에서 위쪽 부분을 출력하기 위해서 사용. 매개변수 a는 아래와 같은 역할을 함
    # 3을 분할한 이유는 연도가 들어가므로 더 길어지기 때문이다.
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


def selectedLeagueAnnouncementPrompt(leaguename):
    # 선택된 리그에 대하여 어떤 리그가 선택되었는지 출력만 하는 부분.
    # 팀 검색과 리그 검색에서 동일하게 사용된다.
    if leaguename == 'epl':
        print('\n == 선택한 리그는 프리미어리그 입니다 ==')
    elif leaguename == 'primera':
        print('\n == 선택한 리그는 라리가 입니다 ==')
    elif leaguename == 'bundesliga':
        print('\n == 선택한 리그는 분데스리가 입니다 ==')
    elif leaguename == 'seria':
        print('\n == 선택한 리그는 세리에 A 입니다 ==')
    elif leaguename == 'ligue1':
        print('\n == 선택한 리그는 리그 1 입니다 ==')
    else:
        print('\n 잘못된 리그를 입력하였습니다. 프로그램을 종료합니다.')
        exit(0)  # 코드가 잘못 들어가면 앞에서 걸러져야 되기 때문에 이 코드가 표현될 때면 오동작할 가능성이 높으므로 강제종료 처리.


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
    selectedLeagueAnnouncementPrompt(leaguename)
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
        fun2_teamSearch(leaguename)
    elif fun2_menu_num == 2:
        leaguename = 'primera'
        fun2_teamSearch(leaguename)
    elif fun2_menu_num == 3:
        leaguename = 'bundesliga'
        fun2_teamSearch(leaguename)
    elif fun2_menu_num == 4:
        leaguename = 'seria'
        fun2_teamSearch(leaguename)
    elif fun2_menu_num == 5:
        leaguename = 'ligue1'
        fun2_teamSearch(leaguename)
    else:
        print('{}는 없는 번호 입니다.\n'.format(fun2_menu_num), flush=False)
        pause()


def fun2_teamSearch(leaguename):
    i = 0
    team_rank_list_num = 0
    selectedLeagueAnnouncementPrompt(leaguename)
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
        print('상위 메뉴로 이동합니다.', flush=False)
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
                team_rank_list_num += 1
            # 여기까지 팀 리스트 호출
            # 팀 선택 시작
            print('\n' + str(int(2021 - league_search_year)) + '년을 입력하셨습니다. 다음 ' + str(
                int(team_rank_list_num)) + '개의 팀 중 원하는 팀을 선택해주세요.')
            teamNumber = int(input(' 선택 : '))
            if 1 <= teamNumber <= team_rank_list_num:  # 전체 리스팅 넘버보다 작은데 0보다 클때만 동작
                print(' 선택한 결과는 다음과 같습니다.')
                resultUpperPrint(2)
                for team in team_rank_list:
                    i += 1  # 기존 구성 활용하기 위해 증감연산 사용
                    if int(i) == int(teamNumber):  # 구조는 같기에 숫자 넣은 것이 몇 번째일때 팀 결과 출력하게끔 처리
                        leagueload(team)
                print("=" * 80)
                pause()
                # 출력 완료 후 팀 검색 종료
            else:
                print('{}는 없는 팀 번호 입니다.\n'.format((team_rank_list_num + 1), flush=False))
                pause()
        except:
            print('인터넷에 연결되지 않았거나 입력에 오류가 있습니다. 다시 한 번 확인해주세요.')
            pause()
    elif league_search_year == 11:
        try:
            print(' 어느 시즌에 뛰었던 팀을 찾고 싶나요? (단위 : ____년)')
            print(' 정보 조회는 2020-21 시즌부터 2011-12 시즌까지 지원합니다.')
            league_search_year = int(input(' 입력 : '))
            if 2011 <= league_search_year <= 2020:
                naver_wfootball = "https://sports.news.naver.com/wfootball/record/index.nhn?category=" + leaguename + "&year=" + str(
                    int(league_search_year))
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
                        league_search_name = team.select('.align_l > div.inner > span.name')[
                            0].text  # 순회하여 매칭된 팀의 이름을 기억
                print(' 선택한 결과는 다음과 같습니다. [ {} ]'.format(league_search_name))  # 일단 팀을 출력
                print(' 조회한 결과는 다음과 같습니다.')
                resultUpperPrint(3)
                j = 0
                leagueTeamFindNum = 0
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
                            leagueTeamFindNum += 1 # 몇 회 조회했는지 카운트
                    j += 1
                print("=" * 90)
                print('[ {} ]'.format(league_search_name) + '는 동 기간동안 ' + str(int(leagueTeamFindNum)) + '회 분의 랭킹이 있습니다.', flush=False)
                pause()
            else:
                print('{}는 없는 년도 입니다.\n'.format(league_search_year, flush=False))
                pause()
        except:
            print('인터넷에 연결되지 않았거나 입력에 오류가 있습니다. 다시 한 번 확인해주세요.')
            pause()
    else:
        print('{}는 없는 번호 입니다.\n'.format(league_search_year, flush=False))
        pause()


while True:
    # 실질적인 코드의 메인 부분
    print('축구 팀 검색 프로그램입니다. \n')
    print(' 1. 순위표 검색')
    print(' 2. 팀 검색\n')
    print(' 0. 프로그램 종료')
    try:
        menu_num = int(input('선택 : '))
        if menu_num == 0 or menu_num == "0":
            print('프로그램을 종료합니다. \n')
            break
        elif menu_num == 1:
            fun1()
        elif menu_num == 2:
            fun2()
        else:
            print('{}는 없는 번호 입니다.\n'.format(menu_num), flush=False)  # 없는 번호에서 과대하게 입력받을 수 있기에 버퍼를 반드시 비움.

    except:
        print('알 수 없는 오류가 발생했습니다. 다시 실행합니다. \n')
        menu_num = None
