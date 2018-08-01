class Mod {
    constructor(){}

    ParseCommand(message, autoMod) {
        if (message.cleanContent[0] !== '!' && message.cleanContent[0].length < 2) return false;
        const command = message.cleanContent.split(' ')[0].split('!')[1].toLowerCase();
        switch(command) {
            case 'addrule':
                return this.AddRule(message, autoMod);
            case 'listrules':
                return this.ListRules(message, autoMod);
            case 'delrule':
                return this.RemoveRule(message, autoMod);
        }
    }

    AddRule(message, autoMod) {
        const msg = message.cleanContent.split(' ');
        msg.splice(0, 1);
        autoMod.AddRule(msg.join(' ')).then(() => {
            message.reply('👍 Rule added!');
        }).catch(err => {
            console.error('Error writing to file:', err);
        });
    }

    ListRules(message, autoMod) {
        let rules = '';
        autoMod.config.rules.map((rule, index) => {
            rules += '\n [' + index + '] ' + rule;
        });

        message.reply('```ps' + rules + '\n```');
    }

    RemoveRule(message, autoMod) {
        const msg = message.cleanContent.split(' ');
        if(isNaN(msg[1])) {
            message.reply('Input the rule index, to find it type `!listrules`');
            return false;
        }
        autoMod.RemoveRule(parseInt(msg[1])).then(() => {
            message.reply('👍 Rule removed!');
        }).catch((msg, err) => {
            if(err) {
                console.error('Error writing to file:', err);
            }
            message.reply(msg);
        });
    }
}

export default Mod;