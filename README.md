Read the doc folder for installation instructions and api/model breakdowns.

NOTES/BUGS/IMPROVEMENTS:
Statistics API returns all status messages for a device. This can be hundreds of messages so a range parameter should probably be added.

We had to fork Chunked Upload ( https://github.com/juliomalegria/django-chunked-upload ) to this project because there were few issues with the original code that were difficult to override. Most notably a callable could not be assigned to upload_to of files.