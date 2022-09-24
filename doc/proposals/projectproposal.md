---
title: "Project Proposal"
author: Colton Loftus
geometry: margin=4cm
output: pdf_document
---

For individuals with disabilities, machine learning provides a powerful way to create more useful accessibility software. Voice recognition software is a particularly useful example that has allowed many to interact with their computers hands free.

However many models related to specialty tasks suffer from a lack of data, well trained models, and an ecosystem through which to train them. Machine learning tasks such as disability software that lack corporate incentives often depend upon grassroots communities to collect data and improve models.

Despite these challenges, there are ways to accomplish these goals and build better machine learning systems for specialty tasks and communities.
Currently, many companies use federated learning as a way to train models while still preserving customer privacy. Federated learning allows for all training to be done on a user's device with no data sent to a centralized server. For instance, Google and Apple use federated learning as a way to locally improve voice assistant and keyboard prediction without having the user send data off device. However, federated learning is typically oriented for this sort of large-scale business problem, not community-driven data sharing.

Implicitly through the use of disability software, individuals can quickly obtain valuable datasets for training future models. For instance, users with voice controlled software can generate and validate labeled audio files while dictating. Yet in order for this data to be used for others, there needs to be better options for trustfully sharing and distributing models across user communities. Disabled users and any other populations that will be crowd-sharing data should trust that they will continue to have autonomy and privacy when doing so.

In my project I will be creating a server and client for creating a community driven federated learning system. This infrastructure will be

- Decentralized
- Private
- Generalizable across machine learning tasks
- Easy to use and self host

While I'm specifically interested in the application of this project on ML-related voice-controlled disability software these tools will generalize to any special ML tasks.
