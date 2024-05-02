# post_creator
I recently converted [my blog](https://puppydogkisses.com) to an Eleventy blog using Netlify. Now that's done, I wanted to automate publishing new posts.

- Netlify will automatically build the site anytime changes are committed to the [repository](https://github.com/cometgrrl/puppydogkisses).
- Each post consists of an image, tags, a title, and a post date. 
- This makes generating the markdown automatically pretty easy based on a set naming convention for the images.

Here's how it works:
- post_creator.py runs via the crontab on my machine.
- If it finds any .jpeg files in the specified directory, then:
    - For each .jpeg, post_creator checks if the date (YYYYMMDD) in the filename is in the future. If it is, those are skipped.
    - If the date is not in the future, the filename is parsed to make the markdown file.
-  The image filenames are in the format YYYYMMDD__tags__title.jpeg
    - post_creator uses the date as the post date, then fills in the markdown's tags, title, and image parameters.
- Once the markdown files are created, they are moved to the blog's local repository and committed. 
- Netlify will then automatically rebuild the site and voila, new puppy photos are published on [Puppy Dog Kisses](https://puppydogkisses.com).

I didn't do a lot of error handling, that's all for a future version! I did, however, update it to use OOP.
