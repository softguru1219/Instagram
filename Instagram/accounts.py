import pandas as pd

class Accounts():

    def __init__(self, csv):
        self.df = pd.read_csv(csv)
        self.init_all_accounts()

    def init_all_accounts(self):
        """ Read all accounts from Accounts excel sheet """
        
        self.accounts = (
            [
                {
                    "fullname" : account.Fullname,
                    "email" : account.Email, 
                    "username" : account.Username,
                    "password" : account.Password,
                    "sex" : account.Sex,
                    "bio" : account.Bio,
                    "dp" : account.DP,
                    "created" : account.Created
                }
                for idx, account in self.df.iterrows()
            ]
        )

    def get_all_accounts(self):
        return self.accounts

    def get_volume_accounts(self):
        return len(self.accounts)

    def get_account(self, idx=None,username=None):

        if idx == None and username == None:
            return "No identifier specified!"

        if idx is not None:
            return self.accounts[idx]

        elif username is not None:
            for account in self.accounts:
                if username == account.username:
                    return account
    



        
