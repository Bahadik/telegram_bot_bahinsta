import requests

def parse_content_url(html_code):
    image_text = 'property="og:image"'
    video_text = 'property="og:video:secure_url"'
    str_list = html_code.split()
    result = ''

    for i in range(len(str_list)):
        if str_list[i] == 'content="image"':
            break
        elif str_list[i] == image_text or str_list[i] == video_text: 
            result = str_list[i + 1]
            if result[-2] == '4':
                break

    if result != '':
        result = result[9:-1]

    return result

def get_logined_html_code(login_post, url):
    url_home = 'https://www.instagram.com/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    with requests.Session() as s:
        s.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                          'ig_vw': '1920', 'csrftoken': '',
                          's_network': '', 'ds_user_id': ''})
        s.headers.update({'Accept-Encoding': 'gzip, deflate',
                          'Accept-Language': accept_language,
                          'Connection': 'keep-alive',
                          'Content-Length': '0',
                          'Host': 'www.instagram.com',
                          'Origin': 'https://www.instagram.com',
                          'Referer': 'https://www.instagram.com/',
                          'User-Agent': user_agent,
                          'X-Instagram-AJAX': '1',
                          'X-Requested-With': 'XMLHttpRequest'})
        r = s.get(url_home)
        s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        login = s.post(url_login, data=login_post,
                       allow_redirects=True)
        s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        csrftoken = login.cookies['csrftoken']
        r = s.get(url)
        html_code = r.text
        logout_post = {'csrfmiddlewaretoken': csrftoken}
        logout = s.post(url_logout, data=logout_post)

    return html_code

def get_content_url(login_post, url):
    if login_post == {}:
        r = requests.get(url)
        html_code = r.text
    else:
        html_code = get_logined_html_code(login_post, url)

    return parse_content_url(html_code)

def download_content(login_post, url):
    content_url = get_content_url(login_post, url)
    
    r = requests.get(content_url, stream=True)
    with open('file', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)
