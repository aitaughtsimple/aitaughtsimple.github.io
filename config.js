/*
  SITE SETTINGS: the one place to change the club's details.

  Change a value below, save, and push. Every page (the website and the
  flyer) reads from here.

  Two things live outside this file on purpose:
  1. Link previews (the title and card people see when you text or email
     the link) are read by apps that do not run this file. If you change
     the name, also update the lines marked RENAME at the top of
     index.html and flyer/index.html.
  2. The QR code on the flyer is an image. If you change `url`, run
     `python3 tools/make_qr.py` to make a new one (see README.md).
*/
window.SITE = {
  name: "AI Taught Simple",
  email: "aitaughtsimple@gmail.com",

  // The public web address. The flyer prints this and its QR code points here.
  url: "https://aitaughtsimple.github.io/",

  // Who runs it. First names only.
  team: "Jaiden and Shubh",
  school: "Glenelg High School",
  area: "Howard County, Maryland",

  // Shown in the "Upcoming classes" section and on the flyer.
  firstClasses: "January 2027"
};
