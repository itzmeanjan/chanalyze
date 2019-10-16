# chanalyze
A simple WhatsApp Chat Analyzer ( for both Private &amp; Group chats ), made with :heart:
## nomenclature
**Chat** _+_ **Analyze** _=_ **chanalyze**
## motivation
- I was interested in learning how much time I'm spending on WhatsApp _or_ in which conversation I'm more or less involved/ attached _or_ at which part of day I'm more involved in Chatting etc.
- So I'm writing these scripts for analyzing **WhatsApp** Chat _( both Private & Group )_, which can easily be exported into a _*.txt_ file from WhatsApp Mobile Application.
- That _*.txt_ is parsed, cleaned & objectified, so that it can be analyzed with ease.
- For sake of **Privacy** test data file(s), which were used for plotting following chart(s), are kept private. Also Contact Name(s)/ Number(s) are partially grayed.
## usage
- Clone this repository in a suitable place on your system or just download this ZIP.
```shell
$ git clone https://github.com/itzmeanjan/chanalyze.git
```
- If downloaded ZIP, first unzip it in a suitable place on your system _( may be at `echo $HOME` :wink: )_
- Get into chanalyze _( root directory of this project )_
```shell
$ cd chanalyze
```
- If you list all files/ dirs present under it, you'll find two BASH scripts, named **chanalyze** & **install**
```shell
$ ls # or use `tree`, if you've it
```
- You need to make both of them executable
```shell
$ chmod +x chanalyze install
```
- Make sure you've installed **pip3** via your system package manager
```shell
$ sudo apt-get install python3-pip # for ubuntu
```
```shell
$ sudo dnf install python3-pip # for fedora
```
```shell
$ sudo eopkg install python3-pip # for solus
```
- Time to install dependencies of this project via **pip3**
```shell
$ ./install
```
![installation_instruction_screenshot](installation_instruction.png)
- Follow the instruction, which you find on screen _( red colored )_
- You need to append _path to this project directory_ to your system `PATH` variable
- If you're using BASH, search for a file, named `.bashrc` in `HOME` directory of your system. Can't find ? --- _Then create a file of same name in your HOME directory_
```shell
$ find ~/ -name '.bashrc'
```
- Add following line at the end of that script _( BASH initialization / setup script )_
```shell
export PATH="$PATH:/path/which/was/requested/to/be/added/in/previous/step"
```
- Now Log Out of system & Log In _( or run following command )_
```shell
$ cd
$ source .bashrc
```
- Open terminal & run
```shell
$ chanalyze
```
- If you find any output similar to following one, then you're done with installation & `PATH` setup
```shell
[+]chanalyze v0.1.1 - A simple WhatsApp Chat Analyzer

	$ chanalyze `path-to-exported-chat-file` `path-to-sink-directory`

[+]Author: Anjan Roy<anjanroy@yandex.com>
[+]Source: https://github.com/itzmeanjan/chanalyze ( MIT Licensed )

[#]Success: 0.0000%
```
- Now analyze your exported WhatsApp chat(s), using **chanalyze**
## chanalysis _( Chat Analysis )_
### 1. Participation of Users in Chat
_Following Bar chart depicts how two participants in a Private Chat contributed to that Chat_

![participationInPrivateChatByUser](plots/participationInPrivateChatByUser.png)

_This one depicts how participants in a Group Chat contributed to that Chat_

![participationInGroupChatByUser](plots/participationInGroupChatByUser.png)

_For sake of **Privacy** Participants' Contact Names/ Numbers are partially grayed_

---

### 2. Contribution of Users in Chat by Hour
I splitted a day into 8 equal parts and extracted statistics of activity ( mine & others too ) for each of those timespans, to learn when users are more active. And no doubt result was interesting _( atleast for Group Chat :wink: )_.

- 00:00:00 - 02:59:59
- 03:00:00 - 05:59:59
- 06:00:00 - 08:59:59
- 09:00:00 - 11:59:59
- 12:00:00 - 14:59:59
- 15:00:00 - 17:59:59
- 18:00:00 - 20:59:59
- 21:00:00 - 23:59:59

Following Pie charts show how two participants contributed to a Private chat i.e. how much active were they at which time period.

![activityOfParticipantOne](plots/contributionInPrivateChatOf*******oyByHour.png)

![activityOfParticipantTwo](plots/contributionInPrivateChatOf******************atty_\)ByHour.png)

Following Pie charts showing how participants were contributing in a Group Chat.

![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************SS\)ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************597ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************377ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************965ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************316ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************895ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************494ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************013ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf*************CSS\)ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf**********749ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************858ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf*********SS\)ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************537ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************334ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************422ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************058ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf*************8347ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************456ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************4775ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************181ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************691ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************459ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************093ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************979ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************697ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************183ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************502ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************606ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf*******oyByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************849ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************116ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************CSS\)ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************421ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************848ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************963ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************2_78ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************051ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf*********S\)ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************454ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************877ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************592ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************203ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************425ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************382ByHour.png)
![activityOfParticipantInGroupChat](plots/contributionInGroupChatOf************669ByHour.png)

---

### 3. Detailed Activity Analysis of Chat Participants _( by minute )_
In previous section, I tried to find out how users are spending their time in Chat(s), which we're analyzing, by splitting the whole day into **8** equal parts.

Time for some detailed investigation ... :wink:

Here I'm going to split whole day into 4 equal parts and draw 4 subplots, where I'll try to depict how a user spent each minute of his/ her day _( 1440 minutes in a day )_ over this period of time _( for which we've Chat record )_, in this Chat.

It'll be helpful in understanding, when this user is generally more or less active _( i.e. activity patterns / sleep patterns )_, depending upon what we're observing for this period of time.

No doubt you've already understood, if you had a very long Private Chat with a person or a high traffic group, consider analyzing that Chat file, you'll be happy to learn much more about those participating peoples.

So I applied `util.plotActivityOfUserByMinute()` on a collection of messages from each Participants of Chat _( both Private & Group )_, and result was really interesting.

Check them out.

#### For Private Chat :
1.

![detailedActivityOfParticipantOne](plots/detailedActivityOf*******oyInPrivateChatByMinute.svg)
2.

![detailedActivityOfParticipantTwo](plots/detailedActivityOf******************atty_\)InPrivateChatByMinute.svg)

#### For Group Chat :
1.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************SS\)InGroupChatByMinute.svg)
2.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************597InGroupChatByMinute.svg)
3.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************377InGroupChatByMinute.svg)
4.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************965InGroupChatByMinute.svg)
5.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************316InGroupChatByMinute.svg)
6.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************895InGroupChatByMinute.svg)
7.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************494InGroupChatByMinute.svg)
8.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************013InGroupChatByMinute.svg)
9.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf*************CSS\)InGroupChatByMinute.svg)
10.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf**********749InGroupChatByMinute.svg)
11.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************858InGroupChatByMinute.svg)
12.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf*********SS\)InGroupChatByMinute.svg)
13.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************537InGroupChatByMinute.svg)
14.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************334InGroupChatByMinute.svg)
15.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************422InGroupChatByMinute.svg)
16.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************058InGroupChatByMinute.svg)
17.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf*************8347InGroupChatByMinute.svg)
18.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************456InGroupChatByMinute.svg)
19.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************4775InGroupChatByMinute.svg)
20.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************181InGroupChatByMinute.svg)
21.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************691InGroupChatByMinute.svg)
22.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************459InGroupChatByMinute.svg)
23.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************093InGroupChatByMinute.svg)
24.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************979InGroupChatByMinute.svg)
25.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************697InGroupChatByMinute.svg)
26.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************183InGroupChatByMinute.svg)
27.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************502InGroupChatByMinute.svg)
28.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************606InGroupChatByMinute.svg)
29.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf*******oyInGroupChatByMinute.svg)
30.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************849InGroupChatByMinute.svg)
31.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************116InGroupChatByMinute.svg)
32.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************CSS\)InGroupChatByMinute.svg)
33.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************421InGroupChatByMinute.svg)
34.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************848InGroupChatByMinute.svg)
35.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************963InGroupChatByMinute.svg)
36.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************2_78InGroupChatByMinute.svg)
37.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************051InGroupChatByMinute.svg)
38.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf*********S\)InGroupChatByMinute.svg)
39.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************454InGroupChatByMinute.svg)
40.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************877InGroupChatByMinute.svg)
41.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************592InGroupChatByMinute.svg)
42.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************203InGroupChatByMinute.svg)
43.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************425InGroupChatByMinute.svg)
44.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************382InGroupChatByMinute.svg)
45.

![detailedActivityOfParticipantInGroupChat](plots/detailedActivityOf************669InGroupChatByMinute.svg)

---

### 4. Activeness of Chat _( by Date )_
Here we'll try to understand how participants of a Chat _( Private or Group )_ were active on each day of Year _( for which we've record )_.

If a chat is very long _( spanning over a period of more than one Year )_, then we'll plot whole data for one year i.e. we'll simply accumulate data into 365 _( or 366 )_ days of one year.

For smaller chats it'll be performing as expected.

Let's take some examples ...

_For Private Chat_

![activenessOfPrivateChatByDate](plots/activenessOfPrivateChatByDate.svg)

_For Group Chat_

![activenessOfGroupChatByDate](plots/activenessOfGroupChatByDate.svg)

---

### 5. Conversation Initializing Participant Identification _( using Mean & Median Delay )_ - Reflecting interest of Participant(s) towards Chat
In a Chat _( may be Private or Group )_, there're multiple conversations, which start and end at different point of day _( may be spanning across multiple days )_, within that whole time period, for which we've Chat record.

Now we need to identify those messages _( using index )_, which were at verge of these conversation(s) i.e. end of one conversation & init of next conversation.

Now if we've that stat, we can simply get time elapsed between those messages on verge.

So what we do, calculate time elapsed between all messages for a Chat i.e.

**# of delays to be calculated = ( # of messages in Chat - 1 )**

Now there'll be multiple time delay values _( well they're in Second )_, which will be same, so we'll find unique values.

Using those unique delay values, we'll compute median _( aah !!!, need to sort them ascendingly first )_ & mean delay.

Those messages, which were sent after some time _>=_ mean delay, from previous message sent by some paricipant of this Chat, are extracted, so that we can find out who sent this message _( using index )_.

Now our job is easy, we've determined which participant started how many conversation(s) over lifetime of this Chat, which can give us an idea about which participant is how much keen in participating in that Chat.

We can perform similar analysis using median delay.

Implementation Time _( on test data )_ ...

For a Private Chat

![conversationInitializerStatPrivate](./plots/conversationInitializerStatPrivate.jpg)

For one Group Chat

![conversationInitializerStatGroup](./plots/conversationInitializerStatGroup.jpg)

---

**More to come soon ... :wink:**