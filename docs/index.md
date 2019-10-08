# chanalyze
A WhatsApp Chat analyzer, for both Private & Group Chats, written with :heart:

**I'll keep updating this page, cause I'm still working on it**

## nomenclature
*Chat* + *Analyze* = **Chanalyze**

## motivation
- Won't it be really great if you could learn, how much time you're spending on a certain WhatsApp Chat or what's your activity like etc.
- Yeah that's what drove me to write these simple *Python* scripts, so that I can get a deeper insight into my chat behaviour _( also of others )_.
- Well this enabled me to learn more about, when a certain participant is generally more active i.e. **helps you to have a shallow understanding of their sleep patterns**.
- And a lot more ... :wink:

## data source
- Open WhatsApp on your mobile
- Click on a Chat
- Click on top right Options
- From there select **More**
- And **Export Chat**
- Consider uploading to Drive & download _*.txt_ later

## using
- I wrote it while using *Python 3.7.3*, so consider using it or above
- Otherwise *Python* type annotation may cause some unexpected issues
- Now clone _[this](https://github.com/itzmeanjan/chanalyze)_ repository
- Make sure you've _matplotlib 3.x.x_ installed
- I'm expecting you've already exported chat from _WhatsApp_ & downloaded so
- Create a directory named, `data` under root of this project
- Put _*.txt_ into this directory

### Participation of Users in Chat
Invoke `util.plotContributionInChatByUser()`, to generate a Bar chart, depicting how participants contributed to a Chat i.e. by percentage

### Active Time Period _( in this Chat )_ of Participants
I splitted a whole day into 8 equal sized parts, as follows
- 00:00:00 - 02:59:59
- 03:00:00 - 05:59:59
- 06:00:00 - 08:59:59
- 09:00:00 - 11:59:59
- 12:00:00 - 14:59:59
- 15:00:00 - 17:59:59
- 18:00:00 - 20:59:59
- 21:00:00 - 23:59:59

To learn more about when a certain participant is more active i.e. in which time period, giving you a understanding of someone's sleep pattern.

No doubt it's more effective for Group Chats.

Consider invoking `util.plotContributionOfUserByHour()`, to generate a Pie chat of activity of selected user _( from Chat object )_

**More to come soon ...** :wink:

## license
It's MIT licensed :blush:
## support
Consider showing some :heart: by putting :star: on this _[repo](https://github.com/itzmeanjan/chanalyze)_

:copyright: Anjan Roy
