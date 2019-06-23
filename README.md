# nickname_bot
A discord bot that randomly changes your nickname from a user defined pool of nicknames each time you send a message

Github link: *[here](https://github.com/RyanTheNerd/nickname_bot)*

Add link: *[here](https://discordapp.com/oauth2/authorize?client_id=504395357472686099&permissions=201554944&scope=bot)*

## Commands:

### Nickname commands:
Nicknames will automatically be archived within a week of being added. To add a name back, use the `/addname` command.

#### General format:
With all name commands you can either pass a mention and then a name, or just a name. For example, `/addname [mention] [name]` adds `[name]` to `[mention]`'s pool. If you'd like to access your own pool, only pass a name.

#### Command listing:
* `/addname [mention] [name]` - Adds `[name]` to `[mention]`'s pool
* `/rmname [mention] [name]` - Removes `[name]` from `[mention]`'s pool
* `/lsname [mention]` - Lists all current names in `[mention]`'s pool
* `/lsarchived [mention]` - Lists all archived names in `[mention]`'s pool
* `/lsall [mention]` - Lists all names, previous and current in `[mention]`'s pool


### Other commands:
* `/clr` or `/cls` - Clears all bot output from up to 5 days before
* `/alexjones [top], [bottom]` - Create a meme with Alex Jones
* `/hackerman [top], [bottom]` - Create a meme with Hackerman
* `/quote` - Generate a random quote
* `/deepfry [url]` - Deepfry an image located at `[url]`

### Easter eggs:
* `{fighter} VS {figher}: FIGHT!` - Simulate a fight between two characters
* `Either {this} or {that}`       - Pick one of the statements to be true

The rest are actual easter eggs so those are for you to find out
