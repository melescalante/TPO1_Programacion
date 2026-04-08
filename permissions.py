from data import users

ROLE_LEVELS = {
    "user": 1,
    "admin": 2
}

def has_permission(user, required_level):
    if not user:
        print('Debes logearte para usar el sistema')
        return
    
    user_level = ROLE_LEVELS.get(user.get("rol"), 1)
    
    if user_level >= required_level:
        return True
            
    print('No tienes permiso')
    return False
