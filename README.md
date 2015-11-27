# gallery-import

Little collection of Python scripts. The idea is to have a one-click solution for importing pictures into a
gallery like [sigal](https://github.com/saimn/sigal). The main script is called autogallery.py and does:

- Check if my local NAS is on, if not switch it on
- Search for .JPG or .jpg files in a dropbox folder called autogallery
- Extract the shooting date of the picture(s) from the EXIF data
- Put the pictures into a monthly folder. If the folder does not exist, create it (including a index.md template for the description)
- Put the pictures also in a separate folder ("new pictures"), which was cleared before.
- Call Sigal
- Sync the whole Sigal output with the webserver
- Send a notification message via Telegram to certain users

Sorry for the german strings in the code, but I think you will understand it easily.

I combined this with a MacOS automator script, which does on the client computer:
- Upload the selected picture to the fileserver via sftp
- Call the autogallery.py via ssh


So now my wife could on her Mac right-click on a picture and it will automagically put into our web gallery. And the whole family gets notified that new baby pictures are available. :)

