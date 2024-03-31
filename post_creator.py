# This creates markdown files for new posts on PuppyDogKisses.com based on the file name of the image.
# The format of the markdown file looks like this:
'''
---
image: "/img/20240226__Roxy__Oh_Hi.jpeg"
title: Hi
date: 2024-02-26T15:00:00.000Z
tags: Roxy
---
{% image './20240226__Roxy__Oh_Hi.jpeg', '' %}
'''
# Filenames of the the images will be in the format of YYYYMMDD__tags__title.jpeg, we'll use this to generate the markdown files.

import datetime
import os
import subprocess

test_mode = False
REPOSITORY_PATH = "/Users/brienna/Code/puppydogkisses/content/blog/"
IMAGES_FOLDER = "/Users/brienna/Code/puppydogkisses_images_for_posts/"

class BlogPost:
    def __init__(self, image_file_name):
        self.image_file = image_file_name
        self.filename = image_file_name.split(".")[0] # save the filename without the extension
        self.markdown_file = f"{self.filename}.md"
        self.markdown_image_path = f"/img/{self.image_file}" # set the image path based on the filename
        self.title_string = ""
        self.tags = []
        self.image_file_path = f"{IMAGES_FOLDER}{self.image_file}"
        self.destination_path = f"{REPOSITORY_PATH}{self.image_file}"
        self.markdown_file_path = f"{IMAGES_FOLDER}{self.markdown_file}"
        self.markdown_destination_path = f"{REPOSITORY_PATH}{self.markdown_file}"

    # this function creates a markdown file for a post based on the image filename
    def create_markdown_file(self):
        #check if the post is ready to be published
        if self.filename[:8] <= datetime.datetime.now().strftime('%Y%m%d'):
            print(f"Image is ready for posting: {self.filename}")
        else:
            print(f"Image skipped: {self.filename}")
            return 1
        
        # split the filename into parts so we can get the title, date, and tags
        self.split_filename = self.filename.split("__")
        
        # get the date from the filename
        self.date = datetime.datetime.strptime(self.split_filename[0], '%Y%m%d')
        self.date = self.date.replace(hour=8, minute=0, second=0, microsecond=0)
       
       #get the title from the filename
        title_list = self.split_filename[2].split("_") # add some error handing here
        for word in title_list:
            self.title_string += word
            self.title_string += " "
        print (f'Title: {self.title_string}')

        # get the tags from the filename
        self.tags = self.split_filename[1].split("_") # add some error handing here
        print (f'Tags: {self.tags}') 

        # create the markdown file in the images folder
        with open(f"{IMAGES_FOLDER}{self.markdown_file}", "w") as file:
            file.write(f"---\n")
            file.write(f"image: \"{self.markdown_image_path}\"\n")
            file.write(f"title: {self.title_string}\n")
            file.write(f"date: {self.date}\n")
            file.write(f"tags: {self.tags}\n")
            file.write(f"---\n")
            file.write(f"{{% image './{self.image_file}', '' %}}")
        print (f"{self.markdown_file} created")
        return 0

    # this function moves the images and markdown files to the correct folder
    def move_files(self):        
        os.rename(self.image_file_path, self.destination_path) # add some error handing here
        os.rename(self.markdown_file_path, self.markdown_destination_path) # add some error handing here
        print(f"Files moved to repository: {self.filename}, {self.markdown_file}")
        return 0


    # this function publishes the posts to the blog by adding, committing, and pushing the files to the repository
    def publish_posts(self):
        today = datetime.date.today()
        git_add_command ="git add "
        git_commit_command = f"git commit -m  'New posts for {today}'"
        git_push_command = "git push -u origin HEAD"

        # add filenames to the git add command
        git_add_command += f"{self.image_file} {self.markdown_file} "
        # run the git add command

        os.chdir(REPOSITORY_PATH)
        
        add_result = subprocess.run(git_add_command, shell=True, capture_output=True, text=True)
        if add_result.returncode == 0:
            print("Add command executed successfully.")
            print("Output:", add_result.stdout)        
            print(f"Files were successfully added.")
            # run the git commit command
            commit_result = subprocess.run(git_commit_command, shell=True, capture_output=True, text=True)
            if commit_result.returncode == 0:
                print("Commit command executed successfully.")  
                print("Output:", commit_result.stdout)
                print(f"Files were successfully committed.")
                # run the git push command
                push_result = subprocess.run(git_push_command, shell=True, capture_output=True, text=True)
                if push_result.returncode == 0:
                    print("Push command executed successfully.")
                    print("Output:", push_result.stdout)
                    print(f"Files were successfully pushed.")
                else:
                    print("Push command execution failed.")
                    print("Error:", push_result.stderr) 
                    print(f"Files were not pushed.")
                    exit()
            else:
                print("Commit command execution failed.")
                print("Error:", commit_result.stderr)
                print(f"Files were not committed.")
                exit()
        else:
            print("Add command execution failed.")
            print("Error:", add_result.stderr) 
            print(f"Files were not added.")
            exit()
        return 0

#images_folder_path = "/Users/brienna/Documents/PuppyDogKisses"  # replaced with IMAGES_PATH
files = os.listdir(IMAGES_FOLDER)
post_list = []
created_count = 0
result = -1
# Check if there are files in the folder, if so, create a post for each image (.jpeg) file
if files:
    for file in files:
        if file.endswith(".jpeg"):
            blog_post = BlogPost(file)
            result = blog_post.create_markdown_file() # Create markdown file 
            if result == 0:
                post_list.append(blog_post)  # Append the result to the list
                created_count += 1 # Increment the post count
elif created_count == 1:
    print(f"{created_count} post successfully created.")
elif created_count > 1:
    print(f"{created_count} posts successfully created.")
else: print("No posts were created.")

posts_to_publish = []  # Initialize files_to_publish list
published_count = 0 # Initialize published_count variable
move_result = -1
publish_result = -1

if test_mode is False: # check for test mode
    for post in post_list: # move the files to the repository location, if not in test mode
        move_result = BlogPost.move_files(post)
        if move_result == 0:
            posts_to_publish.append(post)  # Append the post to the list to be published
            print(f"Post added to posts_to_publish: {post.image_file}")
    for post in posts_to_publish: # publish the files to the repository location, if not in test mode
        publish_result = BlogPost.publish_posts(post) # Publish the posts
        if publish_result == 0:
            published_count +=1
            print(f"Post published: {post.image_file}")
else:  print("Test mode: files not moved or commited to repository.")
if published_count == 1:
    print("1 post published.")
else: print(f"{published_count} posts published.")



