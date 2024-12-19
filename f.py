global syed
global cp
import requests
import json
import threading
from time import sleep
import os
import random
import re

def banner():
    print('''
           ███████╗██╗   ██╗███████╗██████╗     ███████╗██████╗ 
           ██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗    ██╔════╝██╔══██╗
           ███████╗ ╚████╔╝ █████╗  ██║  ██║    █████╗  ██████╔╝
           ╚════██║  ╚██╔╝  ██╔══╝  ██║  ██║    ██╔══╝  ██╔══██╗
           ███████║   ██║   ███████╗██████╔╝    ██║     ██║  ██║
           ╚══════╝   ╚═╝   ╚══════╝╚═════╝     ╚═╝     ╚═╝  ╚═╝
                                                               
''')

class myThread(threading.Thread):
    def __init__(self, proxies, cookie, idpage_follow):
        threading.Thread.__init__(self)
        self.proxies = proxies
        self.cookie = cookie
        self.idpage_follow = idpage_follow

    def run(self):
        try:
            self.get_page()
        except Exception as e:
            print('ERROR: ' + str(e))

    def savefile(self, cookie, token):
        file_name = 'cookie.txt'
        with open(file_name, 'r', encoding='utf-8') as file:
            data = file.readlines()
        try:
            data.remove(cookie + '\n')
        except:
            data.remove(cookie)
        data.append(cookie + '|' + token + '\n')
        with open(file_name, 'w', encoding='utf-8') as file:
            file.writelines(data)

    def get_page(self):
        try:
            self.uid = self.cookie.split('c_user=')[1].split(';')[0]
        except:
            return None
        pxs = self.proxies
        if len(self.cookie.split('|')) == 2:
            if 'EAA' in self.cookie.split('|')[1]:
                cookie = self.cookie.split('|')[0]
                token_E = self.cookie.split('|')[1]
            else:
                cookie = self.cookie
                token_E = get_token_1(cookie)
        else:
            cookie = self.cookie
            token_E = get_token_1(cookie)
        if token_E == False:
            token_E = getToken(cookie, pxs)
            if token_E == False:
                print('Get token Error')
                return
        head = {'cookie': cookie}
        if 'EAA' in token_E:
            try:
                open(f'./Success/{self.idpage_follow}.txt', 'r')
            except:
                open(f'./Success/{self.idpage_follow}.txt', 'w')
            textid = open(f'./Success/{self.idpage_follow}.txt', 'r').read()
            url_tokenpage = 'https://graph.facebook.com/me/accounts?fields=access_token&limit=100&access_token=' + token_E
            getTokenPage = requests.get(url_tokenpage, headers=head)
            if 'error' in getTokenPage.text:
                print('ERROR GETTING PAGE')
                return
            getTokenPage = getTokenPage.json()['data']
            index = 1
            for get in getTokenPage:
                token_page = get['access_token']
                idpage = get['id']
                if idpage in textid:
                    continue
                def fl(token_page, head, pxs, idpage_follow, idpage, uid, index):
                    global syed
                    headers = {
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9',
                        'content-type': 'application/x-www-form-urlencoded',
                        'cookie': self.cookie,
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                        'x-fb-friendly-name': 'CometUserFollowMutation'
                    }
                    data = {
                        'method': 'POST',
                        'fb_api_caller_class': 'RelayModern',
                        'fb_api_req_friendly_name': 'CometUserFollowMutation',
                        'variables': '{\"input\":{\"attribution_id_v2\":\"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,tap_bookmark,1728917052006,775849,118869867981634,,\",\"is_tracking_encrypted\":false,\"subscribe_location\":\"PROFILE\",\"subscribee_id\":\"' + self.idpage_follow + '\",\"tracking\":null,\"actor_id\":\"' + idpage + '\",\"client_mutation_id\":\"3\"},\"scale\":1}',
                        'server_timestamps': 'true',
                        'doc_id': '8959345304089984'
                    }
                    pr = {'access_token': token_page}
                    buff_f = requests.post('https://graph.facebook.com/graphql/', headers=headers, params=pr, data=data, proxies=pxs, timeout=50).text
                    if 'Following' in buff_f:
                        print(f'[{syed}]Link|{idpage_follow}|Page-id|{str(index)}{idpage}|Syed-Follow-Success')
                        syed += 1
                        with open(f'./Success/{self.idpage_follow}.txt', 'a') as wf:
                            wf.writelines(f'{idpage}\n')
                thread = threading.Thread(target=fl, args=(token_page, head, pxs, self.idpage_follow, idpage, self.uid, index))
                thread.start()
                thread.join()
                index += 1

def getToken(cookie, pxs):
    try:
        response = requests.get('https://mbasic.facebook.com', headers={'cookie': cookie}, proxies=pxs).text
        fb_dtsg = response.split('<input type=\"hidden\" name=\"fb_dtsg\" value=\"')[1].split('\"')[0]
        app_id = '350685531728'
        url = f'https://www.facebook.com/dialog/oauth/business/cancel/?app_id={app_id}&version=v12.0&logger_id=&user_scopes[0]=user_birthday&user_scopes[1]=user_religion_politics&user_scopes[2]=user_relationships&user_scopes[3]=user_relationship_details&user_scopes[4]=user_hometown&user_scopes[5]=user_location&user_scopes[6]=user_likes&user_scopes[7]=user_education_history&user_scopes[8]=user_work_history&user_scopes[9]=user_website&user_scopes[10]=user_events&user_scopes[11]=user_photos&user_scopes[12]=user_videos&user_scopes[13]=user_friends&user_scopes[14]=user_about_me&user_scopes[15]=user_posts&user_scopes[16]=email&user_scopes[17]=manage_fundraisers&user_scopes[18]=read_custom_friendlists&user_scopes[19]=read_insights&user_scopes[20]=rsvp_event&user_scopes[21]=xmpp_login&user_scopes[22]=offline_access&user_scopes[23]=publish_video&user_scopes[24]=openid&user_scopes[25]=catalog_management&user_scopes[26]=user_messenger_contact&user_scopes[27]=gaming_user_locale&user_scopes[28]=private_computation_access&user_scopes[29]=instagram_business_basic&user_scopes[30]=user_managed_groups&user_scopes[31]=groups_show_list&user_scopes[32]=pages_manage_cta&user_scopes[33]=pages_manage_instant_articles&user_scopes[34]=pages_show_list&user_scopes[35]=pages_messaging&user_scopes[36]=pages_messaging_phone_number&user_scopes[37]=pages_messaging_subscriptions&user_scopes[38]=read_page_mailboxes&user_scopes[39]=ads_management&user_scopes[40]=ads_read&user_scopes[41]=business_management&user_scopes[42]=instagram_basic&user_scopes[43]=instagram_manage_comments&user_scopes[44]=instagram_manage_insights&user_scopes[45]=instagram_content_publish&user_scopes[46]=publish_to_groups&user_scopes[47]=groups_access_member_info&user_scopes[48]=leads_retrieval&user_scopes[49]=whatsapp_business_management&user_scopes[50]=instagram_manage_messages&user_scopes[51]=attribution_read&user_scopes[52]=page_events&user_scopes[53]=business_creative_transfer&user_scopes[54]=pages_read_engagement&user_scopes[55]=pages_manage_metadata&user_scopes[56]=pages_read_user_content&user_scopes[57]=pages_manage_ads&user_scopes[58]=pages_manage_posts&user_scopes[59]=pages_manage_engagement&user_scopes[60]=whatsapp_business_messaging&user_scopes[61]=instagram_shopping_tag_products&user_scopes[62]=read_audience_network_insights&user_scopes[63]=user_about_me&user_scopes[64]=user_actions.books&user_scopes[65]=user_actions.fitness&user_scopes[66]=user_actions.music&user_scopes[67]=user_actions.news&user_scopes[68]=user_actions.video&user_scopes[69]=user_activities&user_scopes[70]=user_education_history&user_scopes[71]=user_events&user_scopes[72]=user_friends&user_scopes[73]=user_games_activity&user_scopes[74]=user_groups&user_scopes[75]=user_hometown&user_scopes[76]=user_interests&user_scopes[77]=user_likes&user_scopes[78]=user_location&user_scopes[79]=user_managed_groups&user_scopes[80]=user_photos&user_scopes[81]=user_posts&user_scopes[82]=user_relationship_details&user_scopes[83]=user_relationships&user_scopes[84]=user_religion_politics&user_scopes[85]=user_status&user_scopes[86]=user_tagged_places&user_scopes[87]=user_videos&user_scopes[88]=user_website&user_scopes[89]=user_work_history&user_scopes[90]=email&user_scopes[91]=manage_notifications&user_scopes[92]=manage_pages&user_scopes[93]=publish_actions&user_scopes[94]=publish_pages&user_scopes[95]=read_friendlists&user_scopes[96]=read_insights&user_scopes[97]=read_page_mailboxes&user_scopes[98]=read_stream&user_scopes[99]=rsvp_event&user_scopes[100]=read_mailbox&user_scopes[101]=business_creative_management&user_scopes[102]=business_creative_insights&user_scopes[103]=business_creative_insights_share&user_scopes[104]=whitelisted_offline_access&redirect_uri=fbconnect%3A%2F%2Fsuccess&response_types[0]=token&response_types[1]=code&display=page&action=finish&return_scopes=false&return_format[0]=access_token&return_format[1]=code&tp=unspecified&sdk=&selected_business_id=&set_token_expires_in_60_days=false'
        response = requests.post(url, headers={'cookie': cookie}, data={'fb_dtsg': str(fb_dtsg)}, proxies=pxs)
        token_fb = re.findall('access_token=([^\"]*)&data_access_expiration_time', response.text)[0]
        return token_fb
    except:
        return False

def get_token_1(cookie):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'priority': 'u=0, i',
        'sec-ch-ua': '\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '\"Windows\"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    get = requests.get('https://business.facebook.com/content_management', headers=headers).text
    try:
        token = 'EAAG' + get.split('EAAG')[1].split('\"')[0]
        return token
    except:
        return False

proxy_data = []
if os.path.exists('proxy.txt'):
    list_proxy = open('proxy.txt', 'r', encoding='utf-8').readlines()
    proxy_data = []
    for proxy in list_proxy:
        proxy = proxy.strip()
        if '@' not in proxy:
            try:
                proxy_authen = {'host': proxy.split(':')[0], 'port': proxy.split(':')[1], 'user': proxy.split(':')[2], 'pass': proxy.split(':')[3]}
                proxy_data.append(f"http://{proxy_authen['user']}:{proxy_authen['pass']}@{proxy_authen['host']}:{proxy_authen['port']}")
            except:
                proxy_authen = {'host': proxy.split(':')[0], 'port': proxy.split(':')[1]}
                proxy_data.append(f"http://{proxy_authen['host']}:{proxy_authen['port']}")
        else:
            try:
                proxy_authen = {'host': proxy.split('@')[1].split(':')[0], 'port': proxy.split('@')[1].split(':')[1], 'user': proxy.split('@')[0].split(':')[0], 'pass': proxy.split('@')[0].split(':')[1]}
                proxy_data.append(f"http://{proxy_authen['user']}:{proxy_authen['pass']}@{proxy_authen['host']}:{proxy_authen['port']}")
            except:
                proxy_authen = {'host': proxy.split('@')[1].split(':')[0], 'port': proxy.split('@')[1].split(':')[1]}
                proxy_data.append(f"http://{proxy_authen['host']}:{proxy_authen['port']}")

file_ck = 'cookie.txt'
banner()
syed = 0
cp = 0
all_ck = open(file_ck, 'r').read().split('\n')
l_idfl = open('link.txt', 'r').read().split('\n')
idfollow = random.choice(l_idfl)

def main(cookie, idfollow):
    if proxy_data != []:
        proxy = random.choice(proxy_data)
        proxies = {'http': proxy, 'https': proxy}
    else:
        proxies = {}
    thread1 = myThread(proxies, cookie, idfollow)
    thread1.run()
for cookie in all_ck:
    try:
        threading.Thread(target=main, args=(cookie, idfollow)).start()
        sleep(0.1)
    except:
        pass

input()
