class LogInTester:
    def is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()
