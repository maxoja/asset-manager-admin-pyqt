# asset-manager-admin-pyqt

## todo
- fetch delay transition
- put things together
- add title on EditPanel

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
- setOnClickUpdate( onClick:func(dict, data) )
- setOnClickDelete( onClick:func(dict, data) )

## references and stuff
- https://github.com/gmarull/qtmodern
- http://www.freepik.com
- https://www.flaticon.com
