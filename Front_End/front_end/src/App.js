import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  MeetingProvider,
  useMeeting,
  useParticipant,
  Constants,
} from "@videosdk.live/react-sdk";
import ReactPlayer from "react-player";
import Hls from "hls.js";

function SpeakerView() {
  return null;
}
function ViewerView() {
  return null;
}
const App = () => {
  const [mode, setMode] = useState(null);

  return mode ? (
    <MeetingProvider
      config={{
        meetingId: "z5dw-5392-mcae",
        micEnabled: true,
        webcamEnabled: true,
        name: "Nhlanhla's Org",
        mode,
      }}
      joinWithoutUserInteraction
      token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlrZXkiOiIyYzgxZjgyOC1lNDUwLTQ5N2MtYmJjZi05NjAzNGNhMWMyOWIiLCJwZXJtaXNzaW9ucyI6WyJhbGxvd19qb2luIl0sImlhdCI6MTcyNTI1NjQzMiwiZXhwIjoxNzI1MzQyODMyfQ.ZZcL3Kcs7MvULGWWlngDl_vNUS3Q9DqKC72TvQBfJAA"
    >
      {mode === Constants.modes.CONFERENCE ? <SpeakerView /> : <ViewerView />}
    </MeetingProvider>
  ) : (
    <div>
      <button
        onClick={() => {
          setMode(Constants.modes.CONFERENCE);
        }}
      >
        Join as Speaker
      </button>
      <button
        style={{ marginLeft: 12 }}
        onClick={() => {
          setMode(Constants.modes.VIEWER);
        }}
      >
        Join as Viewer
      </button>
    </div>
  );
};

export default App;
