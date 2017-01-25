package com.jakebarter.MidgetBot;

import com.google.common.util.concurrent.FutureCallback;
import de.btobastian.javacord.DiscordAPI;
import de.btobastian.javacord.Javacord;


public class botMain {
    public static void main(String[] args){

        //Setup our API call token
        DiscordAPI api = Javacord.getApi("#########################", true);
        String token = api.getToken(); //Storing it incase of future use
        System.out.println("Open");
        //Initialize the bot
        api.connect(new FutureCallback<DiscordAPI>() {

            //Hey! We connected
            public void onSuccess(final DiscordAPI api) {
                //Now let's listen to everyone's messages >:D
                botMessageListener myListener = new botMessageListener();
                api.registerListener(myListener);
                api.setGame("Dying on the inside");
            }

            //Well... something went wrong and we couldn't connect :(
            public void onFailure(Throwable t) {
                // login failed
                t.printStackTrace();
                System.out.println("It seems we cannot connect...");
                //WTF do we do if we cant connect?
            }
        });

    }
}
