from .test_setup import TestSetup


class TestViews(TestSetup):
    def test_1_register_noInput_failed(self):
        print("Test register Failed")
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['email'], ['This field is required.'])
        self.assertEqual(response['username'], ['This field is required.'])
        self.assertEqual(response['password'], ['This field is required.'])
        self.assertEqual(response['password2'], ['This field is required.'])
        print('Success!!!')
    
    def test_2_register_success(self):
        print("Test register Success")
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertEqual(response['response'], 'successfully registered new user.')
        self.assertEqual(response['email'], self.user_data['email'])
        self.assertEqual(response['username'], self.user_data['username'])
        print('Success!!!')

    def test_3_login_failed(self):
        print("Test login Failed")
        wrong_credentials = {
            "username": "failed@gmail.com",
            "password": "failedtest"
        }
        response = self.client.post(self.login_url, wrong_credentials)
        self.assertEqual(response.status_code, 400)
        response = response.json()
        self.assertEqual(response['non_field_errors'], ['Unable to log in with provided credentials.'])
        print("Success!!!")

    def test_4_login_success(self):
        print("Test login Success")
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        print("Success!!!")