from django.shortcuts import render
from accounts.models import User
from datetime import date
from wa_anwa.models import Betting,Participate,Answer,Result
from accounts.models import User
import calendar as cd
from django.http import JsonResponse
import datetime
from datetime import datetime as dt
# Create your views here.

def time(request):
    now = datetime.datetime.now()
    today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
    today6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)
    if now < today8am:
        time=today8am
        return JsonResponse({'hour': "오전 8시", 'day':time.day, 'month':time.month, 'year':time.year, 'endtime':today8am - datetime.timedelta(hours=4)})
    elif now >= today8am and now < today6pm:
        time=today6pm
        return JsonResponse({'hour': "오후 6시", 'day':time.day, 'month':time.month, 'year':time.year, 'endtime':today6pm - datetime.timedelta(hours=4)})
    else:
        time = today8am + datetime.timedelta(days=1)
        return JsonResponse({'hour': "오전 8시", 'day':time.day, 'month':time.month ,'year':time.year,'endtime':today8am + datetime.timedelta(hours=20)})

def index(request):
    return render(request, 'wa_anwa/index.html')


def ranking(request):

    #  유저 모델을 불러옴
    users = User.objects.all()
    print(users)
    len_user = len(users)

    # 유저 별 달의 포인트와 적중률을 담을 배열 생성
    all_Participate = [0]*len_user
    all_HitRate = [[0]*len_user for _ in range(2)]


   # 이번 달에 진행한 배팅을 모두 불러온다.
    today = datetime.date.today()
    year = today.year
    m = today.month
    if len(str(m)) == 1:
        m = '0'+str(m)
    else:
        m = str(m) 
    search = str(year) + '-' + m
    bettings = Betting.objects.filter(date__contains=search)

        # 사용자 별로 이번 달의 배팅 안에서 연결된 Participate 불러오기 


    # print("betting:",bettings)
    for k in range(len_user):
        temp_user = users[k]
        user_pk = temp_user.pk
        for i in range(len(bettings)):
            user_betting = bettings[i]
            participates = Participate.objects.filter(betting = user_betting,user = temp_user )
            # print('participates:', participates)
            for j in range(len(participates)):
                participate = participates[j]
                    # result = participate.result
                result = Result.objects.get(participation = participate)
                # print('user_pk:',temp_user.pk)
                all_Participate[user_pk-1] += result.point

                # 적중률 계산을 위해서 성공 실패 횟수를 저장
                if result.win == True:
                    all_HitRate[0][user_pk-1] += 1
                elif result.win == False:
                    all_HitRate[1][user_pk-1] += 1
                


    export_ranking = []
    ranking = []
    ranking_Num = []
    ranking_HitRate = []

    
    copy_all_Participate = all_Participate.copy()
    # ranking 배열에 달의 포인트, 적중률, user 정보를 내림차순으로 넣어준다 
    for i in range(len(all_Participate)):
        max_num = max(all_Participate)
        index =  copy_all_Participate.index(max_num)
        if all_HitRate[0][i] == 0:
            hitrate = 0
        else:
            hitrate = all_HitRate[0][i]/(all_HitRate[0][i] + all_HitRate[1][i]) *100
        
        ranking.append(users[index])
        temp = [i+1,users[index], max_num, hitrate]
        export_ranking.append(temp)
     

        all_Participate.remove(max_num)
    
    
    # 현재 유저 찾기
    now_user = request.user
    user_pk = now_user.pk
    print(ranking)
  
    print("user_pk:",user_pk)
    # user_ranking 배열에 현재 접속한 유저의 등수, 포인트, 적중률, user 정보를 넣어준다
    for i in range(len(ranking)):
        temp = ranking[i]
        print(temp,temp.pk, temp.point)
        if temp.pk == user_pk:
            
            user_ranking = temp
            user_ranking_Num = i

            if all_HitRate[0][i] == 0:
                user_HitRate = 0
            else:
                user_HitRate = all_HitRate[0][i]/(all_HitRate[0][i] + all_HitRate[1][i]) *100

            user_Point = copy_all_Participate[temp.pk-1]
            break

    return render( request, 'wa_anwa/ranking.html', { 'export_ranking': export_ranking,'ranking':ranking,'ranking_Num':ranking_Num, 'ranking_HitRate': ranking_HitRate, 'user_ranking':user_ranking,'user_ranking_Num':user_ranking_Num ,'user_HitRate':user_HitRate , 'user_Point': user_Point ,'month': m })

def mypage(request):
    # 유저 객체를 불어와서 전달
    now_user = request.user
    my_user = User.objects.get(pk = now_user.pk)

    # 이번 달에 진행한 배팅을 모두 불러온다.
    today = datetime.date.today()
    year = today.year
    m = today.month
    bettings = Betting.objects.filter()

    # 이번 달 진행한 배팅을 불러와 적중률 계산하고 달력 표시용 데이터 수집
    hitRate = [0,0]
    calender = [[0]*3 for _ in range(31)]

    for i in range(31):
        calender[i][1] = i+1

    for i in range(len(bettings)):
            user_betting = bettings[i]
            day= user_betting.date.day
            # participates = user_betting.participates

            participates = Participate.objects.filter(betting = user_betting)
            if len(participates) != 0:
                for j in range(len(participates)):
                    participate = participates[j]
                    # result = participate.result
                    result = Result.objects.get(participation = participate)
                
                    # 적중률 계산을 위해서 성공 실패 횟수를 저장
                    if result.win == participate.choice:
                        hitRate[0] += 1
                        calender[day][0] = 1
                        calender[day][2] = participate.point

                    elif result.win != participate.choice:
                        hitRate[1] += 1
                        calender[day][0] = 2
                        calender[day][2] = -1 * participate.point
            elif len(participates) != 0:
                return render( request, 'wa_anwa/mypage.html', {'my_user':my_user, 'calender': calender, 'month':m})

    today=date.today()
    c=cd.Calendar(firstweekday=1)
    monthcal=[]
    # 주 단위로 나눠서 담기
    for i in c.monthdayscalendar(today.year,today.month):
        
        weekcal=[]
        for j in range(len(i)):
            buffer = [0,0,0]
            for k in range(31):
                if i[j] == calender[k][1]:
                    print(i[j])
                    buffer[1] = i[j]
                    buffer[0] = calender[k][0]
                    buffer[2] = calender[k][2]
                    break
            weekcal.append(buffer)
        monthcal.append(weekcal)


    if hitRate[0] == 0:
        user_hitRate = 0
    else:
        user_hitRate = hitRate[0]/(hitRate[0] + hitRate[1]) *100


    return render( request, 'wa_anwa/mypage.html', {'monthcal':monthcal,'my_user':my_user, 'user_hitRate':user_hitRate, 'calender': calender, 'month':m})


def betting(request,id):
    return render(request, 'wa_anwa/map.html', {'id':id})

def map(request):
    user = request.user
    if user.is_authenticated:
        participate = Participate.objects.filter(user = user).last()
        lastResult = Result.objects.filter(participation=participate)
        
        # if lastResult.checked:
        if lastResult != False:
            return render(request, 'wa_anwa/map.html', {'user_point':user.point})
        else: 
            lastResult.checked = True
            return render(request, 'wa_anwa/result.html')
    else:
        return render(request, 'wa_anwa/index.html')

def createparticipate(request):
    participate = Participate.objects.create(region=request.POST['region'], time=request.POST['time'], date=request.POST['date'])
    return JsonResponse({})
