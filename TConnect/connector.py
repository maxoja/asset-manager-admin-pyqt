import requests

__USERID = ''
__AUTHTOKEN = ''

def loggedIn():
    return __USERID != ''

def hasToken():
    return __AUTHTOKEN != ''

def getAuthToken():
    return __AUTHTOKEN

def getUserID():
    return __USERID


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
            global __USERID
            global __AUTHTOKEN
            __USERID = result['id']
            __AUTHTOKEN = comment
            onsuccess()
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

def createAdmin(name, username, password, email, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/registeradmin/'

    data = {}
    data['authtoken'] = getAuthToken()
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

def getCreatorList(onreceive, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/listallartist/'
    data = {}
    data['authtoken'] = getAuthToken()

    print('getting creator list . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('get creator list result:', response.text)
        onreceive(response.json())
    else:
        onerror()

# add file
def addFile(name, path, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/addfile/'
    data = {}
    data['authtoken'] = getAuthToken()
    data['name'] = name
    data['path'] = path

    print('add file . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('add file result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess(comment[-32:])
        else:
            onfailed(tag, comment)
    else:
        onerror()

# add file version
def addVersion(fileid, version, filetype, onsuccess, onfailed, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/addversion/'
    data = {}
    data['authtoken'] = getAuthToken()
    data['id'] = fileid
    data['version'] = version
    data['filetype'] = filetype

    print('add version . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('add version result:', response.text)
        result = response.json()
        tag = result['tag']
        comment = result['comment']

        if tag == 0:
            onsuccess(comment[-32:])
        else:
            onfailed(tag, comment)
    else:
        onerror()

# remove file

# list all file
def getFileList(onreceive, onerror):
    url = 'http://17chuchu.pythonanywhere.com/SystemArt/listallfile/'
    data = {}
    data['authtoken'] = getAuthToken()

    print('getting file list . . .')
    response = requests.post(url, json=data)

    if response.ok:
        print('get file list result:', response.text)
        onreceive(response.json())
    else:
        onerror()

# list all version of a file

if __name__ == '__main__':
    def onsuccess():
        print("success")

    def onfailed(tag, comment):
        print("login failed:", tag, comment)

    def onerror():
        print("error:")

    login('admin', '1234', onsuccess, onfailed, onerror)

    # createCreator('saitama', 'sait3do*!*o', '', 'sai3.com', onsuccess, onfailed, onerror)

    # createAdmin(getAuthToken(), 'Tawan Thampipattanakul', 'tawan', '1234', 'tawan.tpptnk@gmail.com', onsuccess, onfailed, onerror)

    def onreceive(result):
        print('receive:', result)

    # getCreatorList(onreceive, onerror)

    getFileList(onreceive, onerror)

    def onsuccess(fileid):
        print("success add file", fileid)

    # addFile("hello.png", "root/hello.png", onsuccess, onfailed, onerror)
    addVersion("5966f98c3e7c4c4cbef4c917d9ef99e8", "1.0", ".png", onsuccess, onfailed, onerror)

