'use strict';

Object.defineProperty(exports, "__esModule", {
    value: true
});

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _fs = require('fs');

var _fs2 = _interopRequireDefault(_fs);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var AutoMod = function () {
    function AutoMod(serverID) {
        var _this = this;

        _classCallCheck(this, AutoMod);

        this.server = serverID;

        _fs2.default.readFile('./Config/Servers/' + serverID + '.json', 'utf8', function (err, data) {
            if (err) {
                _fs2.default.writeFileSync('./Config/Servers/' + serverID + '.json', JSON.stringify({ rules: [] }), 'utf8', function (err) {
                    console.error('Error creating file:', err);
                });
                _this.config = { rules: [] };
            } else {
                _this.config = JSON.parse(data);
            }
        });
    }

    _createClass(AutoMod, [{
        key: 'Moderate',
        value: function Moderate(message) {
            var _this2 = this;

            return new Promise(function (resolve, reject) {
                var toDelete = void 0;
                var _iteratorNormalCompletion = true;
                var _didIteratorError = false;
                var _iteratorError = undefined;

                try {
                    for (var _iterator = _this2.config.rules[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                        var rule = _step.value;

                        toDelete = new RegExp(rule).test(message.content);
                        if (toDelete) break;
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

                resolve(toDelete);
            });
        }
    }, {
        key: 'AddRule',
        value: function AddRule(rule) {
            var _this3 = this;

            return new Promise(function (resolve, reject) {
                _this3.config.rules.push(rule);
                _fs2.default.writeFile('./Config/Servers/' + _this3.server + '.json', JSON.stringify(_this3.config), 'utf8', function (err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(true);
                    }
                });
            });
        }
    }, {
        key: 'RemoveRule',
        value: function RemoveRule(index) {
            var _this4 = this;

            return new Promise(function (resolve, reject) {
                if (index >= _this4.config.rules.length) {
                    return reject('Rule #' + index + ' does not exist, to list rules type `!listrules`', null);
                }
                _this4.config.rules.splice(index, 1);
                _fs2.default.writeFile('./Config/Servers/' + _this4.server + '.json', JSON.stringify(_this4.config), 'utf8', function (err) {
                    if (err) {
                        reject('Error updating rule', err);
                    } else {
                        resolve(true);
                    }
                });
            });
        }
    }]);

    return AutoMod;
}();

exports.default = AutoMod;