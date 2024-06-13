import firebase_admin
from firebase_admin import credentials, auth

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate('soil-analysis-crop-reco-firebase-adminsdk-5xkp7-66ebf5eb6a.json')
firebase_admin.initialize_app(cred)

# Function to create a new user
def create_user(email, password):
    user = auth.create_user(email=email, password=password)
    print('Successfully created new user:', user.uid)

# Function to get user details
def get_user_by_email(email):
    user = auth.get_user_by_email(email)
    print('Successfully fetched user data:', user.uid)
    return user

# Function to verify a user by email and password (Firebase Admin SDK doesn't directly support login, but you can create a custom token)
def verify_user(email, password):
    try:
        user = get_user_by_email(email)
        # Create a custom token for the user
        custom_token = auth.create_custom_token(user.uid)
        print('Custom token for user:', custom_token)
        return custom_token
    except firebase_admin.auth.AuthError as e:
        print('Error verifying user:', e)

# Example usage
email = 'Test@gmail.com'
password = '123456'

create_user(email, password)  # Create a new user
user = get_user_by_email(email)  # Get user details
custom_token = verify_user(email, password)  # Verify user and get a custom token
