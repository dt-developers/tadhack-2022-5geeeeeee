TADHack Showcase: 5G API Priotization Visualization
===================================================

Hello everyone, welcome to this visualisation of our local, testbed only 5G api network traffic priorization APIs. As a shooter. Done on a weekend. In Python.

What?
=====

Take a look at the screenshots:

<img src="/status/final.png" width="100"/>

That screenshot tells you alot: You see an enemy and the ✂️  represent the activation of the low latency api: While fast, it only does a bit of damage to the evil red dots.

The ✍️ is also here mightier then the sword: If you happen to select the throughput apis as a weapon (hit 2️⃣ ) on the keyboard, you'll be able to shoot stronger, bigger and yellower sessions, but sadly they are more expensive!

Can you kill all the red dot enemies (Lag in network) before your money and your health (?) runs out?

Note for pronounciation: The actual title of the app is `5Geeeeeeee`. Imagine a happy programmer and user being excited about using this app: Yipee. Important is that everytime you say the name, it has to be pronounced just a bit differently.

Also: [YouTube](https://youtu.be/A4ZEjhT8M0g) 

How?
====

I keep dabbling in engines of old, and am happy to learn more on the go, so this time I decided to start building a doom like engine! Please don't go to close to the walls, I still have to figure out how to effectively transfer data from a texture to the screen.

This complete thing works by using [ray casting](https://en.wikipedia.org/wiki/Ray_casting) aka, it shots rays for all columngs of the display and sees where it hits. Smart people have invented [BSPs](https://en.wikipedia.org/wiki/Binary_space_partitioning) for optimizing the amount of calculations to be done. I did not use them.

Instead all columns will check all walls (represented as lines) if their ray shot collides with the line. If there is a collection it is determined if it was in the texture, or if it was outside. Based on a successfull hit, the distance of that intersection can be determined. The inverse of that distance is then used for the hights of the wall.

Since all calculations are 2d, I started with the minimap in the top left corner and build a way of moving the camera and shooting "sessions"(bullets) based on different "apis"(weapons). Once the 2d was established as not too bad, the 3d aspect was taken into account.

There are no floors or ceilings (except for the awesome T and hubraum colors) because those are hard. You would need to shoot another ray from the floor / ceiling to the eye of the camera, to see where they would hit z=0 or z=1(or whatever your wall height is), to then also calculate the right texture coordinate. 

The missing animations for the arm (mine by the way) are to be implemented by the reader. I encourage you to think about using [Karls](https://twitter.com/kommanderkarl)(not affiliated) animations as a basis.

And indeed, the textures are coming directly from the [hubraum](hubraum.com)-offices and my hands.

# Next?

What is next is a break, and thinking about it some more. If you wan to experimient on our 5G APIs outside of this showcase, please head over to our [applications page](https://developer.telekom.com/5g-eap).
