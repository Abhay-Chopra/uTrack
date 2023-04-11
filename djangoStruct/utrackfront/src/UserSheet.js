import React, { useState, useEffect } from "react";
import UserTable from "./UserTable";
function UserSheet(props) {
  return (
    <div
      className="UserPage"
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
        <UserTable />
      </p>
    </div>
  );
}

export default UserSheet;
