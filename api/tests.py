from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient
from django.urls import reverse
from api.models import *
import logging

#logging.basicConfig(filename='log.txt')

#TODO Model Tests
#TODO Serializer/Validator Tests
#TODO Endpoint/Permissions Tests


#ENDPOINT/PERMISSIONS TESTS####################################################################

class acquireTokenTestCase(TestCase):
    """
        test that JWT tokens can be acquired by authenticated users and super users
        and nobody else
    """

    #did not need setUpTestData since not much shared state between tests
    #for this class, but i used it on following classes
    #and wanted to be consistent

    #should not need to define a teardown function ins setUpTestData rolls back
    #all database operations after all test methods have executed.
    @classmethod
    def setUpTestData(cls):
        cls.superuser_credentials = {
                "username":"token_superuser", 
                "password":"abcd",
                "email":"token_superuser@test.com"
        }
        cls.superuser = User.objects.create_superuser(**cls.superuser_credentials)
        
        cls.valid_user_credentials = {
                "username":"token_valid_user", 
                "password":"efgh",
                "email":"token_valid_user@test.com"
        }
        cls.valid_user = User.objects.create_user(**cls.valid_user_credentials)
  
        cls.invalid_user_credentials = {
                "username":"token_invalid_user", 
                "password":"hijk",
                "email":"token_invalid_user@test.com"
        }
        #no create for invalid user

        cls.client = APIClient()
        cls.token_url = reverse('token_obtain_pair')

    def test_anonymous_can_not_get_token(self):
        response = self.client.post(path=self.token_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('access' not in response.data.keys())
    
    def test_valid_creds_can_get_token(self):
        response = self.client.post(
                path=self.token_url,
                data=self.valid_user_credentials,
                format='json'
                )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data.keys())

    def test_invalid_creds_not_get_token(self):
        response = self.client.post(
                path=self.token_url,
                data=self.invalid_user_credentials,
                format='json'
                )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('access' not in response.data.keys())
    
    def test_superuser_can_get_token(self):
        response = self.client.post(
                path=self.token_url,
                data=self.superuser_credentials,
                format='json'
                )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data.keys())

class AddTokenHeaderMixin:
    token_endpoint = "/api/token/"

    def generate_authorization_header(self, cred_payload=None):
        """
            gets jwt and attaches to http header dictionary for test client requests.
            if no credentials supplied, attach empty dictionary

            PARAMETERS:
            -----------
                - string token_endpoint : relative url of endpoint to acquire tokens from
                - dict cred_payload : user credentials to access API
                    - required fields: "username" and "password"
            
            RETURNS:
            --------
                - dict header_dict : dict with no keywords or, if valid cred_payload, with 
                jwt token attached. 

        """
        #if no credentials supplied, attach nothing to header
        if cred_payload == None:
            return {}

        """
        #if credentials passed with no username and password fields
        if "username" not in cred_payload.keys() and "password" not in cred_payload.keys():
            print(f"tests::EndPointTestCase::generate_authorization_header: cred payload must contain fields for both username and password")
            return None
        """
        data = APIClient().post(path=self.token_endpoint, data=cred_payload, format='json').data
        if 'access' not in data.keys():
            print(f"test::EndPointTestCase::generate_authorization_header: credentials did not produce a key")
            return {}

        return {"HTTP_AUTHORIZATION": f"Bearer {data['access']}" } 

class UserEndpointTestCase(TestCase, AddTokenHeaderMixin):

    @classmethod
    def setUpTestData(cls):
        cls.superuser_cred_payload = {
                "username": "test_superuser",
                "password": "abcd",
                "email": "test_superuser@test.com"
        }
        test_superuser = User.objects.create_superuser(**cls.superuser_cred_payload)

        cls.valid_user_cred_payload = {
                "username": "valid_user",
                "password": "efgh",
                "email": "valid_user@test.com"
        }
        cls.valid_user = User.objects.create_user(**cls.valid_user_cred_payload)

        
        cls.invalid_user_cred_payload = {
                "username": "invalid_user",
                "password": "hijk",
                "email": "invalid_user@test.com"
        }
        cls.invalid_user = User.objects.create_user(**cls.invalid_user_cred_payload)

    def test_superuser_can_list_users(self):
        response = APIClient().get(
                path='/api/users/',
                data=None,
                **self.generate_authorization_header(self.superuser_cred_payload)
                )
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 1)
    
    def test_user_can_not_list_users(self):
        response = APIClient().get(
                path='/api/users/',
                data=None,
                **self.generate_authorization_header(self.valid_user_cred_payload)
                )
        self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_can_not_list_users(self):
        response = APIClient().get(
                path='/api/users/',
                data=None,
                )
        self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_retrieve_user(self):
        response = APIClient().get(
                path=f'/api/users/{self.valid_user.id}/',
                data=None,
                **self.generate_authorization_header(self.superuser_cred_payload)
                )
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.valid_user.username)

    def test_valid_user_can_retrieve_user(self):
        response = APIClient().get(
                path=f'/api/users/{self.valid_user.id}/',
                data=None,
                **self.generate_authorization_header(self.valid_user_cred_payload)
                )
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.valid_user.username)

    def test_invalid_user_can_not_retrieve_user(self):
        response = APIClient().get(
                path=f'/api/users/{self.valid_user.id}/',
                data=None,
                **self.generate_authorization_header(self.invalid_user_cred_payload)
                )
        self.assertTrue(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_can_not_retrieve_user(self):
        response = APIClient().get(
                path=f'/api/users/{self.valid_user.id}/',
                data=None,
                )
        self.assertTrue(response.status_code, status.HTTP_401_UNAUTHORIZED)
