### Individual Assignment 1

1. I used semantic elements like <header>, <section>, <nav>, etc to basically split up the index.html file so it'd be way more easier to not only read, but also provide a good base for future alterations. Keeps things readable and helps tools like search engines or screen readers more easily search around through the portfolio page.
2. Honestly? I was really inspired by some recent games I've played and/or saw online, so I tried to replicate the kinda... edgy skewed shapes. The biggest challenge in that was tryin' to make things work good and look good on all devices. Like, as an example, i used a 2-column grid to place the photo alongside the text to make it more readable on all devices, and made it so that the skews were zeroed out on mobile displays to make it easier on the eyes.
3. Hm... probablya dding new sections. Since it's a purely static web, tryin' to add new things on just the one index.html file has to be manually hardcoded in. I much prefer a system where I just have multiple pages that all interconnect instead of just one page w everything. User interactions on CSS are also kinda limited to only the hoverin' thing from what i found? like, for things that aren't wildly overcomplicated.

P.S. I did use some minor AI assistance through Gemini, mostly on the final bit, the atelier gallery? I was askin' how to do the thing where pressin' the image would show a bigger n clearer version of the image, analyzed the snippet it gave, and then applied it to my own work and made my own half-baked version w the game link thing. Otherwise, all code was independently sourced from... mostly the MDN Web Docs https://developer.mozilla.org/en-US/, and an old book I had as a kid and now as a PDF; CoderDojo's Create With Code: Build Your Own Website https://archive.org/details/createwithcodebu0000hatt_i6t9

### Individual Assignment 2

1. The project's urls.py -> defines the landing page n chooses the views based on the paths, the application url.py -> routes the url to the views it wants, view -> accepts user requests, takes model data, n sends it to the templates, models -> basically the big data form you fill in w things, template -> html file that displays apps
2. I think moreso just bc itd be easier to like. change around? like, switching and changing things is easier if everythin's less cluttered
3. makemigrations = makes a migration file but doesnt apply it yet, migrate = applies it to the big database; thhe use to do one or the other is that. well. sometimes you dont wanna immediately apply changes to the big database so ppl can review frist or to avoid conflicts n whatevs.

P.S. I did use some minor AI assistance through Gemini, kinda because I had a problem with the skills not showing up; turns out? i was being a dumbass and copied the atelier's thing to make skills in the views.py instead of using the experiences thing as a base... so it never had the ability to display skills lmao

### Individual Assignment 2

1. uh... iirc it's because JSON is like. integrated with javascript right? like, it's natively compatible, unlike w/ XML where you gootta do some finagling to get it to work w the shit that's alr present in Django
2. Client sends HTTP request mapped to a specified view -> the view uses Django's ORM to query the database for the requested data -> Database returns data as python objects -> view passes that to a serializer which formats it into a JSON-formatted text string -> View packages the string into an HTTP response and sends that back over to the client
3. Because netowrk protocols like HTTP and frontend browsers can't exactly read oor understand native python objects, so serialization translates it into smth they can actually read

P.S. I. may have forgotten to write this yesterday (Monday, 21st of September 2026). Just goes to show I should not do this while nursing a headache...