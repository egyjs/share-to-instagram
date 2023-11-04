# tasks.py
from instagrapi import Client
from celery import Celery

# Initialize Celery
app = Celery('instagram_poster', broker='redis://localhost:6379/0')



# Celery task for posting to Instagram
@app.task
def post_to_instagram(username, password, image_path, caption):
    try:
        cl = Client()
        cl.login(username, password)
        
        print(f"Logged in as \"{username}\"")

        # Upload the image
        media = cl.photo_upload(image_path, caption=caption)
        print(f"Uploaded post: \"{media.pk}\"")
        cl.logout()
    except Exception as e:
        print(f'Error: {str(e)}')
