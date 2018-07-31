import axios from 'axios';
import uuid from 'uuid/v1';
import he from 'he';
import { parse } from 'fast-xml-parser/src/parser';

class ChatBot {
    constructor(botID) {
        this.botID = botID;
    }

    Think(thought) {
        return new Promise((resolve, reject) => {
            const data = '?input=' + encodeURIComponent(thought) + '&' +
                'botid=' + this.botID + '&' +
                'uuid=' + uuid();

            axios.get('https://www.pandorabots.com/pandora/talk-xml' + data).then(response => {
                resolve(he.decode(parse(response.data).result.that));
            }).catch(err => {
                reject(null);
            });
        });
    }
}

export default ChatBot;