Replica (Version 0.9.7)
=======

![Replica Dashboard](http://i.imgur.com/FrcnCKy.jpg)

Replica is a Django content management system I originally wrote for clients who wanted a simple and straight forward solution for posting updates. Since then, I've been slowly expanding it, and merged it into my own blog, [A Life Well Played](http://alifewellplayed.com/). Because it's still a work in progress, it's recommended you use at your own risk. File and database structure may yet still change. By 1.0 I'll include DB migrations (if needed).

### Features

* Automatic thumbnail generation for uploaded images
* Post Types. Assign posts different level of importance and style
* Drafts. All revisions for entries are saved and compared to the most recent content.
* Markdown Support. Replica uses a simple markdown editor which even allows you to preview content with a click of a button.
* Responsive. The Dashboard is mobile friendly, in both reviewing and publishing new content.
* Charts! Powered by Charts.js, charts are generated on the fly to see posting history.

### Getting Started

At 1.0, I'll have a proper way to install Replica. Until then, it's pretty straight forward:

* Copy the 'replica' (and optional 'core') directory to your apps directory.
* 'templates' contents should be placed in your 'templates' directory. 'Pulse' is the frontend blog portion of Replica, while 'dashboard' is the admin area used to manage content.
* The 'replica' directory in 'static' should remain in tact and placed wherever you serve your static media from.


### Contribute

My immediate priority is better unit tests and docs, but feel free to send pull requests on additional features and bug fixes you might find. Right now, the UI assets (CSS/JS/Images) are minified and merged with the app repo. In a future update I plan to fork the UI assets into a separate repo to allow more user customization.  
