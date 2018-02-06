# Adobe_Sign_API_Itegration
This is a simple web application interface utilizing the Adobe EchoSign API. It's written in Python and uses the Flask micro-framework.

## Prerequisits
In order to deploy our code, we need to create a virtual environment, this way we can install any packages and not have to worry about the main system packages. To do so, open up the terminal and type the following:   
`pip install virtualenv`

Once virtualenv package is installed, navigate to your file destination of choice. You will then follow up with the following command:   
`virtualenv ASIC_Env`

I chose to name my virtualenv ASIC_Env

Next, we need to activate the virtualenv with the following:   
`source ASIC_Env/bin/activate`

Now we can install the packages to run the web application:   
```
pip install Flask
pip install oauth
pip install request
pip install request-oauthlib
pip install Werkzeug
```

Once all the packages have successfully installed, we can clone the git repo into the virtualenv folder. If you named your virtualenv differently, you can simply delete the root folder from the git repo.

## Setting up an Adobe application
1. You need to create an Adobe developer account on https://www.adobe.com/go/esign-dev-create
2. Once the account is created, follow the steps on deploying an applicaiton.
3. After the application is deployed, copy down the `Client ID` as well as  `Client Secret`, open up the `authorization.py` file, and fill in the missing information.
4. You will need to configure the redirect url in Configure OAuth settings to `https://example.com`
5. Lastly, you need to enable `user_read`, `user_write`, `user_login`, `agreement_read`, `agreement_write`, & `agreement_send` and set all their modifiers to self.

## Running the application
In your terminal, navigate into the virtualenv directory. In your terminal, type the follow:   
`python main.py`

This will activate flask and generate a local host on your machine to host the web application.

In your web browser, navigate to the follow page:   
`local:5000`

This should bring you to the following page:
![Alt text](https://github.com/NathanNguyen345/Adobe_Sign_API_Itegration/blob/master/ASIC_Env/images/1_oauth.png)

This is the OAuth 2.0 authorization page. In order to get access to the server on behalf of the application admin, you will need to click the hyperlink. This will populate a new tab and redirect you to the follow screen:
![Alt text](https://github.com/NathanNguyen345/Adobe_Sign_API_Itegration/blob/master/ASIC_Env/images/2_verify.png)

You will need to sign in as the application admin that's associated with the client id that you used earlier. Once you've signed in, you'll be redirected to https://example.com, which you will then copy the callback url. Next, you will paste the callback url into the main authorization page and click get token. This will bring you to the upload documentation page:
![Alt text](https://github.com/NathanNguyen345/Adobe_Sign_API_Itegration/blob/master/ASIC_Env/images/3_upload.png)

1. In the user input field, type in a reciepient's email address (example@domain.com). You're allowed to type in multiple reciepients, but each email address must be followed by a space.
2. Upload a file by clicking the upload button. You're allowed to upload any of the following `txt`, `pdf`, `jpg`, `png`, `doc`, `docx`, `gif`, & `rtf`. This can be edited in the `main.py` file. I was using a demo account and Adobe kept sending me an error message to my account saying that the pdf file reached max length, but the file was only 1 page. However, I sent a .rtf file with no issue. The `test1.rtf` file is located in the repo if you want to save it and use that.
3. Click the send button.

You will be redirected to the following page:
![Alt text](https://github.com/NathanNguyen345/Adobe_Sign_API_Itegration/blob/master/ASIC_Env/images/4_send_file.png)

Lastly, if you check the recipients email, you will see the document is there for you to sign.
![Alt text](https://github.com/NathanNguyen345/Adobe_Sign_API_Itegration/blob/master/ASIC_Env/images/5_email.png)
