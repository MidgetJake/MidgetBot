package com.jakebarter.MidgetBot;

import java.util.Random;

//A class for 8 ball is nicer
//Means easy expansion
class bot8Ball {

    public String EBall(){
        Random random = new Random();
        int randomNum = random.nextInt((15) + 1);

        switch (randomNum){
            case 0 :
                return "It's not looking likely...";
            case 1:
                return "It's looking quite likely!";
            case 2:
                return "Look forward to it!";
            case 3:
                return "You don't understand...";
            case 4:
                return "Don't count on it";
            case 5:
                return "The future doesn't look bright";
            case 6:
                return "The future looks bright";
            case 7:
                return "YES!";
            case 8:
                return "Yes";
            case 9:
                return "NO!";
            case 10:
                return "No";
            case 11:
                return "It's a 50/50 chance";
            case 12:
                return "The chances are as high as you believe!";
            case 13:
                return "The chances are about as good as the quality of the code I am written with";
            case 14:
                return "...";
            default:
                return "I would rather not answer that...";
        }

    }
}
