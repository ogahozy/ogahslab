# ogahslab
This is a full stack website powered by Flask web framework and Python. This work is inspired by Miguel Grinberg. check here https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world. 
You can fork and clone it for you own used. I am personally using it as my blogging sites. 
You can also submit pull request for patches and errors. I am just a learner and not an expert

# How to use it
1. git clone https://github.com/ogahozy/ogahslab .
2. cd ogahslab .
3. pip install -r requirements.txt .
4. export FLASK_APP=ogahslab.py .
# you can now add your environment variables
5. export MAIL_USERNAME='your sendgrid username' # if you are using sendgrid account.
6. export MAIL_PASSWORD='you password' .
7. export WEB_ADMIN='you verified sendgrid sender email'.
8. flask run .
# you are done
if you want to push it to heroku just as i did or any other platform, 
then you following Miguel post here https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-heroku .
