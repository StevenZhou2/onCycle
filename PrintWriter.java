import processing.serial.*;

public class PrintWriter{

//File IO Definitions
Serial mySerial;
PrintWriter output;

void setup(){
	//Define Serial stream and write output
	mySerial = new Serial(this,Serial.list()[0],9600);
	output = createWriter("accData.txt");
}

void draw(){
	if (mySerial.available()>0){
		String value = mySerial.readString();
		if (value!=null){
			output.println(value);
		}
	}

}

void keyPressed(){
	output.flush();
	output.close();
	exit();
}

}