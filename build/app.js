'use strict';

var _discord = require('discord.js');

var _discord2 = _interopRequireDefault(_discord);

var _secrets = require('./secrets');

var _AutoMod = require('./modules/AutoMod');

var _AutoMod2 = _interopRequireDefault(_AutoMod);

var _ChatBot = require('./modules/ChatBot');

var _ChatBot2 = _interopRequireDefault(_ChatBot);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var client = new _discord2.default.Client();
var chatBot = new _ChatBot2.default(_secrets.chatBotKey);
var serverMods = {};
var ready = false;

client.on('ready', function () {
    console.log(' -- Initialising Server Mods -- ');
    // Create mod profiles for each server as auto mod will vary
    var _iteratorNormalCompletion = true;
    var _didIteratorError = false;
    var _iteratorError = undefined;

    try {
        for (var _iterator = client.guilds[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
            var server = _step.value;

            serverMods[server[1].id] = new _AutoMod2.default(server[1].id);
            console.log(server[1].id + ' - Initialised');
        }
    } catch (err) {
        _didIteratorError = true;
        _iteratorError = err;
    } finally {
        try {
            if (!_iteratorNormalCompletion && _iterator.return) {
                _iterator.return();
            }
        } finally {
            if (_didIteratorError) {
                throw _iteratorError;
            }
        }
    }

    console.log(' -- Completed -- \n');
    console.log(' -- Bot Started -- ');

    ready = true;
});

// Only setup events if the client is connected
client.login(_secrets.discordKey).then(function () {
    client.on('message', function (message) {
        if (!ready) return;
        if (message.author.id === client.user.id) return;

        // Done asynchronously so it doesn't hold up anything even if the message is to be deleted.
        serverMods[message.guild.id.toString()].Moderate(message).then(function (toDelete) {
            if (toDelete) message.delete();
        });

        if (message.attachments.size > 0) {
            message.react('👍').then(function () {
                message.react('👎').catch(function () {
                    return console.error('Message no longer exists');
                });
            }).catch(function () {
                return console.error('Message no longer exists');
            });
        }

        if (message.isMentioned(client.user)) {
            var msg = message.cleanContent.replace('@', '');
            var ownNick = client.user.username;
            var _iteratorNormalCompletion2 = true;
            var _didIteratorError2 = false;
            var _iteratorError2 = undefined;

            try {
                for (var _iterator2 = message.mentions.members[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                    var user = _step2.value;

                    if (user[1].id === client.user.id) {
                        ownNick = user[1].nickname;
                    }
                }
            } catch (err) {
                _didIteratorError2 = true;
                _iteratorError2 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion2 && _iterator2.return) {
                        _iterator2.return();
                    }
                } finally {
                    if (_didIteratorError2) {
                        throw _iteratorError2;
                    }
                }
            }

            msg = msg.replace(ownNick + ' ', '');
            chatBot.Think(msg).then(function (response) {
                message.reply(response);
            });

            return true; // We don't want to execute a command if we are just talking to the bot
        }
    });
});