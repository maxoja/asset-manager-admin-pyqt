# asset-manager-admin-pyqt

## todo
- callback attachable to EditPanel for UPDATE & DELETE
- create right hand side form to edit user details
- fetch delay transition
- put things together

## EditPanel
- addEditRow( key:str, widgetType:class )
- getEditValue( key:str )
- getEditValueDict()

## LoginDialog
- setVerification
- customized warning dialogue when authentication has failed
- return Accepted when verification success 

## UserListView
- setTitle( text:str )
- setIcon( iconPath:str )
- addUser( user:dict )
- removeUser( key:str, value:str )
- setOnSelectUser( onSelect:func )

## references and stuff
- https://github.com/gmarull/qtmodern
- http://www.freepik.com
- https://www.flaticon.com
