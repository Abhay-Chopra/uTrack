import React, { useState, useEffect } from "react";
import axios from "axios";
import { useHistory, useLocation } from "react-router-dom";

function UserTable() {
  let userName = "";
  let userNum = "";
  const [sessions, setSessions] = useState([]);
  const location = useLocation();
  const history = useHistory();
  userName = location.state.params;
  userNum = location.state.anotherParam;

  const facilities = [
    { name: "Fitness Center", value: 1 },
    { name: "Aquatic Center", value: 2 },
    { name: "Racquet Center", value: 3 },
    { name: "Gymnastic Center", value: 4 },
    { name: "Bouldering Wall", value: 5 },
    { name: "Outdoor Center", value: 6 },
  ];

  const getFacilityName = (facilityId) => {
    const facility = facilities.find((f) => f.value === facilityId);
    return facility ? facility.name : "Unknown Facility";
  };

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/api/Checkins/?tracked_username=${userNum}`)
      .then((response) => {
        setSessions(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <div
      style={{
        height: "400px",
        overflow: "scroll",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <h2>
        <span>User: </span>
        <span>{userName}</span>
      </h2>
      <table>
        <thead>
          <tr>
            <th style={{ padding: "0 50px" }}>Date</th>
            <th style={{ padding: "0 50px" }}>Facility</th>
            <th style={{ padding: "0 50px" }}>Hours</th>
          </tr>
        </thead>
        <tbody>
          {sessions.map((session) => (
            <tr key={session.tracked_username}>
              <td>{session.date}</td>
              <td>{getFacilityName(session.facility_id)}</td>
              <td>{session.time_in_facility}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          width: "100%",
          marginTop: "1%",
        }}
      >
        <button
          onClick={() => {
            history.push("/");
            history.go(0);
          }}
          style={{ marginLeft: "45px" }}
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default UserTable;
