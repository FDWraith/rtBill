def getSecretData():
    with open("secrets.txt", "r") as secrets:
        info = secrets.read().split("\n")
        secretsDict = {
            'APP_SECRET_KEY': info[0],
            'EMAIL_ADDRESS': info[1],
            'EMAIL_PASSWORD': info[2]
        }
        return secretsDict

def validate():
    return 'user' in session
