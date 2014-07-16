Replica (Version 0.9.8)
=======

![Replica Dashboard](http://i.imgur.com/FrcnCKy.jpg)

Replica is a Django content management system I originally wrote for clients who wanted a simple and straight forward solution for posting updates. Since then, I've been slowly expanding and rebuilding it, and merged it into my own blog, [A Life Well Played](http://alifewellplayed.com/). Because it's still a work in progress, it's recommended you use at your own risk. You should probably have a good understanding of Django if you want to incorporate this into your project. File and database structure is also still a work in progress. By 1.0, I'll start including DB migrations (if needed).


## Features

* Automatic thumbnail generation for uploaded images
* Post Types. Assign posts different level of importance and style
* Topics. Assign any number topics/categories to posts. All topics have their own settings, including thumbnail images.
* Drafts. All revisions for entries are saved and can be compared to the most recent content.
* Markdown Support. Replica uses a simple markdown editor which even allows you to preview content with a click of a button.
* Quick post. Quickly jot down an idea from the frontpage of the dashboard, and expand on it later on.
* Responsive. The Dashboard is mobile friendly, in both reviewing and publishing new content.
* Charts! Powered by Charts.js, charts are generated on the fly to see posting history.

## Getting Started

At 1.0, I'll have a proper way to install Replica. Until then, it's pretty straight forward:

* Copy the 'replica' (and optional 'core') directory to your apps directory.
* 'templates' contents should be placed in your 'templates' directory. 'Pulse' is the frontend blog portion of Replica, while 'dashboard' is the admin area used to manage content.
* The 'replica' directory in 'static' should remain in tact and placed wherever you serve your static media from.
* I've included the basic template files needed to use the app in your own project, but you still need to provide your own CSS/layout for the site. base.html in the templates directory will also require you to make your own modifications.

## Contribute

My immediate priority is better unit tests and docs, but feel free to send pull requests on bug fixes you might find. Right now, the UI assets (CSS/JS/Images) are minified and merged with the app repo. In a future update I plan to fork the UI assets for the dashboard into a separate repo to allow more user customization.

## Support

This software is provided 'as-is'. I can not help you get this working with your project, or offer any kind of support at this moment. If you believe you encountered a bug, open an [issue on Github](https://github.com/underlost/Replica/issues).

## License

Replica is released under the [MIT License](LICENSE).
