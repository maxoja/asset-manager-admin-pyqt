import requests


def login(username, password, onsuccess, onfailed, onerror):
    url = "http://17chuchu.pythonanywhere.com/SystemArt/login/"

    data = {}
    data['username'] = username
    data['password'] = password

    print('logging in . . . ')
    response = requests.post(url, json=data)

    if response.ok:
        print('login result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']     # act as token when success

        if tag == 0:
            userid = result['id']
            onsuccess(userid, comment)
        else:
            onfailed(tag, comment)
    else:
        onerror()


def createCreator(name, username, password, email, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/register/'

    data = {}
    data['name'] = name
    data['username'] = username
    data['password'] = password
    data['email'] = email

    print('creating creator . . . ')
    response = requests.post(url, json=data)

    if response.ok:
        print('create creator result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess()
        else:
            onfailed(tag, comment)
    else:
        onerror()

def createAdmin(authtoken, name, username, password, email, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/registeradmin/'

    data = {}
    data['authtoken'] = authtoken
    data['name'] = name
    data['username'] = username
    data['password'] = password
    data['email'] = email

    print('creating admin . . . ')
    response = requests.post(url, json=data)

    if response.ok:
        print('create admin result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess()
        else:
            onfailed(tag, comment)
    else:
        onerror()


if __name__ == '__main__':
    userid = ''
    auth = ''
    def onsuccess(id, token):
        print("login success")
        global auth
        global userid
        auth = token
        userid = id

    def onfailed(tag, comment):
        print("login failed:", tag, comment)

    def onerror():
        print("login error:")

    login('admin', '1234', onsuccess, onfailed, onerror)

    def onsuccess():
        print("create creator success")

    # createCreator('saitama', 'sait3do*!*o', '', 'sai3.com', onsuccess, onfailed, onerror)

    # createAdmin(auth, 'Tawan Thampipattanakul', 'tawan', '1234', 'tawan.tpptnk@gmail.com', onsuccess, onfailed, onerror)


