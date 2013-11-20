var ws = new WebSocket("ws://localhost:8888/websocket");
ws.onmessage = function(evt){
  var msg = evt.data;
  HandleMavlink(msg);
                //var msg_json = JSON.parse(msg);
                //x = document.createElement("p");
                //x.innerHTML = new_text;
                //document.getElementById("chatbox").appendChild(x);
                //out_str = new_text.mavpackettype + String(new_text.system_status);
                //document.getElementById("heartbeat_text").innerHTML = msg_json;
}
 
function DispatchText(){
  //first, get message from input field
  var userInput = document.getElementById("message").value;
  //then, clear input field
  document.getElementById("message").value = "";
  //now, create a paragraph element
  x = document.createElement("p");
  //set the p text to the input 
  x.innerHTML = "You sent: " + userInput;
  //stick the input into the chat box
  document.getElementById("chatbox").appendChild(x);
  //send user input to server for processing
  ws.send(userInput);
}

function HandleMavlink(msg){
  var msg_json = JSON.parse(msg);
  switch(msg_json.mavpackettype)
  {
    case 'VFR_HUD':
      document.getElementById('alt').innerHTML = msg_json.alt.toFixed(3);
      document.getElementById('heading').innerHTML = msg_json.heading.toFixed(1);
      break;
    case 'ATTITUDE':
      document.getElementById('pitch').innerHTML = msg_json.pitch.toFixed(6);
      document.getElementById('roll').innerHTML = msg_json.roll.toFixed(6);
      break;
    case 'GPS_RAW_INT':
      document.getElementById('lat').innerHTML = (msg_json.lat/10000000).toFixed(7);
      document.getElementById('lon').innerHTML = (msg_json.lon/10000000).toFixed(7);
      document.getElementById('time_sec').innerHTML = (msg_json.time_usec/1000000).toFixed(4);
      break;
    default:    
      for(var part in msg_json){
        document.getElementById(msg_json.mavpackettype + part).innerHTML = msg_json[part].toString();
      }
  }
}
