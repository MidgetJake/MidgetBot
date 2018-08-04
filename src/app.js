import Discord from 'discord.js';
import { discordKey, chatBotKey } from './secrets';
import AutoMod from './modules/AutoMod';
import ChatBot from './modules/ChatBot';
import ModCommands from './modules/Commands/Mod'
import fs from 'fs';

const client = new Discord.Client();
const chatBot = new ChatBot(chatBotKey);
const modCmd = new ModCommands();
const serverMods = {};
let ready = false;

if (!fs.existsSync('./Config')){
    fs.mkdirSync('./Config');
}

if (!fs.existsSync('./Config/Servers')){
    fs.mkdirSync('./Config/Servers');
}

client.on('ready', () => {
    console.log(' -- Initialising Server Mods -- ');
    // Create mod profiles for each server as auto mod will vary
    for(let server of client.guilds) {
        serverMods[server[1].id] = new AutoMod(server[1].id);
        console.log(server[1].id + ' - Initialised');
    }
    console.log(' -- Completed -- \n');
    console.log(' -- Bot Started -- ');

    ready = true;
});

// Only setup events if the client is connected
client.login(discordKey).then(() => {
    client.on('message', message => {
        if (!ready) return;
        if(message.author.id === client.user.id) return

        // Done asynchronously so it doesn't hold up anything even if the message is to be deleted.
        serverMods[message.guild.id.toString()].Moderate(message).then( toDelete => {
            if(toDelete) message.delete();
        });

        if (message.attachments.size > 0) {
            message.react('👍').then( () => {
                    message.react('👎').catch(() => console.error('Message no longer exists'));
                }
            ).catch(() => console.error('Message no longer exists'));
        }

        if (message.isMentioned(client.user)) {
            let msg = message.cleanContent.replace('@', '');
            let ownNick = client.user.username;
            for (let user of message.mentions.members) {
                if(user[1].id === client.user.id) {
                    ownNick = user[1].nickname ? user[1].nickname : client.user.username;
                }
            }

            console.log(ownNick);
            msg = msg.replace(ownNick + ' ', '');
            console.log(msg);
            chatBot.Think(msg).then(response => {
                message.reply(response);
            });

            return true; // We don't want to execute a command if we are just talking to the bot
        }

        const msg = message.cleanContent.split(' ');
        if (message.member.hasPermission(8)) {
            modCmd.ParseCommand(message, serverMods[message.guild.id.toString()]);
        }

        if(msg[0].toLowerCase() === '!riolu') {
            let variant = '';
            const variants = ['Ah', 'Angery', 'Annoy', 'Cri', 'Dizz', 'Erk', 'Gleam', 'Happ', 'No', 'O', 'Phew', 'Sad', 'Smile', 'SuperHapp', 'Tear', 'Waa'];
            if (msg[1]) {
                variant = msg[1].toLowerCase();
                variant = variant.split('');
                variant[0] = variant[0].toUpperCase();
                variant = variant.join('');
                if(variant === 'Superhapp') {
                    variant = 'SuperHapp';
                }
            } else {
                variant = variants[Math.floor(Math.random()*variants.length)];
            }

            message.channel.send('Riolu is ' + variant ,{
                files: [
                    './Images/Riolu/Riolu' + variant + '.png',
                ],
            })
        }
    });

    // Can't get around the AutoMod by editing a message ;)
    client.on('messageUpdate', (oldMsg, message) => {
        if (!ready) return;
        if (message.author.id === client.user.id) return;

        // Done asynchronously so it doesn't hold up anything even if the message is to be deleted.
        serverMods[message.guild.id.toString()].Moderate(message).then( toDelete => {
            if(toDelete) message.delete();
        });
    })
});