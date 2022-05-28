# API Backend for my fullstack web development signature
My initial idea was to create a forum witch would serve post-entries and each entry would contain an HTML file witch later would be displayed in a full post route
## Realization
What end up happening is that Heroku, the site I intend to deploy, did not have a proper filesystem to store the files. So I decided to highly nerf my initial idea, because I did not want to set an S3 just to store some few files and storing base64 strings in a database is not a really good idea (but tempting).
## Actual Project
The actual project is just a very (very) simple Flask API that would fetch posts and push posts to the database, a postgresql database. Each post consist of a title, a body and an image URL.
