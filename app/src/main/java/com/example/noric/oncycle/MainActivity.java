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

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;


public class MainActivity extends AppCompatActivity {

    TextView Timer;
    TextView displayAcc;
    Button start, pause, reset;
    ImageView leftArr, rightArr, brakes;
    long timeInMS, sTime, timeBuff;
    long updateTime = 0L;
    Handler handler;
    int seconds, minutes, ms;

    private DatabaseReference AvgAcc;
    private DatabaseReference isTurned;
    private DatabaseReference rightTurn;
    private DatabaseReference leftTurn;
    private DatabaseReference brakeSignal;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Timer = (TextView) findViewById(R.id.tvTimer);
        start = (Button) findViewById(R.id.btStart);
        pause = (Button) findViewById(R.id.btPause);
        reset = (Button) findViewById(R.id.btReset);
        displayAcc = (TextView) findViewById(R.id.tvAcc);
        leftArr = (ImageView) findViewById(R.id.leftArrow);
        rightArr = (ImageView) findViewById(R.id.rightArrow);
        brakes = (ImageView) findViewById(R.id.brakes);

        AvgAcc = FirebaseDatabase.getInstance().getReference().child("data").child("AvgAcc");
        isTurned = FirebaseDatabase.getInstance().getReference().child("data").child("isTurned");
        rightTurn = FirebaseDatabase.getInstance().getReference().child("data").child("RightTurn");
        leftTurn = FirebaseDatabase.getInstance().getReference().child("data").child("LeftTurn");
        brakeSignal = FirebaseDatabase.getInstance().getReference().child("data").child("BrakeSignal");

        AvgAcc.addValueEventListener(new ValueEventListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String AvgAccValue = dataSnapshot.getValue().toString();
                displayAcc.setText("Avgerage Accleration: " + AvgAccValue);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        isTurned.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String isTurnedValue = dataSnapshot.getValue().toString();
                if (isTurnedValue.equals("1")) {
                    rightArr.setVisibility(View.INVISIBLE);
                    leftArr.setVisibility(View.INVISIBLE);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        leftTurn.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String leftTurnValue = dataSnapshot.getValue().toString();
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

        rightTurn.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String rightTurnValue = dataSnapshot.getValue().toString();
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

        brakeSignal.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String brakeSignalValue = dataSnapshot.getValue().toString();
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

        start.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sTime = SystemClock.uptimeMillis();
                handler.postDelayed(runnable, 0);

                reset.setEnabled(false);
            }
        });

        pause.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
               timeBuff += timeInMS;

               handler.removeCallbacks(runnable);

               reset.setEnabled(true);
            }
        });

        reset.setOnClickListener(new View.OnClickListener() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onClick(View view) {
                timeInMS = 0L;
                sTime = 0L;
                updateTime = 0L;
                seconds = 0;
                minutes = 0;
                ms = 0;

                Timer.setText("00:00:00");
            }
        });
    }

    public Runnable runnable = new Runnable() {
        @SuppressLint({"SetTextI18n", "DefaultLocale"})
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
