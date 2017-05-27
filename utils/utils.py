def getSecretData():
    with open("secrets.txt", "r") as secrets:
        info = secrets.readlines()
        secretsDict = {
            'APP_SECRET_KEY': secrets[0],
            'EMAIL_ADDRESS': secrets[1],
            'EMAIL_PASSWORD': secrets[2]
        }
        return secretsDict
