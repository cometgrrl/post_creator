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

import datetime # to parse the date from the filename
import os # to get and move the files
import subprocess # to run git commands

test_mode = False
REPO_ROOT = "/Users/brienna/Code/puppydogkisses"
REPOSITORY_PATH = f"{REPO_ROOT}/content/blog/"
IMAGES_FOLDER = "/Users/brienna/Code/puppydogkisses_images_for_posts/"

def run_git(command, cwd, description):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode == 0:
        if result.stdout.strip():
            print(f"{description} output: {result.stdout.strip()}")
    else:
        print(f"{description} failed.")
        if result.stdout.strip():
            print("Output:", result.stdout.strip())
        if result.stderr.strip():
            print("Error:", result.stderr.strip())
    return result

def ensure_repo_ready(repo_root):
    status_result = subprocess.run(
        "git status --porcelain",
        shell=True,
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    if status_result.returncode != 0:
        print("Git status check failed.")
        if status_result.stderr.strip():
            print("Error:", status_result.stderr.strip())
        return False
    if status_result.stdout.strip():
        print("Repo has uncommitted changes. Please commit/stash them first.")
        print("Status output:", status_result.stdout.strip())
        return False

    fetch_result = run_git("git fetch --prune", repo_root, "Git fetch")
    if fetch_result.returncode != 0:
        return False

    pull_result = run_git("git pull --rebase", repo_root, "Git pull --rebase")
    if pull_result.returncode != 0:
        print("Rebase failed. Resolve conflicts or run 'git rebase --abort'.")
        return False

    status_after = subprocess.run(
        "git status --porcelain",
        shell=True,
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    if status_after.returncode != 0:
        print("Git status check failed after sync.")
        if status_after.stderr.strip():
            print("Error:", status_after.stderr.strip())
        return False
    if status_after.stdout.strip():
        print("Repo is not clean after sync. Please resolve and retry.")
        print("Status output:", status_after.stdout.strip())
        return False

    return True

def is_jpeg_file(file_path):
    try:
        with open(file_path, "rb") as handle:
            start = handle.read(2)
            if start != b"\xff\xd8":
                return False
            handle.seek(-2, os.SEEK_END)
            end = handle.read(2)
            return end == b"\xff\xd9"
    except OSError:
        return False

def normalize_image_filename(file_name, folder_path):
    file_path = os.path.join(folder_path, file_name)
    base_name, extension = os.path.splitext(file_name)
    extension = extension.lower()

    if extension in [".jpeg", ".jpg"]:
        return file_name
    if extension == "":
        if is_jpeg_file(file_path):
            new_name = f"{file_name}.jpeg"
            new_path = os.path.join(folder_path, new_name)
            if os.path.exists(new_path):
                print(f"Skipping {file_name}: {new_name} already exists.")
                return None
            os.replace(file_path, new_path)
            print(f"Added .jpeg extension: {file_name} -> {new_name}")
            return new_name
        print(f"Skipped non-JPEG file with no extension: {file_name}")
        return None
    print(f"Skipped unsupported file type: {file_name}")
    return None

class BlogPost:
    def __init__(self, image_file_name):
        self.image_file = image_file_name
        self.filename = os.path.splitext(image_file_name)[0] # save the filename without the extension
        self.markdown_file = f"{self.filename}.md"
        self.markdown_image_path = f"/img/{self.image_file}" # set the image path based on the filename
        self.title_string = ""
        self.tags = []
        self.image_file_path = f"{IMAGES_FOLDER}{self.image_file}"
        self.destination_path = f"{REPOSITORY_PATH}{self.image_file}"
        self.markdown_file_path = f"{IMAGES_FOLDER}{self.markdown_file}"
        self.markdown_destination_path = f"{REPOSITORY_PATH}{self.markdown_file}"
        self.repo_image_rel = f"content/blog/{self.image_file}"
        self.repo_markdown_rel = f"content/blog/{self.markdown_file}"
        self.files_to_commit = []

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
        try:
            self.files_to_commit = []
            os.replace(self.image_file_path, self.destination_path)
            self.files_to_commit.append(self.repo_image_rel)

            if os.path.exists(self.markdown_destination_path):
                if os.path.exists(self.markdown_file_path):
                    os.remove(self.markdown_file_path)
                print(f"Markdown already exists, leaving unchanged: {self.markdown_file}")
            else:
                os.replace(self.markdown_file_path, self.markdown_destination_path)
                self.files_to_commit.append(self.repo_markdown_rel)

            print(f"Files moved to repository: {self.filename}, {self.markdown_file}")
            return 0
        except OSError as error:
            print(f"File move failed for {self.filename}.")
            print("Error:", error)
            return 1

def publish_posts(files_to_commit):
    if not files_to_commit:
        print("No files to publish.")
        return 1

    unique_files = list(dict.fromkeys(files_to_commit))
    today = datetime.date.today()
    git_add_command = "git add " + " ".join(unique_files)
    git_commit_command = f"git commit -m 'New posts for {today}'"
    git_push_command = "git push -u origin HEAD"

    add_result = run_git(git_add_command, REPO_ROOT, "Git add")
    if add_result.returncode != 0:
        print("Files were not added.")
        return 1

    commit_result = run_git(git_commit_command, REPO_ROOT, "Git commit")
    if commit_result.returncode != 0:
        print("Files were not committed.")
        return 1

    push_result = run_git(git_push_command, REPO_ROOT, "Git push")
    if push_result.returncode != 0:
        print("Files were not pushed.")
        return 1

    print("Files were successfully pushed.")
    return 0

#images_folder_path = "/Users/brienna/Documents/PuppyDogKisses"  # replaced with IMAGES_PATH
files = os.listdir(IMAGES_FOLDER)
post_list = []
created_count = 0
result = -1
# Check if there are files in the folder, if so, create a post for each image (.jpeg) file
if files:
    for file in files:
        file_path = os.path.join(IMAGES_FOLDER, file)
        if not os.path.isfile(file_path):
            continue
        normalized_name = normalize_image_filename(file, IMAGES_FOLDER)
        if not normalized_name:
            continue
        blog_post = BlogPost(normalized_name)
        result = blog_post.create_markdown_file() # Create markdown file 
        if result == 0:
            post_list.append(blog_post)  # Append the result to the list
            created_count += 1 # Increment the post count
if created_count == 1:
    print(f"{created_count} post successfully created.")
elif created_count > 1:
    print(f"{created_count} posts successfully created.")
else: print("No posts were created.")

files_to_commit = []
moved_count = 0
publish_result = -1

if test_mode is False: # check for test mode
    if post_list and not ensure_repo_ready(REPO_ROOT):
        print("Repository not ready. Aborting.")
        exit(1)
    for post in post_list: # move the files to the repository location, if not in test mode
        move_result = BlogPost.move_files(post)
        if move_result == 0:
            moved_count += 1
            if post.files_to_commit:
                files_to_commit.extend(post.files_to_commit)
            print(f"Post staged for publish: {post.image_file}")
    if moved_count == 1:
        print("1 post moved.")
    elif moved_count > 1:
        print(f"{moved_count} posts moved.")
    else:
        print("No posts were moved.")

    if files_to_commit:
        publish_result = publish_posts(files_to_commit)
        if publish_result == 0:
            print("Publish completed.")
        else:
            print("Publish failed.")
    else:
        print("No files to publish.")
else:
    print("Test mode: files not moved or commited to repository.")
