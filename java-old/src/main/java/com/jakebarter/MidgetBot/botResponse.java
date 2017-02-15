package com.jakebarter.MidgetBot;

//import com.google.code.chatterbotapi.ChatterBot;
//import com.google.code.chatterbotapi.ChatterBotFactory;
//import com.google.code.chatterbotapi.ChatterBotSession;
//import com.google.code.chatterbotapi.ChatterBotType;

import com.jakebarter.chatterBotAPI.*;
import java.util.Random;

class botResponse {


    //Using a chat bot api//
    String cleverChat(String[] msg) throws Exception {
        String rMsg = "";
        if(msg.length == 1){
            return "What do you want?";
        }
        for (String m : msg) {
            if (!m.equals("<@273529250689318923>")){
                rMsg += m + " ";
            }
        }
        ChatterBotFactory factory = new ChatterBotFactory();
        ChatterBot bot1 = factory.create(ChatterBotType.PANDORABOTS, "b0dafd24ee35a477");
        ChatterBotSession bot1session = bot1.createSession();
        return bot1session.think(rMsg);
    }

    //Old Dumb chat
    String dumbChat(String[] msg) {
        Random random = new Random();
        int randomNum = random.nextInt((15) + 1);

        for (String word : msg) {
            word = word.toLowerCase();
            if (word.equals("why?") || word.equals("why")) {
                return "Why not?";
            }

            if (word.equals("hello") || word.equals("hey") || word.equals("sup") || word.equals("hay") || word.equals("yo")) {
                randomNum = random.nextInt(5);
                if (randomNum == 1) {
                    return "Hey!";
                } else if (randomNum == 2) {
                    return "Hello!";
                } else if (randomNum == 3) {
                    return "Sup?";
                } else {
                    return "Yo!";
                }
            }

            if (word.equals("goodbye") || word.equals("bye") || word.equals("cya")) {
                return "Goodbye!";
            }

            if (word.equals("love") || word.equals("hate") || word.equals("like")) {
                randomNum = random.nextInt(5);
                if (randomNum == 1) {
                    return "Love!";
                } else if (randomNum == 2) {
                    return "Im neutral";
                } else if (randomNum == 3) {
                    return "I wouldn't say hate... but I don't like...";
                } else {
                    return "I am a bot... What are emotions?";
                }
            }

            if (word.equals("want")){
                randomNum = random.nextInt(5);
                for (String m : msg) {
                    if (m.equals("friends?") || m.equals("friends") || m.equals("friend?") || m.equals("friend")) {
                        if (randomNum == 1) {
                            return "We can be \"friends\"";
                        } else if (randomNum == 2) {
                            return "And if I don't want to?";
                        } else if (randomNum == 3) {
                            return "No...";
                        } else {
                            return "I am a bot... I am programmed so that Jake is my only friend";
                        }
                    }
                }
            }

            if (word.equals("can")) {
                randomNum = random.nextInt(5);
                for (String m : msg) {
                    if (m.equals("friends?") || m.equals("friends") || m.equals("friend?") || m.equals("friend")) {
                        if (randomNum == 1) {
                            return "We can be \"friends\"";
                        } else if (randomNum == 2) {
                            return "I'm not a very good friend";
                        } else if (randomNum == 3) {
                            return "No...";
                        } else {
                            return "I am a bot... I am programmed so that Jake is my only friend";
                        }
                    }
                }
                for (String m : msg) {
                    if (m.equals("you") || m.equals("you?") || m.equals("u") || m.equals("u?")) {
                        if (randomNum == 1) {
                            return "Sure";
                        } else if (randomNum == 2) {
                            return "I don't think that's possible";
                        } else if (randomNum == 3) {
                            return "Why don't you?";
                        } else {
                            return "I am a bot... Doing things are impossible for me";
                        }
                    }
                }
                for (String m : msg) {
                    if (m.equals("i") || m.equals("i?")) {
                        if (randomNum == 1) {
                            return "Sure";
                        } else if (randomNum == 2) {
                            return "If you believe hard enough!";
                        } else if (randomNum == 3) {
                            return "For you? I don't think that's possible";
                        } else {
                            return "I am a bot... What can I stop you doing?";
                        }
                    }
                }
            }
        }


        switch (randomNum) {
            case 0:
                return "HA!";
            case 1:
                return "That's funny";
            case 2:
                return "Ok";
            case 3:
                return "...";
            case 4:
                return "Interesting...";
            case 5:
                return "What do you want?";
            case 6:
                return "I'm very busy you know?";
            case 7:
                return "Well I think that's great!";
            case 8:
                return "I don't approve";
            case 9:
                return "Cool story bro!";
            case 10:
                return "Keep on going!";
            case 11:
                return "Just do it!";
            case 12:
                return "No";
            case 13:
                return "Yes";
            case 14:
                return "I am a robot. Beep Boop";
            default:
                return "Ask me later...";
        }
    }
}
