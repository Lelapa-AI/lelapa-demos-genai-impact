import { ParticipantView } from "./ParticipantView";
// import { Constants } from "@videosdk.live/react-sdk/dist/types/participant";
import { Container } from "./Container";
import { Controls } from "./Controls";
import {
  useMeeting,
  Constants,
  // useParticipant,
} from "@videosdk.live/react-sdk";
import React, { useMemo } from "react";

export function SpeakerView() {
  //Get the participants and HLS State from useMeeting
  const { participants, hlsState } = useMeeting();

  //Filtering the host/speakers from all the participants
  const speakers = useMemo(() => {
    const speakerParticipants = [...participants.values()].filter(
      (participant) => {
        return participant.mode === Constants.modes.CONFERENCE;
      }
    );
    return speakerParticipants;
  }, [participants]);
  return (
    <div>
      <p>Current HLS State: {hlsState}</p>
      {/* Controls for the meeting */}
      <Controls />

      {/* Rendring all the HOST participants */}
      {speakers.map((participant) => (
        <ParticipantView participantId={participant.id} key={participant.id} />
      ))}
    </div>
  );
}

<Container></Container>;
