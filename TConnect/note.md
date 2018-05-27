# ImageCollection

base url
http://17chuchu.pythonanywhere.com/SystemArt/

# LOGIN
http://17chuchu.pythonanywhere.com/SystemArt/login/
- **TAKES**
- - username
- - password
- - {"username": "admin", "password": "1234"}

- **RETURNS**
- - tag ( 0 = success, 1 = failed )
- - comment ( when successful, it will be used further as an authtoken )
- - id ( user id )
- - {"tag": 0, "comment": "620788cacfa642c297512c616730340a", "id": "5ad5f710eb1243bf95f05ec7ce6ce6b7"}

# REGISTER CREATOR
http://17chuchu.pythonanywhere.com/SystemArt/register/
- **TAKES**
- - name
- - username
- - password
- - email
- - {"name": "Chutmongkol Chuasaard", "username": "sassyboi69", "password": "123456", "email": "17chuchu.guy@gmail.com"}

- **RETURNS**
- - tag ( 0 = success, 1 = ???, 2 = email used 3 = already exist )
- - comment
- - {"tag": 0, "comment": "Your registeration for saitama is completed."}

# REGISTER ADMIN
http://17chuchu.pythonanywhere.com/SystemArt/registeradmin/
- **TAKES**
- - authtoken
- - name
- - username
- - passowrd
- - email
- - {"authtoken":"375e37447b5d4431a2ac15e36aadfbfe" ,"name":"Admin","username":"admin","password":"1234","email":"17chuchu.guy@gmail.com"}
- **RETURNS**
- - tag ( 0 = success, 1 = ???, 2 = ???, 3 = ??? )
- - comment
- - {"tag": 0, "comment": "Your registeration for dude man is completed."}

# LIST CREATORS
http://17chuchu.pythonanywhere.com/SystemArt/listallartist/
- **TAKES**
- - authtoken
- - {"authtoken":"375e37447b5d4431a2ac15e36aadfbfe”}
- **RETURNS**
- - dict of users whose key are ids
- - {'f151dd44-5b7f-4fde-9328-b2589db7ee7a': {'name': 'Chutmongkol Chuasaard', 'email': '17chuchu.guy@gmail.com'}, '49ba06e570c445f9907fd4d6bbeac80c': {'name': 'saitama', 'email': 'sai@to.com'}, 'd93ef94a1cfb473c8e11d8016751a008': {'name': 'saitama', 'email': 'sai@to2.com'}}

# ADD FILE
http://17chuchu.pythonanywhere.com/SystemArt/addfile/
- only add record to database not physical file
- path will be path on your application not path in firebase
- takes
- - authtoken
- - name
- - path
- {"authtoken": "bf1b1bf3ebdc4b3ba38b9bc7b99e2a35","name":"assFile.png", "path":"folder/assfile.png"}

# ADD FILE VERSION
http://17chuchu.pythonanywhere.com/SystemArt/addversion/
- will add record to database of new version
- will return "Successfully created version #PathtouploadfiletoFilebase"
- takes
- - authtoken
- - id
- - version
- - filetype
- {"authtoken": "bf1b1bf3ebdc4b3ba38b9bc7b99e2a35","id”:”idofthefile”, "version”:”12_11_223”, "filetype”:”.jpg”}

# REMOVE FILE
http://17chuchu.pythonanywhere.com/SystemArt/removefile/
- will remove file and all of the version from database and filebase
- takes
- - authtoken
- - id
- {"authtoken": "bf1b1bf3ebdc4b3ba38b9bc7b99e2a35","id”:”idofthefile”}

# LIST ALL FILE
http://17chuchu.pythonanywhere.com/SystemArt/listallfile/
- return list of all file in the project
- takes
- - authtoken
- {"authtoken": "bf1b1bf3ebdc4b3ba38b9bc7b99e2a35”}

# LIST ALL VERSION OF A FILE
http://17chuchu.pythonanywhere.com/SystemArt/listallversionoffile/
- return all version of this file id
- takes
- - authtoken
- - fileid
- {"authtoken": "bf1b1bf3ebdc4b3ba38b9bc7b99e2a35","fileid”:”idofthefile”}