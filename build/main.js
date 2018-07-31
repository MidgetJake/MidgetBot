'use strict';

var _discord = require('discord.js');

var _discord2 = _interopRequireDefault(_discord);

var _secrets = require('./secrets');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var client = new _discord2.default.Client();

client.on('ready', function () {
    console.log('---------------');
    console.log('- Started Bot -');
    console.log('---------------');
});

client.login(_secrets.discordKey).then(function (resp) {
    client.on('message', function (message) {
        if (message.author.id !== client.user.id) {
            if (message.content === 'ping') {
                message.reply('pong');
            }
        }
    });
});