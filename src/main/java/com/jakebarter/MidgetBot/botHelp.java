package com.jakebarter.MidgetBot;

//Same as 8Ball
//Separate class for easy expansion
class botHelp {

    String helpMsg(String cmd){
        cmd = cmd.toLowerCase();

        if (cmd.equals("!help")) {
            return "```You just used this... \n\n - Will give you help ```";
        } else if (cmd.equals("!server")) {
            return "```!server command: \n\n - Currently does nothing \n - Planning to add server info here```";
        } else if (cmd.equals("fuck")) {
            return "```Use \"Fuck you\" or \"Fuck u\" \n\n - Some people are rude and need to know there place```";
        } else if (cmd.equals("!program")) {
            return "```!program command: \n\n - Currently does nothing \n - Maybe able to compile code later on?```";
        } else if (cmd.equals("friend?")) {
            return "```Is the bot your friend? \n\n - The bot will respond if you are it's friend```";
        } else if (cmd.equals("!navyseal")) {
            return "```Copypasta command \n\n - What did you just say to me?```";
        } else if (cmd.equals("8ball")) {
            return "```The mystical ball! \n\n - It knows the truth \n - Can predict the future```";
        } else if (cmd.equals("!time")) {
            return "```!time [Zone]\n\n - Get the time in a timezone \n - [Zone] requires abbreviations e.g. GMT/PST \n - Will display current time in timezones```";
        } else if (cmd.equals("image")) {
            return "```Automatic on all images \n\n - Upvote/downvotes on images posted```";
        } else {
            return "Unknown Command: " + cmd;
        }
    }
}
