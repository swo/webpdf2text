# webpdf2text

*webpdf2text* downloads a pdf, converts it to text with *pdftotext*, and shows
the results. You never actually download the pdf. I thought this would be useful
in cases when I had a slow connection: the server downloads the pdf on a fast
connection, and it displayed the reduced information (the text) to me on my slow
connection.

This is a Flask application.

## Notes

To get things working, I had to follow
[this conversation](https://community.c9.io/t/sudo-apt-get-update-isnt-working-on-blank-workspace/10667/5)
to make `apt-get install poppler-utils` to work.

## To do

- Offer the option of pdftotext or pdftohtml