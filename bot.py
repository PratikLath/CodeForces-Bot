# Importing all the required functions
import requests  
from collections import defaultdict
from datetime import datetime
from bottle import (  
    run, post, request as bottle_request
)

# Bot url and dictionaries
BOT_URL = 'https://api.telegram.org/<BOT TOKEN>' 
user_dic={}
user_rat={}
dis=defaultdict(list)

# Helps in retrieiving top 20 questions from Codeforces with the given tag
def help_code(s,chat_i):
    url="https://codeforces.com/api/problemset.problems?tags=" + s
    response = requests.get(url)
    data = response.json()
    data1=data["result"]
    k=0
    s=""
    poma=[]
    for kol in data1["problems"]:
        if "rating" in kol:
            poma.append(kol)
    zoma=sorted(poma, key = lambda k:k['rating'])
    for i in (zoma):
        if "rating" in i:
            if i["rating"]>=user_rat[str(chat_i)]:
                flag=0
                if "contestId" in i and "index" in i:
                    if str(chat_i) in dis:
                        if (i["contestId"],i["index"]) in dis[str(chat_i)]:
                            flag=1
                        else:
                            dis[str(chat_i)].append((i["contestId"],i["index"]))
                    else:
                        dis[str(chat_i)].append((i["contestId"],i["index"]))
                if(k==20):
                    break
                if(flag==0):
                    if "contestId" in i and "index" in i:
                        url1="https://codeforces.com/problemset/problem/"+str(i["contestId"])+"/"+str(i["index"])
                        if(k<20):
                            if "name" in i and "rating" in i:
                                s+=str(k+1)+". "+"<a href=\"" + url1 + "\">" + i["name"] +" [Rating: "+str(i["rating"])  + "]</a>" + "\n"
                                k=k+1
    return s

# Helps in getting the user details 
def user_details(z):
    k="https://codeforces.com/api/user.info?handles="
    k=k+z
    response = requests.get(k)
    s=""
    p=""
    data = response.json()
    if(data["status"]=="FAILED"):
        s="Wrong input! Please, enter valid input."
    else:    
        for i in (data["result"]):
            if "handle" in i:
                s=s+"Handle: "+ i["handle"] + "\n"
            if "firstName" in i and "lastName" in i:
                s=s+"Name: "+ i["firstName"]+ " "+i["lastName"]+"\n"
            if "rating" in i and "maxRating" in i:    
                s=s+"Rating: "+ str(i["rating"]) +  " (Max:"  +str(i["maxRating"])+")\n"
            if "rank" in i:
                s=s+"Rank: "+i["rank"]+"\n"
            if "organization" in i:
                s=s+"Organization: "+i["organization"] +"\n"
            if "city" in i:
                s=s+"City: "+i["city"] +"\n"
            if "country" in i:
                s=s+"Country: "+i["country"]+"\n"
            if "registrationTimeSeconds" in i:
                p=p+str(datetime.fromtimestamp(i["registrationTimeSeconds"]).strftime("%B %d, %Y")) + "\n"
                s=s+"Registered on: "+p+"\n" 
    return s

# Helps in converting seconds into date
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d" % (hour, minutes) 

# Helps to send the desired function to the user
def send_message(data):  
    chat_id = data['message']['chat']['id']
    message_text = data['message']['text']
    arr=[]
    arr.append('implementation') 
    arr.append('dp') 
    arr.append('math') 
    arr.append('greedy')  
    arr.append('brute force')  
    arr.append('data structures')  
    arr.append('constructive algorithms')  
    arr.append('dfs and similar')  
    arr.append('sortings') 
    arr.append('binary search')  
    arr.append('graphs')  
    arr.append('trees')  
    arr.append('strings')  
    arr.append('number theory')  
    arr.append('geometry')  
    arr.append('combinatorics')  
    arr.append('two pointers')  
    arr.append('dsu')  
    arr.append('bitmasks')  
    arr.append('probabilities')  
    arr.append('shortest paths')  
    arr.append('hashing')  
    arr.append('divide and conquer')  
    arr.append('games')  
    arr.append('matrices')  
    arr.append('flows')  
    arr.append('string suffix structures')  
    arr.append('expression parsing')  
    arr.append('graph matchings')  
    arr.append('ternary search')  
    arr.append('meet-in-the-middle')  
    arr.append('fft')  
    arr.append('2-sat')  
    arr.append('chinese remainder theorem')  
    arr.append('schedules')
    if(message_text=='/questions' and str(chat_id) in user_dic):
        s='<b>Select any question tag from the following list:</b>\n\n'
        s=s + str(arr)
    elif(message_text=='/questions'):
        s='You have not added your username till yet. You can add it by typing'+'\n'+ '/username_(Your username). For example, if your username is helloworldxyz, then type'+'\n'+ '/username_helloworldxyz to add your username.'
    else:
        z=0
        for i in range(35):
            if(message_text.lower()==arr[i]):
                z=1
        if(z==0):
            s='Wrong input! Please, enter valid input.'
        else:
            if str(chat_id) in user_dic:
                s=help_code(message_text.lower(),chat_id)
            else:
                s='You have not added your username till yet. You can add it by typing'+'\n'+ '/username_(Your username). For example, if your username is helloworldxyz, then type'+'\n'+ '/username_helloworldxyz to add your username.'
    if(message_text=='/start' or message_text=='/help' ):
        s='Welcome to the Codeforces Bot!'+'\n\n'+'The list of available commands are:'+'\n\n'+'/start -  Start the bot.'+'\n\n'+'/questions - See top questions with a given tag.'+'\n\n'+'/contests - See the list of upcoming contests.' + '\n\n'+ '/add_user - Add your username.'+'\n\n'+ '/delete_user - Delete your username.'+'\n\n'+'/my_user - Show your username.'+'\n\n'+'/user_info - Get any user information.' + '\n\n'+  '/help -  See the list of available tags.' 
    if(message_text[:9]=='/getuser_'):
        s=user_details(message_text[9:])  
    if(message_text=='/contests'):
        s=""
        response = requests.get("https://codeforces.com/api/contest.list?gym=false")
        data = response.json()
        for i in (data["result"]):
            if(i["phase"]=="BEFORE"):
                p=""
                for j in i["name"]:
                    if(j!='#'):
                       p=p+j
                p=p+" ("
                p=p+str(convert(i["durationSeconds"]))+" hrs) - "
                p=p+str(datetime.fromtimestamp(i["startTimeSeconds"]).strftime("%I:%M %p, %B %d, %Y, %A")) + "\n"
                p=p+"https://codeforces.com/contestRegistration/"+str(i["id"])+"\n\n"
                s=p+s
        s="<b>The upcoming contests are:</b>"+"\n\n"+s
    if(message_text=='/user_info'):
        s="To find the information about a particular CodeForces user type /getuser_(Username). For example, if the username is helloworldxyz, then type /getuser_pratiklath to get the information about that user."
    if(message_text=='/add_user'):
        s="Please add your username by typing"+"\n"+"/username_(Your username). For example, if your username is helloworldxyz, then type /username_helloworldxyz to add your username." 
    if(message_text[:10]=='/username_'):
        if str(chat_id) in user_dic:
            s="The username is already added."
        else: 
            var="https://codeforces.com/api/user.info?handles="+message_text[10:]
            response = requests.get(var)
            data = response.json()
            if(data["status"]=="FAILED"):
                s="Wrong input! Please, enter valid input."
            else:
                for para in data["result"]:
                    if "rating" in para:
                        user_rat[str(chat_id)]=para["rating"]
                        user_dic[str(chat_id)]=message_text[10:]
                        s="The username is added!"
                    else:
                        s="Wrong input! Please, enter valid input."
    if(message_text=='/my_user'):
        zz=str(chat_id)
        if zz in user_dic:
            print(user_dic[str(chat_id)])
            s=user_dic[str(chat_id)]
        else:
            s='The given user is not in the database.'
    if(message_text=='/delete_user'):
        if str(chat_id) in user_dic and str(chat_id) in user_rat:
            del user_dic[str(chat_id)]
            del user_rat[str(chat_id)]
            s="The username is deleted!"
        else:
            s="No username exists."
    print(s)
    message_url = BOT_URL + 'sendMessage?chat_id=' + str(chat_id) + '&text=' + s +'&parse_mode=HTML'
    requests.get(message_url)  

# Main function    
@post('/')
def main():  
    data = bottle_request.json
    send_message(data)
if __name__ == '__main__':  
    run(host='localhost', port=88, debug=True)