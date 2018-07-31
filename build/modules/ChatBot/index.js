'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _axios = require('axios');

var _axios2 = _interopRequireDefault(_axios);

var _v = require('uuid/v1');

var _v2 = _interopRequireDefault(_v);

var _he = require('he');

var _he2 = _interopRequireDefault(_he);

var _parser = require('fast-xml-parser/src/parser');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var ChatBot = function () {
    function ChatBot(botID) {
        _classCallCheck(this, ChatBot);

        this.botID = botID;
    }

    _createClass(ChatBot, [{
        key: 'Think',
        value: function Think(thought) {
            var _this = this;

            return new Promise(function (resolve, reject) {
                var data = '?input=' + encodeURIComponent(thought) + '&' + 'botid=' + _this.botID + '&' + 'uuid=' + (0, _v2.default)();

                _axios2.default.get('https://www.pandorabots.com/pandora/talk-xml' + data).then(function (response) {
                    resolve(_he2.default.decode((0, _parser.parse)(response.data).result.that));
                }).catch(function (err) {
                    reject(null);
                });
            });
        }
    }]);

    return ChatBot;
}();

exports.default = ChatBot;