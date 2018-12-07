/*
*Android Application: onCylce
*onCycle is a system that mimics a car's turning features and transfers
*that to a bicycle
*Developer: Steven Zhou
*/

package com.example.noric.oncycle;

import android.annotation.SuppressLint;
import android.os.Handler;
import android.os.SystemClock;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

//Imports for firebase functionalities
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

public class MainActivity extends AppCompatActivity {
    
    //Declaring variables for Android views
    TextView Timer;
    TextView displayAcc;
    Button start, pause, reset;
    ImageView leftArr, rightArr, brakes;
    
    //Declaring variables for creating the timer
    long timeInMS, sTime, timeBuff;
    long updateTime = 0L;
    Handler handler;
    int seconds;
    int minutes;
    int ms;
    
    //Declaring variables to reference the database (firebase)
    private DatabaseReference AvgAcc;
    private DatabaseReference rightTurn;
    private DatabaseReference leftTurn;
    private DatabaseReference brakeSignal;
    
    //Created a start timer function as it is used during the start of application
    //along with the start button
    private void startTimer(){
        sTime = SystemClock.uptimeMillis();
        handler.postDelayed(runnable, 0);

        reset.setEnabled(false);
    }
    
    //Starts the timer as the application is launched
    @Override
    protected void onStart() {
        super.onStart();

        startTimer();
    }
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    
        setContentView(R.layout.activity_main);

        //Declaring variables for Android views
        Timer = (TextView) findViewById(R.id.tvTimer);
        start = (Button) findViewById(R.id.btStart);
        pause = (Button) findViewById(R.id.btPause);
        reset = (Button) findViewById(R.id.btReset);
        displayAcc = (TextView) findViewById(R.id.tvAcc);
        leftArr = (ImageView) findViewById(R.id.leftArrow);
        rightArr = (ImageView) findViewById(R.id.rightArrow);
        brakes = (ImageView) findViewById(R.id.brakes);
    
        //Variables used for referencing points in firebase
        AvgAcc = FirebaseDatabase.getInstance().getReference().child("data").child("AvgAcc");
        rightTurn = FirebaseDatabase.getInstance().getReference().child("data").child("RightTurn");
        leftTurn = FirebaseDatabase.getInstance().getReference().child("data").child("LeftTurn");
        brakeSignal = FirebaseDatabase.getInstance().getReference().child("data").child("BrakeSignal");

        //Event listener for updates on AvgAcc in firebase
        AvgAcc.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String AvgAccValue = dataSnapshot.getValue().toString();
                displayAcc.setText("Average Acceleration: " + AvgAccValue);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        //Event listener for updates on leftTurn in firebase
        leftTurn.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String leftTurnValue = dataSnapshot.getValue().toString();
                //Display image if signal is on, otherwise do not display
                if (leftTurnValue.equals("1")) {
                    leftArr.setVisibility(View.VISIBLE);
                }else {
                    leftArr.setVisibility(View.INVISIBLE);
                }
            }
            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        
        //Event listener for updates on rightTurn in firebase
        rightTurn.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String rightTurnValue = dataSnapshot.getValue().toString();
                //Display image if signal is on, otherwise do not display
                if (rightTurnValue.equals("1")) {
                    rightArr.setVisibility(View.VISIBLE);
                }else {
                    rightArr.setVisibility(View.INVISIBLE);
                }
            }
            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
        
        //Event listener for updates on brakeSignal in firebase
        brakeSignal.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String brakeSignalValue = dataSnapshot.getValue().toString();
                //Display image if signal is on, otherwise do not display
                if (brakeSignalValue.equals("1")) {
                    brakes.setVisibility(View.VISIBLE);
                } else {
                    brakes.setVisibility(View.INVISIBLE);
                }
            }
            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        handler = new Handler();
        
        /*
        *Created event listener for start button
        *Start button will initiate the timer
        */
        start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startTimer();
            }
        });
        
        /*
        *Created event listener for pause button
        *Reset button will pause the time variables and will display the last registered time variable
        */
        pause.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
               timeBuff += timeInMS;

               handler.removeCallbacks(runnable);

               reset.setEnabled(true);
            }
        });
        
        /*
        *Created event listener for reset button
        *Reset button will reset the time variables to 0; android application will display 00:00:00
        */
        reset.setOnClickListener(new View.OnClickListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onClick(View view) {
                timeInMS = 0L;
                sTime = 0L;
                timeBuff = 0L;
                updateTime = 0L;
                seconds = 0;
                minutes = 0;
                ms = 0;

                Timer.setText("00:00:00");
            }
        });
    }
    
    /*
    *Created a runnable object that will update the timer as the time has been elapsed
    */
    public Runnable runnable = new Runnable() {
        public void run() {
            timeInMS = SystemClock.uptimeMillis() - sTime;
            updateTime = timeBuff + timeInMS;
            seconds = (int) (updateTime / 1000);
            minutes = seconds / 60;
            seconds = seconds % 60;
            ms = (int) (updateTime % 1000);

            Timer.setText("" + minutes + ":" + String.format("%02d", seconds) + ":" + String.format("%03d", ms));
            handler.postDelayed(this, 0);
        }
    };
}
