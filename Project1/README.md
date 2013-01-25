# CS5700: Project 1

Eric Chin (chiner)
Pranav Gandhi (hyfi)

## High Level Approach

With experience with network programming from CS3600 (Systems and Networks),
we were both rather comfortable with the basic concepts in socket programming.
We opted to write our program in Python, which naturally allows us a
"high-level" view in working on this project.  

We divided our program generally into three logical parts: parsing command 
line input, sending and receiving messages, and constructing specific
responses to received messages.

## Challenges

While we didn't face any particularly difficult challenges, we did experience
some minor roadblocks.  Namely, a small logic error resulted in a mysteriously
empty and endless "response" (or what we thought to be a response) and some
amount of confusion.

## Testing

Most of our testing revolved observing our program's interactions with the
server.  Because we knew that the server would terminate our session with any of
our bad input, we used those times as a cue to know when we had a problem.  That
said, our testing was done by our communications with the server and making sure
that our program is usable with the various combinations of uses per the project
instructions.
