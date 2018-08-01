# MidgetBot
Installation
-----
1. Clone the repository
2. Run `npm install` in root directory
3. Create a `secrects.js` with contents:
    ```js
        export const discordKey = 'Discord Bot API key';
        export const chatBotKey = 'Pandorabots API key';
     ```
4. Run `npm run build` to build the source
5. Run `npm run quickstart` to start once it's built

To merge steps 4 & 5 together run `npm run start` This will build then start the bot in a single command

Current Features
-----
- Upvote/Downvote on messages with attachments
- Automod with custom regex rules

Planned Features
-----
- Points system
- Quotes system
- Awarding roles for things (points, time in server, etc...)
- Magic 8 ball
- Announcing streams
- Announcing videos
- Welcome/Leaving messages
- Basic fun commands
- Points games
- Anything else I can think of

