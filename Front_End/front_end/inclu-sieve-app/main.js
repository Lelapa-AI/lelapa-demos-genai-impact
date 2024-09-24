// Import the functions you need from the SDKs you need
// import firebase from "firebase/app";
import "firebase/firestore";
import {
  getFirestore,
  collection,
  setDoc,
  doc,
  getDocs,
  onSnapshot,
} from "firebase/firestore";
// import firebase from "firebase/app";
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// import { getDoc } from "firebase/firestore";
// import { getDocs } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyATL0kM5_0AtDf9s82S6Hz-GXjhO-QM-Tw",
  authDomain: "inclu-sieve-app.firebaseapp.com",
  projectId: "inclu-sieve-app",
  storageBucket: "inclu-sieve-app.appspot.com",
  messagingSenderId: "945616995076",
  appId: "1:945616995076:web:e86046e7484b8511400651",
  measurementId: "G-BHW616HFTN",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
const db = getFirestore(app);
// const collect = collection(db, "calls");
// const snapshot = await getDocs(collect);

const querySnapshot = await getDocs(collection(db, "calls"));

querySnapshot.forEach((doc) => {
  console.log(`${doc.id} => ${doc.data()}`);
});
// const callDoc = onSnapshot(collect, (snapshot) => {
//   snapshot.docChanges().forEach((change) => {
//     if (change.type === "added") {
//       console.log("New call: ", change.doc.data());
//     }
//     if (change.type === "modified") {
//       console.log("Modified call: ", change.doc.data());
//     }
//     if (change.type === "removed") {
//       console.log("Removed call: ", change.doc.data());
//     }
//   });
// })

// if (!firebase.app.length) {
//   firebase.initializeApp(firebaseConfig);
// }
// const firestore = firebase.firestore();

const servers = {
  iceServers: [
    {
      urls: ["stun:stun1.l.google.com:19302", "stun:stun2.l.google.com:19302"],
    },
  ],
  iceCandidatePoolSize: 10,
};

// Global State
const pc = new RTCPeerConnection(servers);
let localStream = null;
let remoteStream = null;

// HTML elements
const webcamButton = document.getElementById("webcamButton");
const webcamVideo = document.getElementById("webcamVideo");
const callButton = document.getElementById("callButton");
const callInput = document.getElementById("callInput");
const answerButton = document.getElementById("answerButton");
const remoteVideo = document.getElementById("remoteVideo");
const hangupButton = document.getElementById("hangupButton");

// 1. Setup media sources

webcamButton.onclick = async () => {
  localStream = await navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true,
  });
  remoteStream = new MediaStream();

  // Push tracks from local stream to peer connection
  localStream.getTracks().forEach((track) => {
    pc.addTrack(track, localStream);
  });
  remoteStream.getTracks().forEach((track) => {
    pc.addTrack(track, remoteStream);
  });

  // Pull tracks from remote stream, add to video stream
  pc.ontrack = (event) => {
    event.streams[0].getTracks().forEach((track) => {
      remoteStream.addTrack(track);
    });
  };

  webcamVideo.srcObject = localStream;
  remoteVideo.srcObject = remoteStream;

  callButton.disabled = true;
  answerButton.disabled = false;
  webcamButton.disabled = true;
};

// 2. Create an offer
callButton.onclick = async () => {
  // Reference Firestore collections for signaling
  // const callDoc = db.getFirestore.collection("calls").doc(callDoc);
  const callDocRef = doc(collection(db, "calls"));

  // const offerCandidates = callDoc.collection("offerCandidates");
  // const answerCandidates = callDoc.collection("answerCandidates");

  const offerCandidates = collection(callDocRef, "offerCandidates");
  const answerCandidates = collection(callDocRef, "answerCandidates");

  callInput.value = callDocRef.id;

  // Get candidates for caller, save to db
  pc.onicecandidate = (event) => {
    event.candidate && addDoc(offerCandidates, event.candidate.toJSON());
  };

  // Create offer
  const offerDescription = await pc.createOffer();
  await pc.setLocalDescription(offerDescription);

  const offer = {
    sdp: offerDescription.sdp,
    type: offerDescription.type,
  };

  // await callDoc.set({ offer });
  await setDoc(callDocRef, { offer });

  // Listen for Remote answer

  // unsubscribe.onSnapshot((snapshot) => {
  //   const data = snapshot.data();
  //   if (!pc.currentRemoteDescription && data?.answer) {
  //     const answerDescription = new RTCSessionDescription(data.answer);
  //     pc.setRemoteDescription(answerDescription);
  //   }
  // });

  // const unsubscribe = callDoc.onSnapshot((collect) => {
  //   const data = collect.data();
  //   if (!pc.currentRemoteDescription && data?.answer) {
  //     const answerDescription = new RTCSessionDescription(data.answer);
  //     pc.setRemoteDescription(answerDescription);
  //     console.log(collect);
  //   }
  // });

  // snapshot.forEach((doc) => {
  //   console.log(doc.id, " => ", doc.data());
  // });

  // const unsubscribe = await db.collection("calls").get();
  // snapshot.forEach((doc) => {
  //   console.log(doc.id, "=>", doc.data());
  // });

  // Listen for remote answer
  // callDoc.onSnapshot((snapshot) => {
  //   const data = snapshot.data(callDoc);
  //   if (!pc.currentRemoteDescription && data?.answer) {
  //     const answerDescription = new RTCSessionDescription(data.answer);
  //     pc.setRemoteDescription(answerDescription);
  //     console.log(doc.snapshot);
  //   }
  // });

  // callDoc.onSnapshot((doc) => {
  //   const data = doc.data(); // Use doc.data() to get the data
  //   if (!pc.currentRemoteDescription && data?.answer) {
  //     const answerDescription = new RTCSessionDescription(data.answer);
  //     pc.setRemoteDescription(answerDescription);
  //     console.log(data); // Use data instead of doc.collect
  //   }
  // });

  // db.collection("calls")
  //   .doc(callDoc.id)
  //   .onSnapshot((doc) => {
  //     console.log("Current data: ", doc.data());
  //   });

  // const snapshot = onSnapshot(doc(db, "calls"), (doc) =>
  //   console.log("Current data: ", doc.data())
  // );

  // When answered, add candidate to peer connection

  pc.onicecandidate = (event) => {
    event.candidate && addDoc(answerCandidates, event.candidate.toJSON());
  };

  const answerDescription = await pc.createOffer();
  await pc.setLocalDescription(answerDescription);

  const answer = {
    sdp: answerDescription.sdp,
    type: answerDescription.type,
  };

  // await callDoc.set({ offer });
  await setDoc(callDocRef, { answer });

  // answerCandidates.onSnapshot((snapshot) => {
  //   snapshot.docChanges().forEach((change) => {
  //     if (change.type === "added") {
  //       const candidate = new RTCIceCandidate(change.doc.data());
  //       pc.addIceCandidate(candidate);
  //     }
  //   });
  // });

  const unsubscribe = onSnapshot(callDocRef, (snapshot) => {
    const data = snapshot.data();
    if (!pc.currentRemoteDescription && data?.answer) {
      const answerDescription = new RTCSessionDescription(data.answer);
      pc.setRemoteDescription(answerDescription);
    }
  });

  hangupButton.disabled = false;
};

// 3. Answer the call with the unique ID
answerButton.onclick = async () => {
  // const callId = callInput.value;
  // const callDoc = doc(collection(db, "answer"));

  // const answerCandidates = callDoc.collection("answerCandidates");
  // const offerCandidates = callDoc.collection("offerCandidates");

  // callInput.value = callDoc.id;

  // pc.onicecandidate = (event) => {
  //   event.candidate && answerCandidates.add(event.candidate.toJSON());
  // };

  // const callData = (await callDoc.get()).data();

  // const offerDescription = callData.offer;
  // await pc.setRemoteDescription(new RTCSessionDescription(offerDescription));

  // const answerDescription = await pc.createAnswer();
  // await pc.setLocalDescription(answerDescription);

  const callId = callInput.value; // Assuming you have a call ID
  const answerCollectionRef = collection(
    db,
    "answer",
    callId,
    "answerCandidates"
  );
  const offerCollectionRef = collection(
    db,
    "answer",
    callId,
    "offerCandidates"
  );

  pc.onicecandidate = (event) => {
    event.candidate &&
      addDoc(answerCollectionRef, offerCollectionRef, event.candidate.toJSON());
  };

  const callDocRef = doc(db, "answer", callId);
  const callData = (await getDocs(callDocRef)).data();

  const offerDescription = callData.offer;
  await pc.setRemoteDescription(new RTCSessionDescription(offerDescription));

  const answerDescription = await pc.createAnswer();
  await pc.setLocalDescription(answerDescription);

  const answer = {
    type: answerDescription.type,
    sdp: answerDescription.sdp,
  };

  await callDoc.update({ answer });

  offerCandidates.onSnapshot((snapshot) => {
    snapshot.docChanges().forEach((change) => {
      console.log(change);
      if (change.type === "added") {
        let data = change.doc.data();
        pc.addIceCandidate(new RTCIceCandidate(data));
      }
    });
  });
  hangupButton.disabled = false;
};
