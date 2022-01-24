from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import *
import logging

logging.basicConfig(filename='log.txt')
# Create your tests here.

#TODO Model Tests
#TODO Serializer/Validator Tests
#TODO Endpoint/Permissions Tests


#ENDPOINT/PERMISSIONS TESTS####################################################################
anonymous_credential_data = {}
valid_user_credential_data =  {'username':'ftester', 'password':'password'}
invalid_user_credential_data =  {'username':'dtester', 'password':'password'}
superuser_credential_data =  {'username':'root', 'password':'password'}

class acquireTokenTestCase(TestCase):
    """separate test case to acquire tokens since all endpoint tests depend on getting token. 
        - test that anonymous users can NOT acquire a token
        - test that both authenticated users CAN acquire a token
        - test that super user CAN acquire a token
    """
    #def test_anonymous_can_not_get_token(self):
    #    response = Client().post(
    #            reverse('token_obtain_pair'),
    #            anonymous_credential_data,
    #            format='json',
    #            #Content_type="application/json"
    #            )
    #    self.assertEqual(response.status_code, 400)
    #    self.assertFalse('access' in response.data.keys())
	
    def test_valid_authenticated_can_get_token(self):
        response = Client().post(
                reverse('token_obtain_pair'),
                valid_user_credential_data,
                extra={'CONTENT_TYPE':'application/json'}
                )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data.keys())

    def test_invalid_authenticated_can_get_token(self):
        response = Client().post(
                reverse('token_obtain_pair'),
                invalid_user_credential_data,
                extra={'CONTENT_TYPE':'application/json'}
                )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data.keys())

    def test_superuser_can_get_token(self):
        response = Client().post(
                reverse('token_obtain_pair'),
                superuser_credential_data,
                extra={'CONTENT_TYPE':'application/json'}
                )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data.keys())


class EndpointTestCase(TestCase):
    """base class for all endpoint tests
        - gets tokens for all types of authenticated users
        - adds a 'get_response' helper method to generate responses from request data
        - adds run_test_matrix method to run assertion tests for each request in self.permissions_matrix
    """


    def __init__(self, *args, **kwargs):
        """
            - describes necessary fields in any child classes derived from this one
            - gets JWT authentication tokens for child classes. do not need to do that in child classes
        """
        super(EndpointTestCase, self).__init__(*args, **kwargs)

        #should be set in concrete EndPointTestCase
        self.base_url = ""
        self.valid_slug = ""

        #for each EndpontTestCase, a permissions matrix will be used
        # and the self.run_test_matrix method should be called to do the following:
        #   1. call self.get_response to generate jwt token and get a response from permission data   
        #   2. do an assertion test to compare response.status_code to exp_code

        #PLACEHOLDER to show format of self.permissions_matrix. 
        #this should be populated in each EndpontTestCase's constructors 
        #and should have entries for each desired test
        self.permissions_matrix = [
                {"user_type":"anon", "http_method":"get", "data":None, "slug":"", "exp_data":None, "exp_code":401},
                {"user_type":"anon", "http_method":"post", "data":{"email": "bob@test.com"}, "slug":"", "exp_data": {"field": "email", "value": "bob@test.com"},"exp_code":401},
                {"user_type":"anon", "http_method":"patch", "data":{"email": "bobby2@test.com"}, "slug":"", "exp_data": {"field": "email", "value": "bobby2@test.com"},"exp_code":401}


        ]


        self.valid_user_access_token = Client().post(
                reverse('token_obtain_pair'),
                valid_user_credential_data,
                extra={'CONTENT_TYPE':'application/json'}
                ).data['access']

        self.invalid_user_access_token = Client().post(
                reverse('token_obtain_pair'),
                invalid_user_credential_data,
                extra={'CONTENT_TYPE':'application/json'}
                ).data['access']

        self.superuser_access_token = Client().post(
                reverse('token_obtain_pair'),
                superuser_credential_data,
                extra={'CONTENT_TYPE':'application/json'}
                ).data['access']
       
    def get_response(self, user_type, http_method, base_url, slug="", data=None):
        """
            builds Client request method to get a response object
            allows us to specify user from a couple categories of users {'anon', 'valid', 'invalid', 'super'}
            takes care of applying the correct JWT token that is associated with this user type
            avoids attaching any authorization header fields if type is 'anon'

            PARAMETERS:
            ----------
                - str user_type : set type of user for request
                    - from options {'anon', 'valid', 'invalid', 'super'}
                    - pulls username and password from global variables
                        - valid_user_credential_data
                        - invalid_user_credential_data
                        - superuser_credential_data
                - str http_method : {"get", "post", "put", "patch", "delete"}
                - str base_url : api endpoint like '/api/users/'
                - str slug : optional slug to append to base-name when accessing individual
                - dict data : optional data to pass in for post,put,patch 
            RETURNS:
            --------
                - django.http.response response : response object
        """

        if user_type not in ['anon','valid', 'invalid', 'super']:
            logging.error('invalid user_type')
            return None

        if http_method not in ['get', 'post', 'put', 'patch', 'delete']:
            logging.error('invalid http_method')
            return None
        
        #header_kwargs_dict = {"CONTENT_TYPE":"application/json"}
        header_kwargs_dict = {
                "format":"json",
                "CONTENT_TYPE": "application/json"
                }
       
        tokenDict = {
                "valid":self.valid_user_access_token,
                "invalid":self.invalid_user_access_token,
                "super":self.superuser_access_token
                }

        #if user is not anonymous, attach a JWT token to the header
        if user_type != 'anon':
            header_kwargs_dict['HTTP_AUTHORIZATION'] = "Bearer "+tokenDict[user_type]
            #logging.error(f"api:tests:get_response:: if user is not anon, then token is: {tokenDict[user_type]}\nheader_kwargs_dict is: {header_kwargs_dict}")

        if http_method == 'get':
            return Client().get(
                    base_url+slug,
                    extra=header_kwargs_dict
                    #HTTP_AUTHORIZATION="Bearer "+token
                    )

        elif http_method == 'post':
            if not data:
                logging.error('post needs data')
                return None
            return Client().post(
                    path=base_url+slug,
                    data=data,
                    extra=header_kwargs_dict
                    )

        elif http_method == 'put':
            if not data:
                logging.error('put needs data')
                return None
            return Client().put(
                    base_url+slug,
                    data,
                    extra=header_kwargs_dict
                    )

        elif http_method == 'patch':
            if not data:
                logging.error('patch needs data')
                return None
            return Client().patch(
                    base_url+slug,
                    data,
                    extra=header_kwargs_dict
                    )

        elif http_method == 'delete':
            return Client().delete(
                    base_url+slug,
                    )
        else:
            logging.error('invalid http method')
            return None

    def run_test_matrix(self):
        """runs all tests from self.permissions_matrix
        """
        for perm in self.permissions_matrix:
            response = self.get_response(
                    user_type=perm['user_type'],
                    http_method=perm['http_method'],
                    base_url=self.base_url,
                    slug=perm['slug'],
                    data=perm['data']
                    )
            self.assertEqual(response.status_code, perm['exp_code'], msg=f"{self.base_url}: {str(perm)}")
            if perm['exp_data']:
                field = perm['exp_data']['field']
                self.assertEqual(response.data[field], perm['exp_data']['value'], msg=f"{self.base_url}: {str(perm)}")




class UsersEndpointTestCase(EndpointTestCase):
    def __init__(self, *args, **kwargs):
        super(UsersEndpointTestCase, self).__init__(*args, **kwargs)

        self.base_url = '/api/users/'
        self.valid_slug = str(User.objects.get(username=valid_user_credential_data['username']).id)+'/'
        
        self.update_email_data = {"email": "updatedEmail@test.com"}

        self.new_user_data = {
                "username":"brandNewUser",
                "password":"password",
                "email":"brandNewUser@test.com"
                }
        self.updated_user_data = {
                "username":"updatedUser",
                "password":"password",
                "email":"updatedUser@test.com"
                }

        self.permissions_matrix = [
#                 {"user_type":"anon", "http_method":"get", "data":None, "slug":"", "exp_data": None, "exp_code":401},
#                {"user_type":"anon", "http_method":"get", "data":None, "slug":self.valid_slug,"exp_data": None, "exp_code":401},
#                {"user_type":"anon", "http_method":"post", "data":self.new_user_data, "slug":"", "exp_data":{"field": "username", "value":self.new_user_data['username']}, "exp_code":201},
#                {"user_type":"anon", "http_method":"put", "data":self.update_email_data, "slug":self.valid_slug, "exp_data": None, "exp_code":401},
#                {"user_type":"anon", "http_method":"patch", "data":self.update_email_data, "slug":self.valid_slug, "exp_data": None, "exp_code":401},
#                {"user_type":"anon", "http_method":"delete", "data":None, "slug":self.valid_slug, "exp_data": None, "exp_code":401},
#
#                 {"user_type":"valid", "http_method":"get", "data":None, "slug":"", "exp_data": None, "exp_code":403},
                  {"user_type":"valid", "http_method":"get", "data":None, "slug":self.valid_slug, "exp_data": {'field':'username', 'value':valid_user_credential_data['username']}, "exp_code":200},
#                 {"user_type":"valid", "http_method":"post", "data":self.new_user_data, "slug":"", "exp_data":None, "exp_code": 403},
#                {"user_type":"valid", "http_method":"put", "data":self.new_user_data, "slug":self.valid_slug, "exp_data": {'field':'username', 'value':self.new_user_data['username']}, "exp_code":200},
                 {"user_type":"valid", "http_method":"patch", "data":self.update_email_data, "slug":self.valid_slug, "exp_data": {'field':'email', 'value':self.update_email_data['email']}, "exp_code":200},
#                {"user_type":"valid", "http_method":"delete", "data":None, "slug":self.valid_slug, "exp_data": None, "exp_code":200},
#
#                {"user_type":"invalid", "http_method":"get", "data":None, "slug":"", "exp_data": None, "exp_code":403},
#                {"user_type":"invalid", "http_method":"get", "data":None, "slug":self.valid_slug, "exp_data": None, "exp_code":403},
#                {"user_type":"invalid", "http_method":"post", "data":self.new_user_data, "slug":"", "exp_data":None, "exp_code": 403},
#                {"user_type":"invalid", "http_method":"put", "data":self.new_user_data, "slug":self.valid_slug, "exp_data": None, "exp_code":403},
#                {"user_type":"invalid", "http_method":"patch", "data":self.update_email_data, "slug":self.valid_slug, "exp_data": None, "exp_code":403},
#                {"user_type":"invalid", "http_method":"delete", "data":None, "slug":self.valid_slug, "exp_data": None, "exp_code":200},
      ]

    def test_all_user(self):
        self.run_test_matrix()
