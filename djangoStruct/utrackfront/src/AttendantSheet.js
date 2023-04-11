import React, { useState, useEffect } from "react";
import AttendantTable from "./AttendantTable";

function AttendantPage(props) {
  return (
    <div
      className="AttendantPage"
      style={{
        position: "fixed",
        top: "55%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        backgroundColor: "#F08000",
        borderRadius: 30,
        borderWidth: "thick",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        width: "35%",
      }}
    >
      <p style={{ color: "white", fontSize: "18px", marginTop: "5px" }}>
        <AttendantTable
          attendantName={props.attendantName}
          attendantData={props.attendantData}
          handleSelect={props.handleSelect}
        />
      </p>
    </div>
  );
}

export default AttendantPage;
