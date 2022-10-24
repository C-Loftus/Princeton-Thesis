# Federated Learning for ML-Based Disability Applications

This repository holds the code and written paper for my Princeton senior thesis in Computer Science.

For individuals with disabilities, machine learning provides a powerful way to create more useful accessibility software. Voice recognition software is a particularly useful example that has allowed many to interact with their computers hands free.

However many models related to these types of specialty tasks suffer from a lack of data, well trained models, and an ecosystem through which to train them. Machine learning tasks that lack corporate incentives often depend upon grassroots communities to collect data and improve models.

Despite these challenges, there are ways to accomplish these goals and build better machine learning systems for specialty tasks and communities.
Currently, many companies use federated learning as a way to train models while still preserving customer privacy. Federated learning allows for all training to be done on a user's device with no data sent to a centralized server. However, right now federated learning is typically oriented for large scale businesses, not community-driven data sharing.

# My Project

The goal of my project is to develop a system for federated learning that can successfully accommodate users of all backgrounds and technical abilities. Disabled users often have lots of voice or interaction data, yet in typical machine learning systems this is sensitive data that is a liability to collect in a centralized manner. My goal is to be able to leverage federated learning to share this data in a private way while still retaining data autonomy.

I use Pytorch and Flower to implement a federated learning pipeline for the SPEECHCOMMANDS dataset. Individual clients download this python code on their own device in order to train the model and share the weights after training. I use React and Fast API to create a full stack web application to connect to clients. This is intended to be easy to set up for new server administrators that wish to support grassroots disability accessibility organizations.
