# app.py
from flask import Flask, request, render_template
from tasks import post_to_instagram
from PIL import Image

import json
import os
import time

app = Flask(__name__, static_folder='assets')

# Directories
dirs = {
    'images': 'images'
}
# Load Instagram user credentials from users.json
def load_user_credentials():
    with open('users.json', 'r') as file:
        return json.load(file)

# Resize and save the image
def resize_and_save_image(image, max_width=1080, max_height=1080):
    img = Image.open(image)
    img.thumbnail((max_width, max_height))
    filename, file_extension = os.path.splitext(image.filename)
    resized_image_path = f"{dirs['images']}/{time.time()}{file_extension}"
    img.save(resized_image_path)
    return resized_image_path

@app.route('/admin', methods=['GET'])
def create_instagram_post_form():
    return render_template('admin/index.html')


@app.route('/contribute', methods=['GET'])
def contribute():
    return render_template('contribute.html')



# Save Instagram user credentials to users.json
@app.route('/save_user_credentials', methods=['POST'])
def save_user_credentials():
    username = request.form['username']
    password = request.form['password']

    # Load Instagram user credentials from users.json
    user_credentials = load_user_credentials()

    # Check if the user already exists
    for user in user_credentials:
        if user['username'] == username and user['password'] == password:
            return json.dumps({'success': 0, 'message': 'User already exists!'})

    # Add the new user
    user_credentials.append({
        'username': username,
        'password': password
    })

    # Save the updated user credentials
    with open('users.json', 'w') as file:
        json.dump(user_credentials, file, indent=4)

    return json.dumps({'success': 1, 'message': 'User credentials saved successfully!'})


# Create an Instagram post
@app.route('/post_instagram', methods=['POST'])
def create_instagram_post():
    if 'image' in request.files:
        image = request.files['image']
        caption = request.form['caption']

        # Resize and save the image
        resized_image_path = resize_and_save_image(image)

        # Load Instagram user credentials from users.json
        user_credentials = load_user_credentials()
        
        # Add tasks to the Celery queue for each user
        for user in user_credentials:
            print(f"Adding task to the queue for \"{user['username']}\"")
            #print args user['username'], user['password'], resized_image_path, caption
            print(f"{user['username']}, {user['password']}, {resized_image_path}, {caption}")

            post_to_instagram.apply_async(
                args=(user['username'], user['password'], resized_image_path, caption),
                queue='instagram_posts'
            )

        return json.dumps({'success': 1, 'message': 'Post created successfully!'})
    else:
        return  json.dumps({'success': 0, 'message': 'No image found!'})


















if __name__ == '__main__':
    app.run()
