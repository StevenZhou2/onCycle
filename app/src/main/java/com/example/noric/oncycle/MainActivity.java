package com.example.noric.oncycle;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Handler;
import android.os.SystemClock;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class MainActivity extends AppCompatActivity { //implements LocationListener {

    TextView Timer;
    TextView displaySpeed;
    Button start, pause, reset;
    long timeInMS, sTime, timeBuff;
    long updateTime = 0L;
    Handler handler;
    int seconds, minutes, ms;
    boolean left, right, brake;
/*
    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference myRef = database.getReference("message");

    myRef.addChildEventListener(new ValueEventListener() {
    @Override
    public void onDataChange(com.example.noric.oncycle.DataSnapshot dataSnapshot, String s) {
        // This method is called once with the initial value and again
        // whenever data at this location is updated.
        String value = dataSnapshot.getValue(String.class);
        Log.d(TAG, "Value is: " + value);
    }

    @Override
    public void onCancelled(DatabaseError error) {
        // Failed to read value
        Log.w(TAG, "Failed to read value.", error.toException());
        }
    });
*/

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Timer = (TextView) findViewById(R.id.tvTimer);
        start = (Button) findViewById(R.id.btStart);
        pause = (Button) findViewById(R.id.btPause);
        reset = (Button) findViewById(R.id.btReset);
        //LocationManager lm = (LocationManager) this.getSystemService(Context.LOCATION_SERVICE);

        // TODO: Consider calling
        //    ActivityCompat#requestPermissions
        // here to request the missing permissions, and then overriding
        //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
        //                                          int[] grantResults)
        // to handle the case where the user grants the permission. See the documentation
        // for ActivityCompat#requestPermissions for more details.
        //if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED)
         //   return;

        //lm.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1, 0, this);

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

/*
    @Override
    public void onLocationChanged(Location location) {

                displaySpeed = (TextView) findViewById(R.id.tvSpeed);

                if (location == null) {
                    displaySpeed.setText("-.--");
                } else {
                    double nCurrentSpeed = location.getSpeed() * 3.6;
                    displaySpeed.setText(Double.toString(nCurrentSpeed));
                }
            }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {

    }

    @Override
    public void onProviderEnabled(String provider) {

    }

    @Override
    public void onProviderDisabled(String provider) {

    }

*/
}

