package com.jakebarter.MidgetBot;

import com.google.common.util.concurrent.FutureCallback;
import de.btobastian.javacord.DiscordAPI;
import de.btobastian.javacord.Javacord;

/**
 * Created by midg3 on 24/01/2017.
 */
public class botMain {
    public static void main(String[] args){

        //Setup our API call token
        DiscordAPI api = Javacord.getApi("MjczNTI5MjUwNjg5MzE4OTIz.C2k84Q.zPJuuR5HMV-QYwm6oPpKr4BEg4Y", true);
        String token = api.getToken(); //Storing it incase of future use

        //Initialize the bot
        api.connect(new FutureCallback<DiscordAPI>() {

            //Hey! We connected
            @Override
            public void onSuccess(final DiscordAPI api) {
                //Now let's listen to everyone's messages >:D
                botMessageListener myListener = new botMessageListener();
                api.registerListener(myListener);
            }

            //Well... something went wrong and we couldn't connect :(
            @Override
            public void onFailure(Throwable t) {
                // login failed
                t.printStackTrace();
            }
        });

    }



}
