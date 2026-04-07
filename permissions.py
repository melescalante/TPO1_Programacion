from data import users, loggedUser, permissions
def middleware(user,function,args):
    if not user:
        print('Debes logearte para usar el sistema', user)
        return
    rol=user["rol"]
    for func in permissions[rol]:
        if func in str(function):
            function(args)
            return True
    print('No tienes permiso')
    return
