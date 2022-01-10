from rest_framework.exceptions import APIException

class BadSearchQueryParameterException(APIException):
	status_code = 400
	default_detail = "poorly formed search query parameter. alphanumeric or '|' only."
	default_code = 'bad query parameter'
