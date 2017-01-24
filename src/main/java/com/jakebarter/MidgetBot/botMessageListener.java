package com.jakebarter.MidgetBot;

import de.btobastian.javacord.DiscordAPI;
import de.btobastian.javacord.entities.message.Message;
import de.btobastian.javacord.listener.message.MessageCreateListener;

/**
 * Created by midg3 on 24/01/2017.
 */
public class botMessageListener implements MessageCreateListener {

    @Override
    public void onMessageCreate(DiscordAPI api, Message message) {
        //We don't want the bot to respond to itself... That's just sad
        if (!message.getAuthor().getId().equals("273529250689318923")) {
            //I get to see your messages >:)
            System.out.println(message.getAuthor().getName() + ": " + message.getContent());
            //Let's check if a command was called
            checkMessage(message);
        }
    }

    private void checkMessage(Message m){
        //First we need it broken down
        String[] msg = breakMessage(m);
        //We only want to check the first word

        //Sah dude command
        if (msg[0].equalsIgnoreCase("Sah")){
            m.reply("Sah dude");
        }
    }

    private void sendMessage(Message m){
        m.reply("Suh");
    }

    //Break up the message so we know each word
    private String[] breakMessage(Message m){
        String msg = m.getContent();
        String[] bMsg = msg.split(" ");
        return bMsg;
    }

}