import fs from 'fs';

class AutoMod {
    constructor(serverID) {
        this.server = serverID;

        fs.readFile('./Config/Servers/' + serverID + '.json', 'utf8', (err, data) => {
            if (err) return console.error('Error reading config:', err);
            this.config = JSON.parse(data);
            console.log(this.config);
        });
    }

    Moderate(message) {
        return new Promise((resolve, reject) => {
            let toDelete;
            for (let rule of this.config.rules) {
                toDelete = new RegExp(rule).test(message.content);
                if(toDelete) break;
            }
            resolve(toDelete);
        })
    }

    AddRule(rule) {
        return new Promise((resolve, reject) => {
            this.config.rules.push(rule);
            fs.writeFile('./Config/Servers/' + this.server + '.json', JSON.stringify(this.config), 'utf8', err => {
                if(err) {
                    reject(err);
                } else {
                    resolve(true);
                }
            });
        });
    }

    RemoveRule(index) {
        return new Promise((resolve, reject) => {
            if(index >= this.config.rules.length) {
                return reject('Rule #' + index + ' does not exist, to list rules type `!listrules`', null);
            }
            this.config.rules.splice(index, 1);
            fs.writeFile('./Config/Servers/' + this.server + '.json', JSON.stringify(this.config), 'utf8', err => {
                if(err) {
                    reject('Error updating rule', err);
                } else {
                    resolve(true);
                }
            });
        });
    }
}

export default AutoMod;