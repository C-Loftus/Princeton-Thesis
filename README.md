# Federated Learning for ML-Based Disability Applications

This repository holds the code and written paper for my Princeton senior thesis in Computer Science.

## My Project

The goal of my project is to develop a system for training machine learning models on sensitive medical data without actually needing to have the data directly. Federated learning allows this to be done by training on remote client devices. Thus, the models can be shared by aggregating the weights back to the central server, yet the original data has not been sent off device. This is important, as disabled users often have lots of computer interaction data from applications like voice-dictation, yet in typical machine learning systems this is sensitive data that is a liability to collect in a centralized manner. In addition to the technical aspect of this project, I incorporate my background in HCI and UX design to make web application UIs for machine learning software that are intuitive and accessible. A key challenge in federated learning is communicating with non-technical users who want to retain data autonomy, yet may not understand what is happening on their device during the federated learning process.

I use Pytorch and Flower to implement a federated learning pipeline for the `Speech Commands` dataset. Individual clients download this Python code on their own device in order to train the model and share the model weights after training. I use React and Fast API to create a full stack web application to connect to clients. This is intended to be easy to set up for new server administrators that wish to support grassroots disability accessibility organizations.

## Background and Motivation

For individuals with disabilities, machine learning provides a powerful way to create more useful accessibility software. Voice recognition software is a particularly useful example that has allowed many to interact with their computers hands free.

However many models related to these types of specialty tasks suffer from a lack of data, well trained models, and an ecosystem through which to train them. Machine learning tasks that lack corporate incentives often depend upon grassroots communities to collect data and improve models.

Despite these challenges, there are ways to accomplish these goals and build better machine learning systems for specialty tasks and communities.
Currently, many companies use federated learning as a way to train models while still preserving customer privacy. Federated learning allows for all training to be done on a user's device with no data sent to a centralized server. However, right now federated learning is typically oriented for large scale businesses, not community-driven data sharing. My goal is to help adapt federated learning into a more user-friendly and socially-impactful setting. Many independent software and accessibility communities online require lots of training data for better models, but lack good ways to share it among the group.
