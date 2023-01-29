---
bibliography: ["./citations.bib"]
---

# Abstract

For individuals with disabilities, machine learning provides a powerful way to create more useful accessibility software. Voice recognition software is a particularly useful example that has allowed many to interact with their computers hands free.

However, many models related to specialty tasks suffer from a lack of data, well trained models, or an ecosystem through which to share them. Machine learning tasks for disability software often lack corporate incentives and thus depend upon community-led, manual solutions that potentially compromise privacy.

In my paper, I describe a novel way to apply Federated Learning for voice-based accessibility software. This solution using federated learning allows models to be trained without exposing sensitive voice data to a central server. It applies user-centered design principles to reduce the complexity of the federated learning process for end users. My program allows users to use their data generated from existing accessibility software. This data can be used to build the backend for new voice control solutions on mobile devices. Throughout this paper,I describe the technical implementation of this solution and at the end of the paper, discuss the implications of this work for the future of disability software.

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

Essentially what this means is that the server never sees the data, and thus, it is not subject to the same privacy concerns as traditional machine learning. This is a particularly useful paradigm for healthcare. It allows data autonomy without needing to compromise on the use of large-scale datasets. Users can share data with non-profits and community initiatives without having to worry about the security of their data. This is because the data never leaves the user's device.

Currently within industry, federated learning has been successful particularly with mobile computing like smartphones or IoT devices. Companies like Google and Apple have been able to leverage federated learning to train models on datasets like keyboard data that would be otherwise sensitive to train on. Datasets like these have allowed for useful predictive typing models that are personalized to the individual user. However, as of right now, federated learning is still an emerging research area and usually is abstracted away from end-users.

## Disability Application

While there are many domains that will benefit from this paradigm of data sharing, one of the most promising and the focus of this paper is voice controlled accessibility software. This software allows users without the use of their hands to control their computer without typing or using the mouse. For this type of software, it often relies upon huge voice datasets. While these models have good performance in general use, users may want to fine-tune them for specific applications that would otherwise not be contained in a general-purpose dataset. For instance, Mozilla's Common Voice \footnote{https://commonvoice.mozilla.org/en} is a great data set for general voice recognition, but may not be enough to support user with a particular accent, speech impediment, job specific technical vocabulary.

Disability applications often are supported through grassroots communities with economies of sharing. Within such social arrangements, there is often a compromise regarding either efficiency or privacy.

## HCI and Design Work

For those without full use of their hands, many types of software interaction can be difficult or annoying to navigate with voice controlled software. For instance, not all programs expose an accessibility tree or have good keyboard shortcuts. This is even the case for some popular applications like Adobe Acrobat\footnote{https://acrobat.uservoice.com/forums/590923-acrobat-for-windows-and-mac/suggestions/39448096-acrobat-reader-for-mac-does-not-expose-an-accessib} As result, a user may be forced to use the mouse or an eye tracker which is a less than ideal solution. As a result, I wanted to build all my user interfaces with a web ui. Internet browsers have much more accessibility tooling built in and are generally more accessible. For instance, tools like Rango\footnote{https://github.com/david-tejada/rango/} and Vimium \footnote{https://vimium.github.io/} allow the user to navigate the web with just voice, or just the keyboard, respectively. Thus by creating my user interface for the web, I can take advantage of these already existing tools for better accessibility.

In addition to the accessibility aspects of our design for federated learning paradigms, we will also need to ensure ease-of-use. Most users are not accustomed to dealing with data in a decentralized way. For instance, recent studies have been done regarding the behavior of users in other decentralized networks such as Mastodon. Mastodon is an alternative social media platform that anyone can self-host and federate with other instances. This allows for decentralized data sharing and moderation. However, even though the software is designed for decentralization, users often congregate towards centralized servers. [@10.1145/3355369.3355572] After Elon Musk bought twitter and caused many users to seek alternative platforms, Mastodon saw a huge influx of new users. However, many of these users were confused regarding which instance to use, and how their data was being retained. \footnote{https://www.newyorker.com/culture/infinite-scroll/what-fleeing-twitter-users-will-and-wont-find-on-mastodon}

Thus even though Mastodon is a very different application, it is a good example of how users are not accustomed to dealing with decentralized data. When implementing we need not only new technical solutions, but also new design strategies. After all, our goal is to share data in a way that is both efficient and democratic.

As a result, we need to create new UX design strategies that allow users of all backgrounds to participate in this new model of data sharing. Our federated learning applications need to be accessible for all abilities, easily deployed for grassroots communities, and intuitively communicate the goals of data autonomy.
We will need to overcome these challenges for Federated learning to go beyond just industry adoption and eventually see it come to fruition in non-profits, online groups, and community organizations.

# Background

Before discussing my work, it is useful to give an overview of the existing field of voice-controlled disability software and Federated Learning frameworks. These software tools helped to inform my design decisions. I specifically wanted to create a federated learning solution that could help to address some of the existing issues in this software ecosystem.

## Disability Software

Within voice-controlled disability software, many of the design philosophies behind different programs can be grouped into two main categories.

### Application-Specific Accessibility Software

Application-Specific solutions are the first main category of voice based accessibility tools. These are often the solutions people are most familiar with and are built specifically for one platform like a web browser or smartphone app. In this model, it is up to each program to implement its own accessibility tools. One example is the extension LipSurf. \footnote{https://www.lipsurf.com/} This extension allows users within Chrome to control their browser with just voice. It takes advantage of browser specific accessibility APIs and thus does not provide any control of other desktop applications. While this is a downside for some, it can also be a benefit for others. LipSurf is very easy to install and use, and it is very clear where the goals of the project begin and end. For other desktop applications, it is beyond the scope of this software and as a result the developer and community can focus more on just web tools .

### General Purpose Accessibility Software

General purpose accessibility software is the other philosophy behind the design of voice based accessibility software. Under this design philosophy, the user runs one large voice control program that can interact with the entire desktop, not just one application. While it has much more potential for general use, it is also harder to learn for new users. It is also a greater development burden you need to design around the entire desktop, and not just one application like the browser that is cross platform.

#### Dragon

The first and perhaps most well known example of this sort of accessibility software is Dragon.Dragon is a proprietary voice control program that has been around since the 1990s (and even earlier with early builds). It is heavily marketed towards enterprise and business customers and tends to be focused on providing functionality for industries like healthcare, legal services, law enforcement, and others that require lots of writing. While Dragon has innovated on many fronts over the years, it currently only supports Windows and given its proprietary nature, can be hard to extend and customize. As a result, many users of Dragon (especially those looking to perform specialized tasks like computer programming) have begun to adopt other tools.

#### Talon

One such other tool is Talon. \footnote{https://talonvoice.com/} Talon is a general purpose voice control engine for which individuals can write scripts to customize its behavior. Upon downloading it, Talon provides no desktop control functionality and is only a voice parser. However, there is a large community repository of Talon scripts called Knausj Talon. \footnote{https://github.com/knausj85/knausj\_talon} These can be imported and customized as desired.

Talon has a large user community with specific user scripts for doing nearly anything you would want on your desktop, anything from coding by voice to playing video games. These solutions are often more customizable and efficient given the fact that their designers are often also part of the Talon community as users.
One of the benefits of Talon is that you can enable the option 'Save Recordings.' This will create an annotated dataset of user recordings for every command. Thus it is very easy to generate a personalized dataset when using talon.

While both of these voice control solutions work well for many, each has a downside. Both Dragon-Naturally-Speaking and Talon (here referring to the voice parser,not the user scripts) are closed source. This may be a downside for privacy conscious individuals, even though many extensions are nonetheless open source and community developed. Dragon-Naturally-Speaking is also not free, and the cost may be a significant impediment to many users. Finally, Talon Voice and Dragon do not support mobile devices and lack a way of automatically sharing data in its ecosystem. In Talon, contributing data to use for future model training involves a manual process of sending recorded data to the developer.\footnote{https://noise.talonvoice.com/}

As a result there arenumerous research opportunities in voice controlled accessibility software. Everything from developing new open source voice parsers for mobile devices, to new ways of sharing community customizations and data, all have great potential to dramatically help not only current users, but also future users on devices and architectures that have yet to be commonly adopted.

## Linux Mobile Devices

As we saw when describing the current landscape of hands-free accessibility software, a significant amount of the issues come from the fact that parts of the ecosystem are closed source and do not support mobile devices. Additionally, even though Talon can automatically produce a personalized and labeled dataset, there are not any devices or ecosystems which seek to take advantage of this.

As a result, for my research, I was specifically interested in targeting Linux smartphones.Linux smartphones are unique in the fact that they are a mobile device, but can also typically run any desktop Linux software, so long as a ARM-build exists. This greatly reduces the friction for users that seek to migrate between desktop and mobile devices. An addition to these technical benefits, the demographic of these new open source mobile initiatives are looking to gain data autonomy and participate in grassroots social computing initiatives. This makes them more likely to participate in federated learning technology (especially given the privacy preserving nature of the tech).

By building for a new ecosystem like Linux mobile devices,I wanted to not only solve an existing problem in the voice controlled accessibility ecosystem, but also tie in my work with anticipating future issues that wall come about due to a lack of accessibility support on new ARM mobile devices.

Finally, as previously stated, Linux mobile devices can more easily run existing Linux software than alternatives like Android or IOS. This will allow me to adapt my previous research developing an open source voice parser for linux \footnote{https://github.com/C-Loftus/Starling}. This will allow me to lay the groundwork not only for new community based federated learning solutions,but also the parsers and accessibility software that will consume these models.

# Approach

As previously stated, my project goal was to create a federated learning system for voice controlled disability software. I wanted to create a full ecosystem to show how federated learning could be applied to the disability software space. Additionally, in doing so I also wanted to investigate new design principles and the emerging platform of Linux smartphones.

I split up the technical implementation of my project into five main parts.

- Machine Learning Architecture and Algorithms
- Webserver Backend
- Webserver Frontend
- GUI Client for participating in federated learning and converting talon data
- Packaging and Distribution

A visual description of each part can be seen in the diagram below.

$$
 \forall{talon\_data}_1^{|talon\_data| := N}
$$

```{.mermaid format=svg .mermaid loc=assets}
erDiagram
    TALON_DATA_1 ||--|| TRAINING_CLIENT_1: converts
    TALON_DATA_1 {
        origin client_1_desktop
    }
    TALON_DATA_2 ||--|| TRAINING_CLIENT_2: converts
    TALON_DATA_2 {
        origin client_2_desktop
    }
    TALON_DATA_N ||--|| TRAINING_CLIENT_N: converts
    TALON_DATA_N {
        origin client_N_desktop
    }
    TRAINING_CLIENT_1 ||--|| FLOWER_SERVER : federates_with
    TRAINING_CLIENT_1   {
        platform desktop
    }
    TRAINING_CLIENT_2 ||--|| FLOWER_SERVER: federates_with
    TRAINING_CLIENT_2 {
        platform desktop
    }
    TRAINING_CLIENT_N ||--|| FLOWER_SERVER: federates_with
    TRAINING_CLIENT_N {
        platform desktop
    }
    FLOWER_SERVER ||--|| SPEECH_COMMANDS_MODEL: creates
    SPEECH_COMMANDS_MODEL  ||--|| LINUX_ACCESSIBILITY_CLIENT : powers
    LINUX_ACCESSIBILITY_CLIENT {
        platform mobile
    }

    REACT_FRONTEND ||--|| FAST_API_ENDPOINT: interacts_with
    FAST_API_ENDPOINT ||--|| FLOWER_SERVER: controls

```

The goal of this architecture is to make it so both a server administrator ( the person that will eventually get the final trained model ) and existing Talon users can easily start a federated learning training process . They should be able to do this without needing to have any knowledge of coding. In addition to the user experience goals, the technical design is loosely coupled and is thus easier to build upon in the future. For instance, since the federated learning process can be controlled through a web API,users can develop their own clients or integrate their own ways of parsing Talon user data. My architecture provides a useful default client but is by no means required.

# Implementation

With this background in mind, I will now proceed to discuss the implementation of my software and the various challenges I overcame. As stated previously, I sought to create a minimum viable product for implementing a full federated learning ecosystem. Each part of this ecosystem has a decoupled architecture which will allow new innovations to add features to specific parts of the system without needing to change others.

## Federated Learning Implementation

The first and most essential part of my project was implementing the technical aspects of federated learning. These new machine learning aggregation strategies effected not only my decisions regarding modeling, but also principles of user experience design.

The first thing I had to do was make a decision regarding which federated learning library to use. Currently there are a few main options. There are options like `fedjax` [@fedjax2021], Pysyft[@DBLP:journals/corr/abs-1811-04017], and flwr[@beutel2020flower]. While a comprehensive comparison of all options would be beyond the scope of this paper, I chose to go with flwr. This library allows you to apply federation strategies to existing models in popular frameworks like PyTorch and Tensorflow. flwr thus allows you to focus more on modeling and abstracts away aspects of federated learning like networking and error handling that are less relevant to this project.

With this decision in mind, I then had to choose a model upon which I would implement federated learning. I had a few main goals for this model given the fact that it would be used on lightweight Linux mobile devices.

- It must be a model capable of processing human speech in English
- It should be feasible to train without a GPU
- It does not need to have a large vocabulary size
- The model itself should be small and easy to run on a mobile device
- The model should be focused more on commands rather than dictating sentences

As a result, I decided to use the M5 model architecture.[@https://doi.org/10.48550/arxiv.1610.00087]
This architecture is designed for making inferences on raw wave form data with minimal processing. Compared to larger conformer or wav2letter models, M5 requires less code and disk space to run. As a result it also makes it easier to deploy to mobile devices that may have limited disk space or nontraditional package management.

With regards the technical aspects of this model, it takes advantage of advances in convolutional neural networks while still making it relatively resource efficient to train and process inferences. For instance the paper says how "By applying batch normalization, residual learning, and a careful design of down-sampling layers, we overcome the difficulties in training very deep models while keeping the computation cost low."In the paper they use the UrbanSound8k dataset which contains 10 environmental sounds that the model is trained to distinguish. While this dataset is different from the speech commands used for voice controlled accessibility software, it is a good baseline metric for determining the models performance on classifying discrete noises in a noisy environment: also an essential property for accessibility software.

### Client Implementation

After implementing the model in Pytorch code, it then became time to integrate it with flwr and federated learning. In flwr, it is up to the user to implement 4 main functions on the model.

```
class FlowerClient(fl.client.NumPyClient):

    def get_parameters(self, config):

    def set_parameters(self, parameters):

    def fit(self, parameters, config):

    def evaluate(self, parameters, config):
```

As previously stated, in federated learning, all training happens on device and then the model parameters are exported to a central server where they are aggregated in some way, so as to preserve privacy but also reap the benefits from a large base of training data. As a result it is up to the client to define how they will fit the model, and export parameters to the central server. This implementation can be found in [client/training.py](client/training.py). With regards to the details of the implementation, I use negative log likelihood as my loss function and batch processing to reduce the load of system resources. I use the former given the fact I am doing multi class classification over audio data and want a probability distribution that sums to one. With regards to batch processing, I wanted to incorporate accessibility in an unconventional way. While we often think about accessibility as a physical property, it can also be a technical one back can limit users with lower end hardware from participating in software communities. Simpler models and batch processing make it so we can engage with the largest possible audience. While I do not assume people will be training their models on Linux mobile devices, my hope was that strategies like these can open up such a possibility in the future.

### Training Data
 Now that we have defined the overview of my model architecture.

## Flwr Central Webserver

The first For my backend I used FastAPI. FastAPI allows for the creation of web apis in Python. The goal of this the server is to launch and manage the central Federated Learning server.

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

## Webserver Frontend

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
