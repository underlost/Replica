Replica (Version 1.0.8)
=======

![Replica Dashboard](http://i.imgur.com/FrcnCKy.jpg)

*(Project is still currently being setup. May not work properly, or may be ouright broken)*

Replica is a Django content management system I originally wrote for clients who wanted a simple and straight forward solution for posting updates. Since then, I've been slowly expanding and rebuilding it, and merged it into my own blog, [A Life Well Played](http://alifewellplayed.com/). More specifically, it's a a series of apps bundled tightly together:

`Pulse`
Pulse is the heart of Replica. Most of the blog things are handled here. The models, views, etc, everything you see for the core of the blog can be found here, while the rest of the apps extend upon it.

`Dashbaord`
Dashboard is the administrative side of things. This is also where the editor resides. If any content (Either posts or pages), media, or anything else needs to be added, it's done in the Dashboard.

`API`
The guts of the API portion of Replica. URLS and reusable permissions can be found here.

`contrib`
The smaller, more optional apps of Replica are located here, such as Blips, a microblogging service, and Whisper, a small form app that allows visitors to submit feedback anonymously.

---

Right now it's currently still in beta, but it is stable and secure enough to run a small blog in production using it. Because it's still a work in progress however, it's recommended you use at your own risk. You should probably have a good understanding of Django if you want to incorporate this into your project. File and database structure is also still a work in progress. By 1.0, I'll start including DB migrations (if needed).


## Features
* Automatic thumbnail generation for uploaded images
* Post Types. Assign posts different level of importance and style
* Topics. Assign any number topics/categories to posts. All topics have their own settings, including thumbnail images.
* Drafts. All revisions for entries are saved and can be compared to the most recent content.
* Markdown Support. Replica uses a simple markdown editor which even allows you to preview content with a click of a button.
* Quick post. Quickly jot down an idea from the frontpage of the dashboard, and expand on it later on.
* Responsive. The Dashboard is mobile friendly, in both reviewing and publishing new content.
* API. Replica features a basic, RESTful API. At the moment it is currently read-only, but future updates will expand that.

## Upcoming Features
* Charts! Powered by Charts.js, charts are generated on the fly to see posting history, along with additional stats.
* Additional Permissions. Currently, only users with the is_staff flag are allowed to login and post.
* Better (read: actual) documentation for Replica and how to use it.

## Getting Started
* Copy the 'replica' (and optional 'coreExtend') directory to your apps directory.
* I've included the basic template files needed to use the app in your own project, but you still need to provide your own CSS/layout for the site. base.html in the templates directory will also require you to make your own modifications.

## Contribute
My immediate priority is better unit tests and docs, but feel free to send pull requests on bug fixes you might find. Right now, the UI assets (CSS/JS/Images) are minified and merged with the app repo. In a future update I plan to fork the UI assets for the dashboard into a separate repo to allow more user customization.

## Support
This software is provided 'as-is'. I can not help you get this working with your project, or offer any kind of support at this moment. If you believe you encountered a bug, open an [issue on Github](https://github.com/underlost/Replica/issues).

## License

Replica is released under the [MIT License](LICENSE).
