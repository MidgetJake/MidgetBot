import Discord from 'discord.js';
import Config from './config';
const client = new Discord.Client();

client.on('ready', () => {
    console.log('---------------');
    console.log('- Started Bot -');
    console.log('---------------');
});

client.on('message', message => {
    if (message.content === 'ping') {
        message.reply('pong');
    }
});

client.login(Config.discordkey);