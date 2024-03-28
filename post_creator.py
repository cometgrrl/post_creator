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

# this function creates a markdown file for a post based on the image filename
def create_markdown_file(image_filename):
    #check if the post is ready to be published
    if image_filename[:8] <= datetime.datetime.now().strftime('%Y%m%d'):
       print(f"Image is ready for posting: {image_filename}")
    else:
        print(f"Image skipped: {image_filename}")
        return 0
    # set the image path based on the filename
    md_image_path = f"/img/{image_filename}"
    
    # remove the file extension from the title and split the filename into parts so we can get the title, date, and tags
    filename_without_extension = image_filename.split(".")[0]
    split_filename = filename_without_extension.split("__")
    
    title = split_filename[2].split("_")
    title_string = ""
    for word in title:
        title_string += word
        title_string += " "

    tags = split_filename[1].split("_")

    tag_string = ""

    for tag in tags:
        tag_string += tag
    
    tag_string.strip()
   
    if tag_string[-1:] == ",":
        tag_string = tag_string[:-1] # remove the last comma

    date = datetime.datetime.strptime(split_filename[0], '%Y%m%d')
    date = date.replace(hour=8, minute=0, second=0, microsecond=0)

    # create the markdown file in the images folder
    markdown_filename = f"{filename_without_extension}.md"
    with open(f"{IMAGES_FOLDER}{markdown_filename}", "w") as file:
        file.write(f"---\n")
        file.write(f"image: \"{md_image_path}\"\n")
        file.write(f"title: {title_string}\n")
        file.write(f"date: {date}\n")
        file.write(f"tags: {tag_string}\n")
        file.write(f"---\n")
        file.write(f"{{% image './{image_filename}', '' %}}")
    print (f"{markdown_filename} created")
    return {"image_filename": image_filename, "markdown_filename": markdown_filename}

# this function moves the images and markdown files to the correct folder
def move_files(post):        
    image_file_path = f"{IMAGES_FOLDER}{post['image_filename']}"
    destination_path = f"{REPOSITORY_PATH}{post['image_filename']}"
    md_file_path = f"{IMAGES_FOLDER}{post['markdown_filename']}"
    md_destination_path = f"{REPOSITORY_PATH}{post['markdown_filename']}"
    os.rename(image_file_path, destination_path)
    os.rename(md_file_path, md_destination_path)
    print(f"Files moved to repository: {post['image_filename']}, {post['markdown_filename']}")

    return post


# this function publishes the posts to the blog by adding, committing, and pushing the files to the repository
def publish_posts(file_to_publish):
    today = datetime.date.today()
    git_add_command ="git add "
    git_commit_command = f"git commit -m  'New posts for {today}'"
    git_push_command = "git push -u origin HEAD"

    # add filenames to the git add command
    git_add_command += f"{file_to_publish['image_filename']} {file_to_publish['markdown_filename']} "
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
    return 1

#images_folder_path = "/Users/brienna/Documents/PuppyDogKisses"  # replaced with IMAGES_PATH
files = os.listdir(IMAGES_FOLDER)
created_count = 0  # Initialize post_count variable
post_files = []

# Check if there are files in the folder, if so, create a post for each image (.jpeg) file
if files:
    for file in files:
        if file.endswith(".jpeg"):
            create_result = create_markdown_file(file) # Create markdown file based on the image filename
            if create_result != 0:
                post_files.append(create_result)  # Append the result to the list
                created_count += 1 # Increment the post count
else:
    print("The folder is empty.")
if created_count == 1:
    print(f"{created_count} post successfully created.")
elif created_count > 1:
    print(f"{created_count} posts successfully created.")
else: print("No posts were created.")

files_to_publish = []  # Initialize files_to_publish list
published_count = 0 # Initialize published_count variable

if test_mode is False: # check for test mode
    for post in post_files: # move the files to the repository location, if not in test mode
        move_result = move_files(post)
        files_to_publish.append(move_result)
    for file in files_to_publish: # publish the files to the repository location, if not in test mode
        published_count += publish_posts(file) # Publish the posts
        print(f"Post added to files_to_publish: {post}")
else:  print("Test mode: files not moved or commited to repository.")



