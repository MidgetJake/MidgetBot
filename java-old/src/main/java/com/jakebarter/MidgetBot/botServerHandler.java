package com.jakebarter.MidgetBot;

import de.btobastian.javacord.DiscordAPI;
import de.btobastian.javacord.entities.Server;
import java.util.ArrayList;
import java.util.Hashtable;

//We gonna be handling all the servers we know here!
class botServerHandler {

    private Hashtable<String, botServer> serverList = new Hashtable<String, botServer>();

    public botServerHandler(DiscordAPI api, Server server) {

        botServerJoinListener serverJoin = new botServerJoinListener();
        api.registerListener(serverJoin);

        boolean joined = checkServer(server);
        if(!joined){ //This is saying it's always true but the method returns false... wut...
            setupServer(api, server);
        }

        //let's debug some shit
        System.out.println("AHH   " + server);
    }

    //HOW THE FUCK DO WE GET SERVER INFO!?!?!??!?!?!?!?
    public boolean checkServer(Server server){
        //Are we already a part of this server?
        return false; //Not setup anything yet...
    }

    //Hey did we join a new server? Let's see...


    //Put a new server into a hastable... Hope this works...
    public void setupServer(DiscordAPI api, Server server){
        //How well will this work...
        serverList.put(server.getId(), new botServer(api, server));
    }
}
