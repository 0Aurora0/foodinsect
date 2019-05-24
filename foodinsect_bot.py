import discord
import asyncio
import datetime
from parser import *
 
 
client = discord.Client()
 
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
 
@client.event
async def on_message(message):
    if message.content.startswith('!to'):    #메세지의 내용의 시작이 !to로 시작할 경우
        to_tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)    #오늘 날짜에 하루를 더함
        local_date2 = to_tomorrow.strftime("%Y.%m.%d")    #위에서 구한 날짜를 년.월.일 형식으로 저장
        local_weekday2 = to_tomorrow.weekday()    #위에서  구한 날짜의 요일값을 저장
 
        l_diet = get_diet(2, local_date2, local_weekday2)    #점심식단을 파싱해옴
        d_diet = get_diet(3, local_date2, local_weekday2)    #석식식단을 파싱해옴
 
        if len(l_diet) == 1:    #점심식단의 길이가 1일경우 = parser.py에서 식단이 없을경우 공백한자리를 반환함.
            await client.send_message(message.channel, "급식이 없습니다.")    #급식이 없다고 메세지 보냄
        elif len(d_diet) == 1:    #점심식단의 길이가 1이 아니고 석식식단의 길이가 1일경우 = 점심식단만 있을경우
            lunch = local_date2 + " 중식\n" + l_diet    #날짜와 "중식"을 앞에 붙여서
            await client.send_message(message.channel, lunch)    #메세지 보냄
        else:    #둘다 길이가 1이 아닐경우 = 점심, 석식 식단 모두 있을 경우
            lunch = local_date2 + " 중식\n" + l_diet    #앞에 부가적인 내용을 붙여서
            dinner = local_date2 + " 석식\n" + d_diet
            await client.send_message(message.channel, lunch)    #메세지를 보냄
            await client.send_message(message.channel, dinner)
 
 
   elif message.content.startswith('!g'):
        await client.send_message(message.channel, '날짜를 보내주세요...')    #날짜를 보내달라는 메세지를 보냄
        meal_date = await client.wait_for_message(timeout=15.0, author=message.author)    #제한시간은 15초
 
        if meal_date is None:    #값이 존재하지 않거나 시간이 초과되었을 경우
            await client.send_message(message.channel, '15초내로 입력해주세요. 다시시도 : !g')    #다시 시도하라는 메세지를 보냄
            return
 
        else:    #값이 있다면
            meal_date = str(meal_date.content) # str형으로 변환, (사용자로부터 20180219와 같은 형태로 받아야 합니다.)
            meal_date = '20' + meal_date[:2] + '.' + meal_date[2:4] + '.' + meal_date[4:6]    # 2018.02.19 사이에 점을 추가함
            #(사용자로부터 점이 포함된 값으로 받을경우 위 코드를 삭제해도 됩니다.)
 
            s = meal_date.replace('.', ', ')     # 2018, 02, 19 점을 반점으로 교체
            ss = "datetime.datetime(" + s + ").weekday()"    #eval함수를 통해 요일값을 구하기 위한 작업
            try:
                whatday = eval(ss)    #요일값을 구해서 whatday에 저장
            except:    #오류가 날 경우 다시 시도하라는 메세지를 보냄
                await client.send_message(message.channel, '올바른 값으로 다시 시도하세요 : !g')
                return
            #이하 '내일 식단을 출력하기'와 같음
            l_diet = get_diet(2, meal_date, whatday)
            d_diet = get_diet(3, meal_date, whatday)
 
            if len(l_diet) == 1:
                l_diet = "급식이 없습니다."
                await client.send_message(message.channel, embed=l_diet)
            elif len(d_diet) == 1:
                lunch = meal_date + " 중식\n" + l_diet
                await client.send_message(message.channel, embed=lunch)
            else:
                lunch = meal_date + " 중식\n" + l_diet
                dinner = meal_date + " 석식\n" + d_diet
                await client.send_message(message.channel, lunch)
                await client.send_message(message.channel, dinner)
 
            
    acess_token = os.environ["BOT_TOKEN"]
    client.run('access_token')

    #대기 시간 초과로 봇이 종료되었을 때 자동으로 재실행을 위함
    #import sys, os
    executable = sys.executable
    args = sys.argv[:]
    args.insert(0, sys.executable)
    print("Respawning")
    os.execvp(executable, args)

if __name__ == '__main__':
    main()
