import Discord from 'discord.js';
import Secrets from './secrets';
const client = new Discord.Client();

client.on('ready', () => {
    console.log('---------------');
    console.log('- Started Bot -');
    console.log('---------------');
});

client.on('message', message => {
    if(message.author.id !== client.user.id){
        if (message.content === 'ping') {
            message.reply('pong');
        }
    }
});

client.login(Secrets.discordkey);