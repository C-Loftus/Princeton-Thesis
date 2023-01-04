---
bibliography: ["./citations.bib"]
---

# Abstract

For individuals with disabilities, machine learning provides a powerful way to create more useful accessibility software. Voice recognition software is a particularly useful example that has allowed many to interact with their computers hands free.

However, many models related to specialty tasks suffer from a lack of data, well trained models, or an ecosystem through which to share them. Machine learning tasks for disability software often lack corporate incentives and thus depend upon community-led, manual solutions that potentially compromise privacy.

In my paper, I describe a novel way to apply Federated Learning for voice-based accessibility software. This federated-learning-based solution allows models to be trained without exposing sensitive voice data to a central server. It also seeks to apply user-centered design principles to reduce the complexity of the federated learning process for end users. My program allows users to use their data generated from existing accessibility software. This data can be used to build the backend for new voice control solutions on mobile devices. Throughout this paper,I describe the technical implementation of this solution and at the end of the paper, discuss the implications of this work for the future of disability software.

# Introduction

In recent years, machine learning has created significant advances in patient care across the medical industry. Sophisticated machine learning applications have emerged for drug discovery, disability accommodations, patient monitoring services, and much more. [@10.1145/3167486.3167551] Advances in reinforcement-learning now allows for vital healthcare applications to be deployed even in novel environments.[@10.1145/3477600] New ways of optimizing and distributing training has allowed for models to trained in restrictive environments [@10.1145/3427796.3433935].

Despite these algorithmic advances, health care data continues to be one of the most challenging data sources for machine learning. It is subject to particularly strict legal regulations and the stakes for user privacy are often much higher than other social data. For instance, in the case of automatic diagnostic software, even if the model performs well, steps must be taken to ensure patient privacy throughout the training process.

Thus, in general in order to do machine learning for health care in a traditional setting, data must be rigorously anonymized and stored in secure computing environments. While this is theoretically acceptable, in practice it often fails. This is usually the case for a few main reasons.

#### Trusting legacy systems

When patients trust hospitals with their data, they are often in turn trusting legacy computing environments. Some may also have understaffed or underfunded IT departments. Due to how complex and old many healthcare IT systems are, it is only a matter of time before something goes wrong. Thus, what often happens is what is known as "normal accident" in sociology [@GVK021392943]. Even a small human error can cause a massive loss of data. Thus, we shouldn't necessarily be surprised when such a breach occurs, given the incentive for hackers and chance for so much to go wrong with just one mistake.

#### Anonymity is often not truly anonymous

Many healthcare facilities will preemptively protect patient privacy by only storing anonymous data. That is, data that is decoupled from identifiable information like names, places of residency, or other public info. Yet despite this, is often difficult to preserve enough useful information while still having anonymity. Studies have shown how anonymizing patient data often falls short with regards to data privacy. Many techniques exist for reconstructing and de-anonymizing such datasets. [@langarizadeh2018effectiveness] While methods have improved, it is in principle impossible to have total privacy when sending data to a centralized system.

#### Patients don't have data autonomy

In the US, patients are not expected to manage their own medical data. Most hospitals and small healthcare providers have their own medical databases and manage patient records with proprietary software. While this is fine from a business perspective, it can be cumbersome for those looking to export and manage their own data. This is especially true for those that want to share data with non-profits or community initiatives. While what exactly would constitute a "good" data autonomy model is still up for debate, the fundamental idea is that medical data should be easy to export, and use for machine learning for the benefit of the public.

Thus in summary, our key challenge for machine learning in healthcare is preserving data privacy and user autonomy as we continue to scale our datasets. In 2020, worldwide medical data collection was estimated to be in the realm of 25 exabytes.[@10.1145/3010089.3010143] We need privacy solutions that can scale to this level of data, while still leveraging new machine learning models.

## Federated Learning

Federated Learning is a machine learning paradigm that seeks to solve these issues. In traditional machine learning, clients are required to send their data to a centralized server and trust it will take the appropriate protections to anonymize it. However,in Federated Learning, all training is done on user devices. Then after training is finished, all that is transferred to the server are the model weights. The data itself stays on user devices.

Essentially what this means is that the server never sees the data, and thus, it is not subject to the same privacy concerns as traditional machine learning. This is a particularly useful paradigm for healthcare, and allows data autonomy to be not only feasible, but also efficient. Users can share data with non-profits and community initiatives without having to worry about the security of their data. This is because the data never leaves the user's device.

Currently as of right now, federated learning has been successful particularly with mobile computing like smartphones or IoT devices. Companies like Google and Apple have been able to leverage federated learning to train models on datasets like keyboard data that would be otherwise sensitive to train on. Datasets like these have allowed for useful predictive typing models that are personalized to the individual user.

## Disability Application

While there are many domains that will benefit from this paradigm of data sharing, one of the most promising and the focus of this paper is voice controlled accessibility software. This software allows users without the use of their hands to control their computer without typing or using the mouse. For this type of software, it often relies upon huge voice datasets. While these models have good performance in general use, users may want to fine-tune them for specific applications that would otherwise not be contained in a general-purpose dataset. For instance, Mozilla's Common Voice \footnote{https://commonvoice.mozilla.org/en} is a great data set for general voice recognition, but may not be enough to support user with a particular accent, speech impediment, job specific technical vocabulary.

Disability applications often are supported through grassroots communities with economies of sharing.

## HCI and Design Work

For those without full use of their hands, many types of software interaction can be difficult or annoying to navigate with voice controlled software. For instance, not all programs expose an accessibility tree or have good keyboard shortcuts. This is even the case for some popular applications like Adobe Acrobat\footnote{https://acrobat.uservoice.com/forums/590923-acrobat-for-windows-and-mac/suggestions/39448096-acrobat-reader-for-mac-does-not-expose-an-accessib} As result, a user may be forced to use the mouse or an eye tracker which is a less than ideal solution. As a result, I wanted to build all my user interfaces with a web ui. Internet browsers have much more accessibility tooling built in and are generally more accessible. For instance, tools like Rango\footnote{https://github.com/david-tejada/rango/} and Vimium \footnote{https://vimium.github.io/} allow the user to navigate the web with just voice, or just the keyboard, respectively. Thus by creating my user interface for the web, I can take advantage of these already existing tools for better accessibility.

In addition to the accessibility aspects of our design for federated learning paradigms, we will also need to ensure ease-of-use. Most users are not accustomed to dealing with data in a decentralized way. For instance, recent studies have been done regarding the behavior of users in other decentralized networks such as Mastodon. Mastodon is an alternative social media platform that anyone can self-host and federate with other instances. This allows for decentralized data sharing and moderation. However, even though the software is designed for decentralization, users often congregate towards centralized servers. [@10.1145/3355369.3355572] After Elon Musk bought twitter and caused many users to seek alternative platforms, Mastodon saw a huge influx of new users. However, many of these users were confused regarding which instance to use, and how their data was being retained. \footnote{https://www.newyorker.com/culture/infinite-scroll/what-fleeing-twitter-users-will-and-wont-find-on-mastodon}

Thus even though Mastodon is a very different application, it is a good example of how users are not accustomed to dealing with decentralized data. When implementing we need not only new technical solutions, but also new design strategies. After all, our goal is to share data in a way that is both efficient and democratic.

As a result, we need to create new UX design strategies that allow users of all backgrounds to participate in this new model of data sharing. Our federated learning applications need to be accessible for all abilities, easily deployed for grassroots communities, and intuitively communicate the goals of data autonomy.
We will need to overcome these challenges for Federated learning to go beyond just industry adoption and eventually see it come to fruition in non-profits, online groups, and community organizations.

# Background

Before discussing my work, it is useful to give an overview of the existing field of voice-controlled disability software. These software tools helped to inform my design decisions. I specifically wanted to create a federated learning solution that could help to address some of the existing issues in this software ecosystem.

## Disability Software

Within voice-controlled disability there are a few main categories. First

### Application-Specific Accessibility Software

Application-Specific solutions are often built specifically for one platform like a web browser or

### General Purpose Accessibility Software

#### Dragon

Dragon is an

#### Talon

The next main option for Linux is Talon. \footnote{https://talonvoice.com/} Talon is a general purpose voice control engine for which individuals can write scripts to customize its behavior. Upon downloading it, Talon provides no desktop control functionality and is only a voice parser. However, there is a large community repository of Talon scripts called Knausj Talon. \footnote{https://github.com/knausj85/knausj\_talon} These can be imported and customized as desired.

Talon has a large user community with specific user scripts for doing things like coding by voice and navigating the web browser. These solutions are often more customizable and efficient given the fact that their designers are often also part of the Talon community as users.
One of the benefits of talon is that you can enable the option 'Save Recordings.' This will create an annotated dataset of user recordings for every command. Thus it is very easy to generate a personalized dataset when using talon.

While both of these voice control solutions work well for many, each has a downside. Both Dragon-Naturally-Speaking and Talon are closed source. This may be a downside for privacy conscious individuals, even though many extensions are nonetheless open source and community developed. Dragon-Naturally-Speaking is also not free, and the cost may be a significant impediment to many users. Finally, Talon Voice does not support ARM-based CPUs and lacks a way of automatically sharing data in its ecosystem. Contributing data to use for future model training involves a manual process of sending recorded data to the developer.\footnote{https://noise.talonvoice.com/}

## Linux Mobile Devices

As we saw when describing the current landscape of hands-free accessibility software, a significant amount of the issues come from the fact that parts of the ecosystem are closed source, and do not support ARM-based CPUs. As a result, for my research, I was specifically interested to targeting Linux smartphones.Linux smartphones are unique in the fact that they are often made specifically for the purpose of user privacy. As such, there is significant overlap in the user base with those who are looking to gain data autonomy and participate in grassroots social computing initiatives. In addition, they can typically run any desktop Linux software, so long as it is compiled for an ARM-based CPU and has it appropriate UI for a mobile device, so my federated learning solution could work on both desktop and mobile Linux devices. While Linux smartphones are a very small market currently, there is a passionate community around the devices and I wanted to not only solve an existing problem in the voice controlled accessibility ecosystem, but also tie in my work with anticipating future issues that wall come about due to a lack of accessibility support on new ARM mobile devices.

I believe that I have already helped to progress this challenge through my previous research \footnote{https://github.com/C-Loftus/Starling}. This program I wrote is a proof of concept voice control solution on Linux. In this paper, my solution for sharing data and training models with federated learning can help provide new solutions for the machine learning backend.

# Approach

As stated, my project goal was to create a federated learning system for voice controlled disability software. I wanted to create a proof of concept to show how federated learning could be applied to the disability software space and in doing so investigate new way of UI and UX design.

I split up the technical implementation of my project into five main parts.

- Machine Learning Architecture and Algorithms
- Webserver Backend
- Webserver Frontend
- Linux GUI Client
- Packaging and Distribution

The goal of this architecture is to make it so a server administrator ( the person that will eventually get the final trained model ) can easily start a federated learning training process without needing to have any knowledge of coding. Additionally, since the federated learning process can be controlled through a web API, it makes it easier to create new clients for various different devices.

## Federated Learning Implementation

The first thing I had to do was make a decision regarding which federated learning library to use. Currently there are a few main options. There are options like `fedjax` [@fedjax2021], Pysyft[@DBLP:journals/corr/abs-1811-04017], and flwr[@beutel2020flower]. While a comprehensive comparison of all options would be beyond the scope of this paper, I chose to go with flwr. This library allows you to apply federation strategies to existing models in popular frameworks like PyTorch and Tensorflow.

With this

### Federated Learning Strategies

In federated learning, the flower server needs to make a decision regarding how to aggregate the weights from the clients. Different aggregation strategies can be used to provide better properties for specialty tasks, or make up for technical limitations in the client system (power, network connection, processing power, etc).

When deciding to use a strategy, it is important to consider the following properties: [@https://doi.org/10.48550/arxiv.1602.05629]

- Non-IID: Any particular user's local data set will not necessarily be representative of the population distribution
- Unbalanced: The number of samples per user is not necessarily the same
- Massively Distributed: The number of users is very large
- Heterogeneous: The users' devices are different (e.g. different hardware, different operating systems, different software versions, etc.)
- Limited communication: The users' devices are not necessarily connected to the internet all the time, or have limited bandwidth

The most well known federated learning algorithm is FedAvg, this appeared in the same paper where the term "Federated Learning" was coined.[@https://doi.org/10.48550/arxiv.1602.05629] This algorithm works by randomly sampling from the users and averaging their update weights. However, this algorithm has some limitations. If we have particularly unbalanced data the algorithm may not synthesize between clients well. For this reason, the Federated Average with momentum algorithm was proposed. This strategy helps to eliminate the unbalanced data problem by using a momentum term to help the algorithm converge to a better solution. [@https://doi.org/10.48550/arxiv.1909.06335] This algorithm uses a gradient history to dampen oscillations during training. As a result, this algorithm also has the favorable property of being able to generally train more quickly than FedAvg.

While approaching training from perspective of data heterogeneity is one way to approach the tradeoff, we can also use strategies that try to limit network communication between the client and the server. One such strategy is known as QFedAvg. This strategy uses a quantization technique to reduce the amount of data that needs to be sent between the client and the server. [@https://doi.org/10.48550/arxiv.1602.05629] This strategy is particularly useful when the clients have limited network connectivity. If network speed is not the issue but rather interruptions in the connection, we can use FaultTolerantFedAvg.

Finally, we can also adapt the adaptive optimization methods of traditionally non-federated algorithms. We can use federated versions of adaptive optimizers, including Adagrad, Adam, and Yogi to make our systems easier to tune and gain more favorable convergence behavior. [@https://doi.org/10.48550/arxiv.2003.00295]

## HCI and UX

# Implementation

## Webserver Frontend

## Webserver Backend

For my backend I used FastAPI. FastAPI allows for the creation of web apis in Python.

## Client

## Packaging and Distribution

One of the advantages of building for Linux devices is that there are already multiple options for packaging and software distribution. I had a few main goals when distributing my software. While machine learning dependencies are often very large,

# Evaluation

##

# Future Work

## User Studies

In the future, it could be useful to extend this technical research by seeking out users with disabilities to participate in a user study. These users would need to have a large amount of voice data.

The one limitation on this would be that such users would need to have Linux smartphones. This is a very specialized demographic and thus would not be representative of the smartphone-owning population as a whole.

##

# Conclusion

# Acknowledgements

I would like to thank my advisor, Professor Kyle Jamieson at Princeton University for his advice and insight throughout the research process.
