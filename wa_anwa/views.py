from django.shortcuts import render
from accounts.models import User
import datetime
from wa_anwa.models import Betting,Participate,Answer,Result
from django.http import JsonResponse

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
    # users.sort(key = lambda x:x[0])
    len_user = len(users)

    # 유저 별 달의 포인트와 적중률을 담을 배열 생성
    all_Participate = [0]**len_user
    all_HitRate = [[0]**len_user for _ in range(2)]


    # 이번 달에 진행한 배팅을 모두 불러온다.
    today = datetime.date.today()
    m = today.month
    bettings = Betting.objects.filter(date_year='2022', date_month = m)

    # 사용자 별로 이번 달의 배팅 안에서 연결된 Participate 불러오기 
    for k in range(len_user):
        temp_user = users[k]
        for i in range(len(bettings)):
            user_betting = bettings[i]
            participates = Participate.objects.filter(betting = user_betting)
            for j in range(len(participates)):
                participate = participates[j]
                result = Result.filter(participation = participate)
                all_Participate[temp_user.pk] += result.point

                # 적중률 계산을 위해서 성공 실패 횟수를 저장
                if result.win == True:
                    all_HitRate[0][temp_user.pk] += 1
                elif result.win == False:
                    all_HitRate[1][temp_user.pk] += 1



    ranking = []

    # ranking 배열에 달의 포인트, 적중률, user 정보를 내림차순으로 넣어준다 
    for i in range(len(all_Participate)):
        max_num = max(all_Participate)
        index =  all_Participate.index(max_num)
        hitrate = all_HitRate[i][0] // all_HitRate[i][0] + all_HitRate[i][1]
        temp = [max,hitrate,users[index]]
        ranking.append(temp)
        all_Participate.remove(max_num)
    
    # 현재 유저 찾기
    now_user = request.user
    user_pk = now_user.pk
    user_ranking = []

    # user_ranking 배열에 현재 접속한 유저의 등수, 포인트, 적중률, user 정보를 넣어준다
    for i in range(len(ranking)):
        temp = ranking[i][2]
        if temp.pk == user_pk:
            user_ranking.append(i)
            user_ranking.append(temp)

    return render( request, 'wa_anwa/ranking.html', {'ranking':ranking, 'user_ranking':user_ranking, 'month': m })


def my_page(request):
    # 유저 객체를 불어와서 전달
    now_user = request.user
    my_user = User.objects.get(pk = now_user.pk)

    # 이번 달에 진행한 배팅을 모두 불러온다.
    today = datetime.date.today()
    m = today.month
    bettings = Betting.objects.filter(date_year='2022', date_month = m)

    # 이번 달 진행한 배팅을 불러와 적중률 계산하고 달력 표시용 데이터 수집
    hitRate = []
    calender = [0]*31

    for i in range(len(bettings)):
            user_betting = bettings[i]
            day= user_betting.date.day()
            participates = Participate.objects.filter(betting = user_betting)
            for j in range(len(participates)):
                participate = participates[j]
                result = Result.filter(participation = participate)
                
                # 적중률 계산을 위해서 성공 실패 횟수를 저장
                if result.win == True:
                    hitRate[0] += 1
                    calender[day] = True

                elif result.win == False:
                    hitRate[1] += 1
                    calender[day] = False
    user_hitRate = hitRate[0]//hitRate[0] + hitRate[1]

    return render( request, 'wa_anwa/mypage.html', {'my_user':my_user, 'user_hitRate':user_hitRate, 'calender': calender, 'month':m})


def betting(request, id):
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
    Participate.objects.create(region=request.POST['region'], time=request.POST['time'], date=request.POST['date'])
    return
