class AutoMod {
    constructor(serverID) {
        this.server = serverID;
    }

    Moderate(message) {
        return new Promise((resolve, reject) => {
            resolve(/.*(yeet).*/.test(message.content));
        })
    }
}

export default AutoMod;