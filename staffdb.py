class StaffDB:
    def __init__(self):
        self.credentials = {
            'admin': 'admin',
            'admin2': 'admin2'
        }

    def login(self,username, password):
        if username in self.credentials:
            if self.credentials[username] == password:
                return True

        return False