# System Design General Goals

In general my goals are to design a federated software platform that makes it easy for trusted community leaders to host the central-model updates on their own server, and create easy to install clients that can be remotely called to do training. In general I want to improve federated learning specifically for smaller grassroots communities that don't have as much corporate support ( disability software among others). As result, massive industrial scaling or power optimization isn't my main priority. I specifically want to create a system that helps to enable privacy-essential machine learning tasks that would otherwise be infeasible for small groups and organizations. Making it easy, intuitive, and secure is my top priority.

# Tech Stack

I currently plan to use the federated learning framework [Flower](https://flower.dev/). This code works on top of existing machine learning frameworks and will allow me to more easily transfer existing machine learning code and approaches.

Flower hosts the server and waits for the clients to start their script.Then once they are connected, it will send instructions to the client regarding how many iterations of training to perform and information to send back.

I plan to create a simple web interface that will allow server operators to view connected devices and monitor the training process. This will likely be done in a web framework like `Next.js`.

Finally I plan to create a client that can query the server and perform the training. I would like this client to be able to run on mobile Linux ARM devices since I believe these are important for the privacy-related goals of my system. This client will most likely be written with Rust and GTK.

## Management and Installation

I will use [Yunohost](https://yunohost.org/en?q=%2Fdocs) to install my application. Yunohost is a free open source self-hosting management tool. It allows users to install applications with a click of a button through a web interface which allows self hosting to be done by more people more easily. This will make it so users don't have to worry about manually configuring nginx configs or managing docker containers. I'm not just concerned about the technical infrastructure but also making it easy to deploy so it can actually have the positive impact socially that I'm looking to achieve.

## Example of the web interface

![](assets/yunohostapps.png?raw=true)
![](assets/yunoconf.png)
