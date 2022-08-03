def get_token(request):
    bearer_token = request.headers.get('Authorization', None)
    return str(bearer_token)[7:] if bearer_token is not None else None
