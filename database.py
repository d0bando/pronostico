from deta import Deta  

DETA_KEY = "e0acacrrdtu_KfRQsfJAucaNo9ByZpxEAEvghVz2L6DL"

# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
base = deta.Base("lri_client_database")
drive = deta.Drive("archivos_database")

def insert_user(username, name, email, parameters,password, drivers):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return base.put({"key": username, "name": name, "email": email, "parameters": parameters, "password": password,  "drivers": drivers})


def fetch_all_users():
    """Returns a dict of all users"""
    res = base.fetch()
    res_dic = res.items
    transformed_data = {
        "usernames": {entry["key"]: {
            "email": entry["email"],
            "name": entry["name"],
            "password": entry["password"]
        } for entry in res_dic}
    }
    return transformed_data

# @st.cache_resource
def fetch_user(username):
    return base.fetch({"key": f"{username}"}).items[0]



def get_user(username):
    """If not found, the function will return None"""
    return base.get(username)


def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return base.update(updates, key=username)


def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return base.delete(username)

def create_drive(username, file):
    return drive.put(name=f"{username}/table.xlsx",data=file)

# @st.cache_resource
def get_drive(username):
    file = drive.get(f"{username}/table.xlsx")
    
    if file is None:
        return file
    else:
        return file.read()