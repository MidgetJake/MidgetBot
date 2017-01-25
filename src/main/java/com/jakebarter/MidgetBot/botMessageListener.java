package com.jakebarter.MidgetBot;

import com.vdurmont.emoji.EmojiParser;
import de.btobastian.javacord.DiscordAPI;
import de.btobastian.javacord.entities.message.Message;
import de.btobastian.javacord.listener.message.MessageCreateListener;

import java.util.Calendar;
import java.util.TimeZone;


class botMessageListener implements MessageCreateListener {

    //Hey! A new message
    public void onMessageCreate(DiscordAPI api, Message message) {
        //We don't want the bot to respond to itself... That's just sad
        if (!message.getAuthor().getId().equals("273529250689318923")) {
            //I get to see your messages >:)
            System.out.println(message.getAuthor().getName() + ": " + message.getContent());
            //Let's check if a command was called
            checkMessage(api, message);
        }
    }

    //Break up the message so we know each word
    private String[] breakMessage(Message m){
        String msg = m.getContent();
        //Split that string!
        return msg.split(" ");
    }

    //Check for commands
    private void checkMessage(DiscordAPI api, Message m){
        try {
            //First we need it broken down
            String[] msg = breakMessage(m);
            //We only want to check the first word

            //This is 100% the wrong way to do this... But it works
            if(m.getContent().toLowerCase().contains("<@273529250689318923>")){
                botResponse talk = new botResponse();
                //m.reply(talk.botChat(msg)); //This is the old dumb chat
                m.reply(talk.cleverChat(msg)); //Not that this chat is very clever
            }

            if(msg[0].equalsIgnoreCase("!time")){
                if (msg.length>1){
                    try {
                        TimeZone tz = TimeZone.getTimeZone(msg[1]);
                        Calendar c = Calendar.getInstance(tz);
                        m.reply(c.get(java.util.Calendar.HOUR_OF_DAY) + ":" + c.get(java.util.Calendar.MINUTE) + ":" + c.get(java.util.Calendar.SECOND) + " " + msg[1]);
                    }
                    catch (Exception e) {
                        m.reply("Does that timezone exist?");
                        m.reply("If it does send this to the dev: ");
                        m.reply(e.toString());
                    }
                } else {
                    //We default to GMT because it is the best time
                    TimeZone tz = TimeZone.getTimeZone("GMT");
                    Calendar c = Calendar.getInstance(tz);
                    m.reply(c.get(java.util.Calendar.HOUR_OF_DAY) + ":" + c.get(java.util.Calendar.MINUTE) + ":" + c.get(java.util.Calendar.SECOND) + " GMT");
                }
            }

            if (msg[0].equalsIgnoreCase("!help")){
                if (msg.length > 1){
                    botHelp help = new botHelp();
                    m.reply(help.helpMsg(msg[1]));
                } else {
                    m.reply("```The list of commands that the bot currently supports/has \n" +
                            "note:Not all of these are 100% functional\n" +
                            "Type !help + command to see extra details\n\n" +
                            "**Commands:**\n" +
                            "!help - You just used it\n" +
                            "Fuck - Teaches people not to be rude\n" +
                            "!program - non-functional possibly going to compile code?\n" +
                            "friend? - Is the bot your friend?\n" +
                            "!navyseal - Come on... You know this...\n" +
                            "!time - Displays current time\n" +
                            "image - Not a command but still... Type !help image to see more```");
                }
            }

            // Upvote/Downvote for images
            if (!m.getAttachments().isEmpty()) {
                String tu = EmojiParser.parseToUnicode(":thumbsup:");
                String td = EmojiParser.parseToUnicode(":thumbsdown:");
                m.addUnicodeReaction(tu);
                try {
                    Thread.sleep(750); //  half a second
                } catch(InterruptedException ex) {
                    Thread.currentThread().interrupt();
                }
                m.addUnicodeReaction(td);
            }
            //Sah dude command
            if (msg[0].equalsIgnoreCase("Sah")) {
                m.reply("Sah dude");
            }



            //I guess some server info will be posted here
            if (msg[0].equalsIgnoreCase("!server")) {
                m.reply("This dones't work yet, get away!");
            }

            //People really shouldn't be so rude...
            if (msg.length > 1) { //This stops it from breaking...
                if (msg[0].equalsIgnoreCase("Fuck") && (msg[1].equalsIgnoreCase("you") || msg[1].equalsIgnoreCase("u"))) {
                    m.reply("Fuck you too " + m.getAuthor().getMentionTag());
                }
            }

            //Here because read message
            if(msg[0].equalsIgnoreCase("!Program")){
                m.reply("This might be an exprimental cmd at some point");
            }

            //Makes Jake feel like he has a friend
            if (msg[0].equalsIgnoreCase("Friend?")) {
                if (m.getAuthor().getId().equals("95677195162222592")) {
                    m.reply("I am your best friend Jake! <3");
                } else {
                    m.reply("NO! Jake is my only true friend!");
                }
            }

            if (msg[0].equalsIgnoreCase("!navyseal")) {
                m.reply(navyseal());
            }

            if (msg[0].equalsIgnoreCase("8ball")) {
                bot8Ball a = new bot8Ball();
                m.reply(a.EBall());
            }
        }
        catch (Exception e){
            m.reply("Wow... You broke the bot?");
            m.reply("Send this to the dev to help fix this:");
            m.reply(e.toString());
        }
    }

    // --- Command functions from here ----

    //The entire navy seal copypasta
    private String navyseal(){
        return "What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated " +
                "top of my class in the Navy Seals, and I’ve been involved in numerous secret raids on Al-Quaeda, " +
                "and I have over 300 confirmed kills. I am trained in gorilla warfare and I’m the top sniper in the " +
                "entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck " +
                "out with precision the likes of which has never been seen before on this Earth, mark my fucking " +
                "words. You think you can get away with saying that shit to me over the Internet? Think again, " +
                "fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being " +
                "traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic " +
                "little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can " +
                "kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively " +
                "trained in unarmed combat, but I have access to the entire arsenal of the United States Marine " +
                "Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, " +
                "you little shit. If only you could have known what unholy retribution your little “clever” comment " +
                "was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, " +
                "you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and " +
                "you will drown in it. You’re fucking dead, kiddo.";
        //Holy shit that was long...
    }

}
