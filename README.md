# OmniCall Headless SDK

A lightweight, headless WebRTC engine for 1-on-1 voice calls. Works across Web, Mobile Web, and Desktop.

## Features
- **Headless:** No UI included. Build your own interface.
- **Auto-Busy:** Automatically rejects incoming calls if user is already in a call.
- **Cross-Platform:** Connect Web-to-Web, Mobile-to-Mobile, or Web-to-Mobile.
- **Hardware Management:** Automatically handles microphone permissions and cleanup.

## Installation
Import the `OmniCall` class into your project:

```javascript
import { OmniCall } from './path/to/sdk_core/web/core.js';


## QUICK START

const voice = new OmniCall({
    userId: "User_Unique_ID", // Can be Phone Number or String
    serverUrl: "ws://your-signaling-server:8000",
    onReady: () => console.log("Connected to server"),
    onIncoming: (callerId) => {
        // Show your custom "Incoming Call" popup here
        if(confirm("Call from " + callerId)) {
            voice.acceptCall();
        } else {
            voice.hangup();
        }
    },
    onAccepted: () => console.log("Call Connected!"),
    onBusy: () => alert("User is on another call"),
    onHangup: () => console.log("Call Ended")
});

voice.connect();


## CONTROL CALLS

// Start a call
voice.startCall("Target_User_ID");

// Mute logic (Implementation example)
voice.localStream.getAudioTracks()[0].enabled = false;

// End a call
voice.hangup();