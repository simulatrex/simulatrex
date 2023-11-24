# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2AuthorizationCodeBearer
# from server.config import settings

# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl="https://accounts.google.com/o/oauth2/auth",
#     tokenUrl="https://oauth2.googleapis.com/token",
#     refreshUrl="https://oauth2.googleapis.com/token",
#     scopes={"openid": "OpenID Connect scope"},
# )


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     async with httpx.AsyncClient() as client:
#         response = await client.get(
#             "https://www.googleapis.com/oauth2/v3/userinfo",
#             headers={"Authorization": f"Bearer {token}"},
#         )
#         if response.status_code != 200:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
#             )
#         user_info = response.json()
#         return user_info  # Or map this to your User model/schema
