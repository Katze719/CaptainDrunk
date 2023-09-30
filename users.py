
users = {}

def check_user(guild_id, user_name) -> bool:
    if guild_id not in users:
        users[guild_id] = []
    if user_name in users[guild_id]:
        return True
    return False

def add_user(guild_id, user_name) -> str:
    if check_user(guild_id, user_name) == True:
        return 'You are allready in the list!'
    users[guild_id].append(user_name)
    return f'{user_name} added to list!'

def remove_user(guild_id, user_name) -> str:
    if check_user(guild_id, user_name) == False:
        return 'You are not in the list!'
    del users[guild_id][user_name]
    return f'Deleted {user_name} from list!'

def get_users(guild_id) -> str:
    if guild_id not in users:
        return 'List is empty!'
    result = ''
    for user in users[guild_id]:
        result += f'- {user}\n'
    return f'```\n{result}\n```'
