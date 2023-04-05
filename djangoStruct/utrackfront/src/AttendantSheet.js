import React, { useState, useEffect } from "react";

function AttendantPage() {
  return (
    <div
      className="AttendantPage"
      style={{
        background: "linear-gradient(to bottom right, #E35335, #eb8100)",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <h1 style={{ color: "white", fontSize: "32px", fontWeight: "bold" }}>
        Attendant Page
      </h1>
      <p style={{ color: "white", fontSize: "18px", marginTop: "10px" }}>
        Welcome to the Attendant Page!
      </p>
    </div>
  );
}

export default AttendantPage;
