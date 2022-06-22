def get_token(request):
    token_data_with_bearer = request.headers['Authorization']
    token = str(token_data_with_bearer)[7:]
    return token
