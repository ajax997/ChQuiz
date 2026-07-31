import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import {
    getAuth,
    onAuthStateChanged,
    signOut
} from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";

// Replace with your actual Firebase config
const firebaseConfig = {
        apiKey: "AIzaSyAETrg1LQk7Rxw2mWXjNAtv9RIfW9GpriA",
        authDomain: "chquiz-f8a7d.firebaseapp.com",
        projectId: "chquiz-f8a7d",
        storageBucket: "chquiz-f8a7d.firebasestorage.app",
        messagingSenderId: "341130057342",
        appId: "1:341130057342:web:167cafd452477f15dc6a2f",
        measurementId: "G-YXN5T1X3RY"
    };

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// Helper function: Calls Flask APIs with the fresh Firebase Bearer Token
export async function fetchWithAuth(url, options = {}) {
    const user = auth.currentUser;
    if (!user) {
        throw new Error("No user is currently signed in.");
    }

    // getIdToken() returns cached token or refreshes it if expired
    const idToken = await user.getIdToken();

    options.headers = {
        ...options.headers,
        "Authorization": `Bearer ${idToken}`,
        "Content-Type": "application/json"
    };

    return fetch(url, options);
}

// Global Auth State Observer
onAuthStateChanged(auth, async (user) => {
    if (user) {
        console.log("Firebase Auth State: Signed in as", user.email);
    } else {
        console.log("Firebase Auth State: Signed out");
    }
});